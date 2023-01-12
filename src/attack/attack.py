import subprocess
import re
import nmap
import requests
from bs4 import BeautifulSoup

target_url = "10.0.0.64" #this should be a parameter

#check which ports are open
nm = nmap.PortScanner()
scan_results = nm.scan(target_url, arguments="-sT")

tcp_ports = [port for port in scan_results['scan'][target_url]['tcp'].keys() if scan_results['scan'][target_url]['tcp'][port]['state'] == 'open' and scan_results['scan'][target_url]['tcp'][port]['name'] == 'http']

#attacking every http ports
for port in tcp_ports:

    target_url="http://10.0.0.64:"
    target_url+=str(port)+'/DVWA/' #in our case we have the DVWA cause we know we want to hit here

    #gathering every pages we can in order to attack them (work better for known directories than dirbuster because we use hrefs)
    pages_to_attack=[]
    response=requests.get(target_url)
    soup = BeautifulSoup(response.content,"html.parser")
    for link in (soup.find_all("a")):

        reference = link.get('href')

        if not(reference.startswith('http')): #outside links are banned, we don't want to attack internet !
            pages_to_attack.append(target_url+reference)

    print(pages_to_attack)

    #use dirbuster to find hidden directories and files on the target website
    dirbuster_cmd = f"dirb {target_url} -S"
    dirbuster_output = subprocess.run(dirbuster_cmd, shell=True, capture_output=True).stdout.decode()

    for line in dirbuster_output.split("\n"):

        if line.startswith("==>") or line.startswith("+"):
            print(line)

    # Use PwnXSS to detect potential XSS vulnerabilities
    xss_cmd = f"python3 PwnXSS/pwnxss.py -u {target_url} --depth 5"
    xss_output = subprocess.run(xss_cmd, shell=True, capture_output=True).stdout.decode()

    # Search for XSS vulnerabilities in the PwnXSS output
    xss_vulnerabilities = []
    for line in xss_output.split("\n"):
        if "CRITICAL" in line:
            print(line)
            xss_vulnerabilities.append(line)

    if xss_vulnerabilities:
        for vulnerability in xss_vulnerabilities:
            print(vulnerability)
    else:
        print(f"No potential XSS vulnerabilities were detected on {target_url}.")

    # Use sqlmap to detect SQL injections and display available databases (commented because too verbose, but it works)
    #sqlmap_cmd = 'sqlmap -u "http://10.0.0.64/DVWA/vulnerabilities/sqli_blind/?id=1&Submit=Submit#" -dump -v 0 --batch'
    #sqlmap_output = subprocess.run(sqlmap_cmd, shell=True)
    #print(sqlmap_output)

    #for url in pages_to_attack: #this version will work if there is a way to mine parameters

        # Use sqlmap to detect SQL injections and display available databases
        #sqlmap_cmd = f"sqlmap -u {url} -dump -v 0 --batch"
        #sqlmap_output = subprocess.run(sqlmap_cmd, shell=True)

        #find a way to scrap this output 
        #print(sqlmap_output)

