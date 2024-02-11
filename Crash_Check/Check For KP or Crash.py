import paramiko
import time

def enable_ssh(wtp_prof, fgt_ip, fgt_un, fgt_pwd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(fgt_ip, 22, fgt_un, fgt_pwd)

    channel = ssh.invoke_shell()
    commands = [
        'config wireless-controller wtp-profile',
        f'edit {wtp_prof}',
        'set allowaccess ssh',
        'set login-passwd-change yes',
        'set login-passwd admin',
        'end'
    ]
    for cmd in commands:
        channel.send(cmd + '\n')
        time.sleep(1)

    output = channel.recv(2048)
    print(output.decode('utf-8'))

    channel.close()
    ssh.close()

def ap_info(ap_ip, ap_pwd, fgt_ip, fgt_un, fgt_pwd):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(fgt_ip, 22, fgt_un, fgt_pwd)

        channel = ssh.invoke_shell()
        channel.send(f'execute ssh {ap_ip}\n')
        time.sleep(5)
        output = channel.recv(2048).decode('utf-8')

        if "password:" in output:
            channel.send(ap_pwd + '\n')
            time.sleep(5)

        channel.send('fap-get-status\n')
        time.sleep(2)
        output = channel.recv(2048).decode('utf-8')

        for line in output.split('\n'):
            if "Serial-Number:" in line or "Version:" in line:
                print(line.strip())

        channel.send('kp\n')
        time.sleep(5)
        output = channel.recv(2048).decode('utf-8')
        kp_line_check = "No kernel crash is found" in output

        if kp_line_check:
            print(f"{ap_ip} - No kernel crash is found")
        else:
            print(f"{ap_ip} - KP is seen")

        channel.send('crash\n')
        time.sleep(5)
        output = channel.recv(2048).decode('utf-8')
        crash_line = "Crash observed" in output

        if crash_line:
            print(f"{ap_ip} - Crash observed")
        else:
            print(f"{ap_ip} - No crash observed")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        channel.close()
        ssh.close()

def main():
    FGT_IP = input("FGT IP: ")
    FGT_UN = input("FGT Username: ")
    FGT_PWD = input("FGT Password: ")
    AP_PWD = input("AP Password: ")

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=FGT_IP, username=FGT_UN, password=FGT_PWD, timeout=60)

        cmd1 = "diagnose wireless-controller wlac -c wtp"
        stdin, stdout, stderr = client.exec_command(cmd1)
        result = stdout.read().decode('utf-8')

        ip_list = [line.split(':')[1].strip() for line in result.split('\n') if "local IPv4 addr" in line]
        wtp_profile = [line.split(':')[1].strip() for line in result.split('\n') if "cfg-wtp-profile" in line][1:]

        print(ip_list)
        print(wtp_profile)

        for w in wtp_profile:
            if w not in {"11n-only", "11ac-only"}:
                enable_ssh(w, FGT_IP, FGT_UN, FGT_PWD)
                print("Enabled SSH for wtp-profile:", w)

        for ip in ip_list:
            if ip not in {"127.0.0.1", "0.0.0.0"}:
                ap_info(ip, AP_PWD, FGT_IP, FGT_UN, FGT_PWD)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        client.close()

if __name__ == "__main__":
    main()
