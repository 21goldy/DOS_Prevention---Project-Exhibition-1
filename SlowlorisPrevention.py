import os
import subprocess
import time

allowedConnections = 15
refreshRate = 3

blocked_ips = []
blank_list = []
ips = []

while True:
    if os.geteuid() != 0:
        print("Authentication Required!\n No root privileges.")
        break
    if os.path.isdir('/etc/ufw/'):
        Uncomplicated_firewall = subprocess.Popen(["ufw", "status"], stdout=subprocess.PIPE)
        response = str(Uncomplicated_firewall.communicate())
        if 'inactive' in response:
            print('UFW Disabled. To enable, enter `sudo ufw enable` into your terminal.')
            break
    else:
        print('UFW not installed. To install, enter `sudo apt-get install ufw` into your terminal.')
        break
    file = open('blockedIPs.txt', 'a')
    connectionDetails = os.popen("netstat -ntu|awk '{print $5}'|cut -d: -f1 -s|sort|uniq -c|sort -nk1 -r")
    readDetails = connectionDetails.read()
    scrapedIPs = list(readDetails.split())
    for x in range(len(scrapedIPs)):
        if x % 2 == 0:
            blank_list.append(scrapedIPs[x])
        else:
            ips.append(scrapedIPs[x])
    for x, y in enumerate(blank_list):
        if int(y) > allowedConnections:
            if ips[x] != '127.0.0.1' and ips[x] not in blocked_ips:
                print('Blocking %s with %d connections' % (ips[x], int(y)))
                os.system(str('ufw insert 2 deny from %s' % ips[x]))
                os.system(str('ufw reload'))
                blocked_ips.append(ips[x])
                file.write(ips[x] + '\n')
    file.close()
    time.sleep(refreshRate)
