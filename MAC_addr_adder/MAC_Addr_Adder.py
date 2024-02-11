start_mac = int("0xa1b1ccdd0000", 16)

for i in range(100):
    mac = start_mac + i
    mac_str = "{:012X}".format(mac)
    print(f'edit NT0{i}')
    print('set mac ' + ':'.join(mac_str[j:j+2] for j in range(0, len(mac_str), 2)))
    print('set ssid-policy T_Test')
    print('next')
