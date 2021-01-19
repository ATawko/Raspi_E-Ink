import subprocess, sys

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