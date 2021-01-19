import subprocess, sys

def getNetworkName():
    try:
        return subprocess.check_output(['/usr/sbin/iwgetid', '-r'])
    except:
        return "No Network"

def getIpAddress():
    try:
        #return subprocess.check_output(['hostname', '-I'])

        cmd = '/usr/sbin/ifconfig wlan0 | /usr/bin/grep "inet" | /usr/bin/grep -v "inet6" | /usr/bin/cut -f1-2 -d"n" | /usr/bin/sed "s/ //g" | /usr/bin/sed "s/^.\{4\}//"'
        ip = subprocess.check_output(['bash', '-c', cmd]).decode(sys.stdout.encoding).strip()
        return ip

    except:
        return "No IP"