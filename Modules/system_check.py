import subprocess, psutil, time, sys

def getCpuStats():
    try:
        return str( int(psutil.cpu_percent()) )
    except:
        return "N/A"

def getMemStats():
    try:
        return str( round(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total, 1))
    except:
        return "N/A"

def getDate():
    try:
        cmd = "/usr/bin/date +'%a %d %b %r'"
        return ( str(subprocess.check_output(['bash', '-c', cmd]).decode(sys.stdout.encoding).strip()) )
    except:
        return "Unable To Fetch Date"