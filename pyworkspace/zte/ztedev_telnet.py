import telnetlib
import time
from ftplib import FTP

# telnet
hostip = '192.168.1.1'
username = b'root'
password = b'Zte521'
token = b'/ #'

tnt = telnetlib.Telnet(hostip)
tnt.set_debuglevel(2)
tnt.read_until(b'Login:')
tnt.write(username)
tnt.write(b'\n')

tnt.read_until(b'Password:')
tnt.write(password)
tnt.write(b'\n')
tnt.read_until(token)

tnt.write(b'redir a\n')
tnt.read_until(token)
tnt.write(b'redir p\n')
tnt.read_until(token)
tnt.write(b'sendcmd -pc restart 0\n')
tnt.read_until(token)
tnt.write(b'killall vsftpd && vsftpd -s&\n')
tnt.read_until(token)

# ftp
host = '192.168.1.1'
port = 21
user = 'root'
pwd = 'Zte521'
bufsize = 1024
remotepath = 'var/test_ssu'
ftp = FTP()
time.sleep(1)
ftp.connect(host, port)
time.sleep(0.001)
ftp.login(user, pwd)
time.sleep(0.001)
ftp.set_debuglevel(2)

# data sampling
request_samples = 500
k = 0
while k < request_samples:
    tnt.write(b'iwpriv wifi0 setcmd "ssutest 2 0 1 0 0 1 0 0 0 10"\n')
    tnt.read_until(token)
    tnt.write(b'iwpriv wifi0 setcmd "ssutest 1"\n')
    tnt.read_until(token)

    localpath = 'D:\ZTE\ZTEdev\Bluetooth\ssu' + str(k) + '.dat'
    fid = open(localpath, 'wb')
    ftp.retrbinary('RETR ' + remotepath, fid.write, bufsize)
    fid.close()

    time.sleep(0.001)
    k = k + 1

ftp.quit()
tnt.close()
print('%d samples collected.\n', k)