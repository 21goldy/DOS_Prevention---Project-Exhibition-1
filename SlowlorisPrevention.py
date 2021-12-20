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

    # blocking the IP using the uncomplicated firewall



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



    # list of connected IPs to the server and their details

    connectionDetails = os.popen("netstat -ntu|awk '{print $5}'|cut -d: -f1 -s|sort|uniq -c|sort -nk1 -r")

    readDetails = connectionDetails.read()

    print(readDetails)



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

                # os.system(str('ufw insert 2 deny from %s' % ips[x])) 

                os.system(str('ufw reload'))

                blocked_ips.append(ips[x])

                file.write(ips[x] + '\n')



    file.close()

    time.sleep(refreshRate)  



    # using iptables to block the ip from the system



    IPTABLES_LIST = os.popen("iptables -L")

    read_iptables_list = IPTABLES_LIST.read()

    # print(read_iptables_list)

    

    os.popen('iptables -I INPUT -s 10.0.2.15 -j DROP')

    

    # creating a blacklist of bad IPs [Run only once and comment the below line]

    os.popen("ipset create Slowloris_blacklist hash:ip hashsize 4096")

    

    # Set up iptables rules. Match with blacklist and drop traffic [Run only once and comment the below 2 lines]

    os.popen("iptables -I INPUT -m set --match-set Slowloris_blacklist src -j DROP") 

    os.popen("iptables -I FORWARD -m set --match-set Slowloris_blacklist src -j DROP")

    

    # Add a specific IP address to your newly created blacklist [Change the IP to the one you want to blacklist]

    os.popen("ipset add Slowloris_blacklist 10.0.2.15")

    

    # show details of the blocked ip

    blocking_IPTABLES = os.popen("ipset list")

    ip_IPTABLES = blocking_IPTABLES.read()

    print(ip_IPTABLES)  

    break


