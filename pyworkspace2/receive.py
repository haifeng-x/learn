from socket import *
import socket
import os
import time
import threading
import hashlib
import struct
import json


def cal_md5(file_path):
    with open(file_path, 'rb') as fr:
        md5 = hashlib.md5()
        md5.update(fr.read())
        md5 = md5.hexdigest()
        return md5


def unpack_file_info(j_head):
    file_info_dic = {}
    file_info_dic = json.loads(j_head)  # 反序列化json字典，得到文件信息字典
    if not file_info_dic:
        print('文件不存在')

    file_size = file_info_dic.get('size')
    md5 = file_info_dic.get('md5')
    return file_size, md5
def jindu(dest_file_name, file_size):
    while True:
        if os.path.exists(dest_file_name):
            has_down = os.path.getsize(dest_file_name)
            jindu_num = (has_down/file_size)*100
            print("已下载%.2f%%" % jindu_num, end="\r")
            if int(jindu_num) == 100:
                break
            time.sleep(1)




def download_file():
    """下载文件"""
    server_addr = ('127.0.0.1', 8080)
    count = 1
    while True:
        if count > 10:
            time.sleep(1)
            print('%s|连接%s超时' % (time.strftime('%Y-%m-%d %H:%M:%S'), server_addr))
            break
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(('127.0.0.1', 8080))
            count = 1
            print('%s|服务端%s连接成功' % (time.strftime('%Y-%m-%d %H:%M:%S'), server_addr))
            while True:
                try:
                    dest_file_name = input('请输入您要下载的文件名:')
                    client.send(dest_file_name.encode())
                    head = client.recv(4)
                    j_dic_lenth = struct.unpack('i', head)[0]
                    j_head = client.recv(j_dic_lenth)  # 收json格式的信息字典
                    file_info_dic = json.loads(j_head)  # 反序列化json字典，得到文件信息字典


                    if not file_info_dic:
                        print('文件不存在')

                    file_size = file_info_dic.get('size')
                    md5_recv = file_info_dic.get('md5')

                    if file_size:
                        t = threading.Thread(target=jindu, args=(dest_file_name, file_size))
                        t.start()
                        try:

                            f = open(dest_file_name, "wb")
                            while True:
                                recv_data = client.recv(1024)
                                if recv_data:
                                    f.write(recv_data)
                                else:
                                    f.close()
                                    break
                        except Exception as ret:
                            print("下载文件出错:%s" % ret)
                        else:
                            print("下载(%s)已完成" % dest_file_name)

                        md5 = cal_md5(dest_file_name, )
                        if md5 != md5_recv:
                            print('MD5 compared fail!')
                        else:
                            print('Received successfully')
                            client.close()
                            break
                    else:
                        print("您要下载的文件不存在!")

                except ConnectionResetError:
                    print('%s|服务端%s已中断' % (time.strftime('%Y-%m-%d %H:%M:%S'), server_addr))
                    client.close()
                    break
        except ConnectionRefusedError:
            print('无法连接到服务端')
            count += 1





if __name__ == '__main__':
    download_file()


def main():
    os.makedirs("C:/Recvfile/FileCache", exist_ok=True)


if __name__ == '__main__':
    main()

