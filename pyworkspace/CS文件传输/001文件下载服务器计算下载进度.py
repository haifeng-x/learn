import socket
import os
import time
import hashlib
import struct
import json
BUFFER_SIZE = 1024
def cal_md5(file_path):
    with open(file_path, 'rb') as fr:
        md5 = hashlib.md5()
        md5.update(fr.read())
        md5 = md5.hexdigest()
        return md5

def get_file_info(file_path):
    file_info = {}
    file_size = os.path.getsize(file_path)
    md5 = cal_md5(file_path)
    file_info['size']=file_size
    file_info['md5'] = md5
    return file_info

def send_file():

    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 绑定本地信息
    tcp_server_socket.bind(("", 8080))

    # 让套接字变为监听套接字（被动套接字）
    tcp_server_socket.listen(128)

    # 使用accept等待新客户端的链接
    client_socket,client_addr = tcp_server_socket.accept()
    print("一个新的客户端来到了...信息是：", client_addr)


    recv_data = client_socket.recv(1024).decode()

    if recv_data in os.listdir():
        print("您要下载的文件是：%s" % recv_data)
        # 发送下载文件大小
        #client_socket.send(str(os.path.getsize(recv_data)).encode())

        file_info_dic = get_file_info(recv_data)
        #file_head = struct.pack(HEAD_STRUCT,file_size, md5)
        #client_socket.send((file_info_dic).encode())

        j_head = json.dumps(file_info_dic)  # 将文件信息字典转成json字符串格式
        head = struct.pack('i', len(j_head))
        client_socket.send(head)
        client_socket.send(j_head.encode('utf-8'))
        try:
            f = open(recv_data, "rb")
            while True:
                content = f.read(1024)
                if content:
                    # 如果从文件中读取了数据，那么就给tcp客户端发送过去
                    client_socket.send(content)
                else:
                    break

            f.close()
        except Exception as ret:
            print("发送文件失败:%s " % ret)
        else:
            print("发送文件(%s)成功...." % recv_data)
    else:
        print("找不到您要下载的文件")
        client_socket.send("找不到您要下载的文件".encode())

    client_socket.close()
    tcp_server_socket.close()


if __name__ == '__main__':

    send_file()
