import os

while True:

    if os.geteuid() != 0:
        print("\n\nAuthentication Required!\n No root privileges.\n\n")
        break

    else:
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
        print(" ")
        break

