#Import Standard Python Libraries
import sys, time, traceback
from PIL import Image,ImageDraw,ImageFont

#Import Waveshare Drivers
import Drivers.epd2in13     as epd2in13
import Drivers.epdconfig    as epdconfig

#Import Custom Modules
import Modules.ssh_check        as ssh_check
import Modules.system_check     as system_check
import Modules.network_check    as network_check
import Modules.rtl_tcp_manager  as rtl_tcp

itteration = 0
ip = "127.0.0.1"

while True:
    try:
        netName     = network_check.getNetworkName()
        ipAddr      = network_check.getIpAddress()
        tcpStatus   = rtl_tcp.startRtlTcp(ipAddr)
        date        = system_check.getDate()
        ssh         = ssh_check.checkSshConnections()
        cpu         = system_check.getCpuStats()
        mem         = system_check.getMemStats()

        itteration += 1

        epd = epd2in13.EPD()
        epd.init(epd.FULL_UPDATE)
        epd.Clear(0xFF)

        # Drawing on the image
        image = Image.new('1', (epd2in13.EPD_HEIGHT, epd2in13.EPD_WIDTH), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(image)

        #Draw TCP Status
        draw.text((0, 0), tcpStatus, fill = 0)
    
        #Draw CPU & Mem Stats
        draw.text((200, 0), "CPU:", fill = 0)
        draw.text((225, 0), cpu, fill = 0)
        draw.text((200, 10), "MEM:", fill = 0)
        draw.text((225, 10), mem, fill = 0)

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
