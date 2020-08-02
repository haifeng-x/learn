import threading
import socket
import os
import time
import hashlib
import struct
import json

def get_file_info(file_path):
    file_info = {}
    file_size = os.path.getsize(file_path)
    md5 = cal_md5(file_path)
    file_info['size']=file_size
    file_info['md5'] = md5
    return file_info
#计算文件md5值
def cal_md5(file_path):
    with open(file_path, 'rb') as fr:
        md5 = hashlib.md5()
        md5.update(fr.read())
        md5 = md5.hexdigest()
        return md5

def send_file(new_socket, client_addr):
    # 接收客户端需下载文件文件名
    recv_data = new_socket.recv(1024).decode()
    if recv_data in os.listdir():
        print("您要下载的文件是：%s" % recv_data)
        file_info_dic = get_file_info(recv_data)
        # 将文件信息字典转成json字符串格式
        j_head = json.dumps(file_info_dic)
        head = struct.pack('i', len(j_head))
        #发送数据报头长度
        new_socket.send(head)
        # 发送数据报头内容
        new_socket.send(j_head.encode('utf-8'))
        try:
            f = open(recv_data, "rb")
            while True:
                content = f.read(1024)
                if content:
                    # 如果从文件中读取了数据，那么就给tcp客户端发送过去
                    new_socket.send(content)
                else:
                    print('设备{0}断开连接...'.format(client_addr))
                    break
            f.close()
        except Exception as ret:
            print("发送文件失败:%s " % ret)
        else:
            print("发送文件(%s)成功...." % recv_data)
        new_socket.close()

def main():
    port=int(input('请输入监听的端口号:'))
    # 创建套接字
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 解决程序端口占用问题
    tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # 绑定本地ip地址
    tcp_server_socket.bind(("", port))
    # 将套接字变为监听套接字，最大连接数量为100
    tcp_server_socket.listen(100)
    print("服务器已开启")
    while True:
        new_socket, client_addr = tcp_server_socket.accept()
        print("设备{0}已连接".format(client_addr))
        # 2.创建线程处理设备的需求
        t1 = threading.Thread(target=send_file, args=(new_socket, client_addr))
        t1.start()

if __name__ == '__main__':
    main()