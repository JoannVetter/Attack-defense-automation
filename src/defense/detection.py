import re
import http.server
import time

class AttackHandler(http.server.BaseHTTPRequestHandler):
    def block_attacks(self):
        # Block SQL injection attacks
        if "DROP TABLE" in self.requestline or "INSERT INTO" in self.requestline:
            return True

        # Block XSS attacks
        if "<script>" in self.requestline or "<iframe>" in self.requestline:
            return True

        # Block command injection attacks
        if "|" in self.requestline or "&" in self.requestline:
            return True

        # Block arbitrary file access attacks
        if "../../etc/passwd" in self.requestline or "../../" in self.path:
            return True

        # Block spam of requests
        if self.headers.get("X-Spam") == "Yes":
            return True

        # Block null byte injection attacks
        if "\x00" in self.requestline:
            return True

        # Block HTTP response splitting attacks
        if "\r\n" in self.requestline:
            return True

        # Block cross-site request forgery attacks
        if "csrf_token" not in self.headers:
            return True

        # Block remote file inclusion attacks
        allowed_paths = ['/index.html', '/style.css', '/scripts.js']
        if self.path not in allowed_paths:
            return True

        return False

    def do_GET(self):
        if self.block_attacks():
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Attack detected and blocked.")
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"No attacks detected.")
        
    def log_request(self, code='-', size='-'):
        # Override log_request method to include IP ban
        if code == 400:
            self.banned_ips.add(self.client_address[0])
            timer = threading.Timer(300.0, self.unban_ip, [self.client_address[0]])
            timer.start()
        super().log_request(code, size)

    def unban_ip(self, ip):
        # Remove IP from banned_ips set after 5 minutes
        self.banned_ips.remove(ip)

def run(server_class=http.server.HTTPServer, handler_class=AttackHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

run()
