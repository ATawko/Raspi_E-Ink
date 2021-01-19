import subprocess, sys

def checkTCPStatus():
    try:
        cmd = '/usr/bin/screen -ls | /usr/bin/grep -o tcp'
        if ( "tcp" in str(subprocess.check_output(['bash', '-c', cmd]).decode(sys.stdout.encoding).strip() ) ):
            return True
        else: 
            return False

    except:
        pass

def startRtlTcp(ip):

    if checkTCPStatus():
        return "RTL TCP Running"
    else:
        try:
            cmd = "/usr/bin/screen -dm -S rtl_tcp /usr/local/bin/rtl_tcp -s 1024000 -a " + ip
            subprocess.check_output(['bash', '-c', cmd]).decode(sys.stdout.encoding).strip()
            if checkTCPStatus():
                return "RTL TCP Started"
            else: 
                return "RTL TCP Unable to Start"
        except:
            return "RTL TCP Error"