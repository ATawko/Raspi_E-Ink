import epd2in13
import time, subprocess, sys
from PIL import Image,ImageDraw,ImageFont
import traceback

itteration = 0
ip = "127.0.0.1"

def checkSshConnections():
    try:
        cmd = "/usr/bin/netstat -tnpa | /usr/bin/grep 'ESTABLISHED.*sshd'"
        ssh = str( subprocess.check_output(['bash', '-c', cmd]).decode(sys.stdout.encoding).strip() )

        if not ssh:
            return "No Active SSH Sessions"
        else:
            return "Active SSH Sessions"
    except:
        return "SSH Fetch Error"


def getNetworkName():
    try:
        return subprocess.check_output(['/usr/sbin/iwgetid', '-r'])
    except:
        return "No Network"

def getIpAddress():
    try:
        #return subprocess.check_output(['hostname', '-I'])
        global ip

        cmd = '/usr/sbin/ifconfig wlan0 | /usr/bin/grep "inet" | /usr/bin/grep -v "inet6" | /usr/bin/cut -f1-2 -d"n" | /usr/bin/sed "s/ //g" | /usr/bin/sed "s/^.\{4\}//"'
        ip = subprocess.check_output(['bash', '-c', cmd]).decode(sys.stdout.encoding).strip()
        return ip

    except:
        return "No IP"

def checkTCPStatus():
    try:
        cmd = '/usr/bin/screen -ls | /usr/bin/grep -o tcp'
        
        if ( "tcp" in str(subprocess.check_output(['bash', '-c', cmd]).decode(sys.stdout.encoding).strip() ) ):
            return True
        else: 
            return False

    except:
        pass

def startRtlTcp():
    global ip
    #print("IP:")
    #print(ip)

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

def getDate():
    try:
        cmd = "/usr/bin/date +'%a %d %b %r'"
        return ( str(subprocess.check_output(['bash', '-c', cmd]).decode(sys.stdout.encoding).strip()) )
    except:
        return "Unable To Fetch Date"


while True:
    try:
        netName = getNetworkName()
        ipAddr = getIpAddress()
        tcpStatus = startRtlTcp()
        date = getDate()
        ssh = checkSshConnections()

        itteration += 1

        epd = epd2in13.EPD()
        epd.init(epd.FULL_UPDATE)
        epd.Clear(0xFF)

        # Drawing on the image
        image = Image.new('1', (epd2in13.EPD_HEIGHT, epd2in13.EPD_WIDTH), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(image)

        #Draw TCP Status
        draw.text((0, 0), tcpStatus, fill = 0)
    
        #Draw SSH Sessions
        draw.text((0, 20), ssh, fill = 0)

        #Draw itteration progress
        draw.text((0, 50), 'Itteration: ', fill = 0)
        draw.text((70, 50), str(itteration), fill = 0)

        #Draw Date
        draw.text((0, 80), "Last Update:", fill = 0)
        draw.text((72, 80), date, fill = 0)

        #Draw Connection Status Info
        draw.text((0, 90), '------------------------------------------', fill = 0)
        draw.text((0, 100), "Connected Network:", fill = 0)
        draw.text((110, 100), netName, fill = 0)
        draw.text((0, 110), 'Connection Status:', fill = 0)
        draw.text((110, 110), ipAddr, fill = 0)

        epd.display(epd.getbuffer(image))

    except:
        print('traceback.format_exc():\n%s',traceback.format_exc())
        exit()

    if itteration == 5:
        exit()

    time.sleep(20)
