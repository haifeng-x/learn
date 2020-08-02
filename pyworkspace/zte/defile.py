import os

for file in os.listdir('D:\ZTE\ZTEdev\Bluetooth'):
    fsize = os.path.getsize(f'D:\ZTE\ZTEdev\Bluetooth\{file}')
    if(fsize<1000000):
        os.remove(f'D:\ZTE\ZTEdev\Bluetooth\{file}')