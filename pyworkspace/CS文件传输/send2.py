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
def cal_md5(file_path):
    with open(file_path, 'rb') as fr:
        md5 = hashlib.md5()
        md5.update(fr.read())
        md5 = md5.hexdigest()
        return md5

class WSGIServer(object):
    def __init__(self, port):
        """初始化对象"""

        # 创建套接字
        self.tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 解决程序端口占用问题
        self.tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 绑定本地ip地址
        self.tcp_server_socket.bind(("", port))
        # 将套接字变为监听套接字，最大连接数量为100
        self.tcp_server_socket.listen(100)

    def run_forever(self):
        """设备连接"""
        while True:
            new_socket, client_addr = self.tcp_server_socket.accept()
            #print('%s|客户端%s已连接' % (time.strftime('%Y-%m-%d %H:%M:%S'), client_addr))
            print("设备{0}已连接".format(client_addr))
                # 2.创建线程处理设备的需求
            t1 = threading.Thread(target=self.service_machine, args=(new_socket, client_addr))
            t1.start()

    def service_machine(self, new_socket, client_addr):
        """业务处理"""
        while True:
            # 3.接收设备发送的数据，单次最大1024字节，按‘gbk'格式解码
            recv_data = new_socket.recv(1024).decode()
            # 4.如果设备发送的数据不为空
            if recv_data in os.listdir():
                print("您要下载的文件是：%s" % recv_data)
                file_info_dic = get_file_info(recv_data)
                j_head = json.dumps(file_info_dic)  # 将文件信息字典转成json字符串格式
                head = struct.pack('i', len(j_head))
                new_socket.send(head)
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
                            #print('%s|客户端%s已断开连接' % (time.strftime('%Y-%m-%d %H:%M:%S'), client_addr))
                            break
                    f.close()
                except Exception as ret:
                    print("发送文件失败:%s " % ret)
                else:
                    print("发送文件(%s)成功...." % recv_data)
            # else:
            #     print("找不到您要下载的文件")
            #     new_socket.send("找不到您要下载的文件")
            new_socket.close()
            break


def main():
    port=int(input('请输入监听的端口号:'))
    """创建一个服务器"""
    wsgi_server = WSGIServer(port)
    print("服务器已开启")
    wsgi_server.run_forever()

if __name__ == '__main__':
    main()