mac="0Xa1b1ccdd0000"

for i in range(100):
    mac = "{:012X}".format(int(mac, 16) + 1)
    print ('edit NT0'+str(i))
    print('set mac ' + ':'.join(mac[i] + mac[i + 1] for i in range(0, len(mac), 2)))
    print('set ssid-policy T_Test')
    print('next')