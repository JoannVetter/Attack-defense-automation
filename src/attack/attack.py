import subprocess
import re
import nmap

target_url = "10.0.0.64"
nmap_output_file = "nmap_output.txt"
sqlmap_output_file = "sqlmap_output.txt"
dirbuster_output_file = "dirbuster_output.txt"
nikto_output_file = "nikto_output.txt"

# Check which ports are open
nm = nmap.PortScanner()
scan_results = nm.scan(target_url, arguments="-sT")

tcp_ports = [port for port in scan_results['scan'][target_url]['tcp'].keys() if scan_results['scan'][target_url]['tcp'][port]['state'] == 'open' and scan_results['scan'][target_url]['tcp'][port]['name'] == 'http']

for port in tcp_ports:

    target_url="http://10.0.0.64:"
    target_url+=str(port)+'/'

    # Use sqlmap to detect SQL injections and display available databases
    sqlmap_cmd = "sqlmap --crawl=2 -u {} --dbs --batch > {}".format(target_url, sqlmap_output_file)
    subprocess.run(sqlmap_cmd, shell=True)

    # Use dirbuster to find hidden directories and files on the target website
    dirbuster_cmd = "dirb {} ".format(target_url)
    dirbuster_output = subprocess.run(dirbuster_cmd, shell=True, capture_output=True).stdout.decode()
    print(dirbuster_output)
    # Search for sensitive files in the dirbuster output
    sensitive_files = []
    for line in dirbuster_output.split("\n"):
        if line.startswith("/path/to/sensitive/file"):
            sensitive_files.append(line)

    if sensitive_files:
        print("The following sensitive files were found:")
        for file in sensitive_files:
            print(file)
    else:
        print("No sensitive files were found.")

    # Use xsser to detect potential XSS vulnerabilities
    xsser_cmd = "xsser -u {} --batch".format(target_url)
    xsser_output = subprocess.run(xsser_cmd, shell=True, capture_output=True).stdout.decode()

    # Search for XSS vulnerabilities in the xsser output
    xss_vulnerabilities = []
    for line in xsser_output.split("\n"):
        if "XSS found" in line:
            xss_vulnerabilities.append(line)

    if xss_vulnerabilities:
        print("Potential XSS vulnerabilities were detected:")
        for vulnerability in xss_vulnerabilities:
            print(vulnerability)
    else:
        print("No potential XSS vulnerabilities were detected.")

    # Use Nikto to scan the target website
    nikto_cmd = "nikto -h {} -root /directory/to/scan -User-Agent 'Custom User Agent String' -useproxy http://proxy_server:proxy_port -output {} -ssl -evasion 5 -Format html -Tuning 685,938,958 -Ask no -Display V -dbcheck -nointeractive".format(target_url, nikto_output_file)
    subprocess.run(nikto_cmd, shell=True)
