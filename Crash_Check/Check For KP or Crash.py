import paramiko
import time

################-Function to enable ssh for wtp-profile
def enable_ssh (wtp_prof,fgt_ip,fgt_un, fgt_pwd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(fgt_ip, 22, fgt_un, fgt_pwd)

    channel = ssh.invoke_shell()
    channel.send('config wireless-controller wtp-profile\n')
    time.sleep(1)
    # output=channel.recv(2048)

    channel.send('edit '+wtp_prof+'\n')
    time.sleep(1)
    # output=channel.recv(2048)

    channel.send('set allowaccess ssh\n')
    time.sleep(1)
    # output=channel.recv(2048)

    channel.send('set login-passwd-change yes\n')
    time.sleep(1)
    # output=channel.recv(2048)
    channel.send('set login-passwd admin\n')
    time.sleep(1)
    # output=channel.recv(2048)

    channel.send('end\n')
    time.sleep(1)
    output=channel.recv(2048)

    channel.close()
    ssh.close()


########Funtion to connect to AP & check for KP & Crash
def ap_info (ap_ip,ap_pwd,fgt_ip,fgt_un,fgt_pwd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(fgt_ip, 22, fgt_un, fgt_pwd)
    channel = ssh.invoke_shell()
    kp_line_check = ""

    channel.send('execute ssh '+ap_ip+'\n')
    time.sleep(90)
    output = channel.recv(2048)
    for p in output.decode('utf8').split('\n'):
        if "No route to host" in p:
            print("            ")
            print("Could not SSH to "+ap_ip)
        elif "Connection timed out" in p:
            print("            ")
            print("Could not SSH to " + ap_ip)
        elif "password:" in p:
            channel.send(ap_pwd+'\n')
            time.sleep(1)
            channel.send('\n')

            time.sleep(1)
            channel.send('fap-get-status\n')
            time.sleep(1)
            output = channel.recv(2048)
            print("           ")
            for l in output.decode('utf8').split('\n'):
                if "Serial-Number:" in l:
                    print(l)
                elif "Version:" in l:
                    print(l)
            time.sleep(2)
        ###########Check for KP
            channel.send('kp\n')
            time.sleep(5)
            output = channel.recv(2048)
            for KP_line in output.decode('utf8').split('\n'):
                if "No kernel crash is found" in KP_line:
                    kp_line_check = "No kernel crash is found"

            if kp_line_check == "No kernel crash is found":
                print(ap_ip+" - No kernel crash is found")
            else:
                print(ap_ip+" - KP is seen")
        #########Check for Crash
            channel.send('crash\n')
            time.sleep(5)
            output = channel.recv(2048)
            for crash_line in output.decode('utf8').split('\n'):
                if "firmware" in crash_line:
                    crash_line = "Crash observed"

            if crash_line == "Crash observed":
                print(ap_ip+" - Crash observed")
            else:
                print(ap_ip+" - No crash observed")

            channel.close()
            ssh.close()

########Login to FGT##################

FGT_IP=input("FGT IP: ")
FGT_UN=input("FGT Username: ")
FGT_PWD=input("FGT Password: ")
AP_PWD=input("AP Password: ")
try:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=FGT_IP, username=FGT_UN, password=FGT_PWD, timeout= 60)

except Exception as e:
    print(e)

else:
#######Exe command on FGT and get list of connected WTP IP and its WTP-Profile
    cmd1 = "diagnose wireless-controller wlac -c wtp"
    stdin, stdout, stderr = client.exec_command(cmd1)
    result = stdout.read()
    error = stderr.read()
    ip_list = []
    wtp_profile = []
    ip2 = []
    ip_str = ""
    wtp_str = ""
    for line in result.decode('utf8').split('\n'):
            if "local IPv4 addr" in line:
                line_new = line.split(':')
                #print(line_new)
                ip = line_new[1]
                ip_str = ip_str + ip
                #print(ip_str)
                ip_list = ip_str.split(" ")

            elif "cfg-wtp-profile" in line:
                l2 = line.split(':')
                prof = l2[1]
                wtp_str = wtp_str + prof
                wtp_profile = wtp_str.split(" ")

    wtp_profile = wtp_profile[1:]
    ip_list = ip_list[1:]
    print(ip_list)
    print(wtp_profile)
    client.close()

    for w in wtp_profile:
        if w == "11n-only":
            pass
        elif w == "11ac-only":
            pass
        else:
            enable_ssh(w, FGT_IP, FGT_UN, FGT_PWD)
            print("Enabled SSH for wtp-profile: "+w)

    for ip in ip_list:
        if ip == "127.0.0.1":
            pass
        elif ip == '0.0.0.0':
            pass
        else:
            ap_info(ip,AP_PWD,FGT_IP,FGT_UN,FGT_PWD)
