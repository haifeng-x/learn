import socketserver
import time
import socket
import os
import time
import hashlib
import struct
import json

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



class MyTcpHandler(socketserver.BaseRequestHandler):
    # 到这里表示服务端已监听到一个客户端的连接请求,将通信交给一个handle方法实现，自己再去监听客户连接请求
    def handle(self):
        # 建立双向通道，进行通信
        print('%s|客户端%s已连接' % (time.strftime('%Y-%m-%d %H:%M:%S'), self.client_address))
        while True:
            try:
                recv_data = self.request.recv(1024).decode()

                if recv_data in os.listdir():
                    print("您要下载的文件是：%s" % recv_data)

                    file_info_dic = get_file_info(recv_data)

                    j_head = json.dumps(file_info_dic)  # 将文件信息字典转成json字符串格式
                    head = struct.pack('i', len(j_head))
                    self.request.send(head)
                    self.request.send(j_head.encode('utf-8'))
                    try:
                        f = open(recv_data, "rb")
                        while True:
                            content = f.read(1024)
                            if content:
                                # 如果从文件中读取了数据，那么就给tcp客户端发送过去
                                self.request.send(content)
                            else:
                                break

                        f.close()
                    except Exception as ret:
                        print("发送文件失败:%s " % ret)
                    else:
                        print("发送文件(%s)成功...." % recv_data)
                else:
                    print("找不到您要下载的文件")
                    self.request.send("找不到您要下载的文件".encode())
            except ConnectionResetError:
                print('%s|客户端%s已断开连接' % (time.strftime('%Y-%m-%d %H:%M:%S'), self.client_address))
                break


if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(('127.0.0.1', 8080), MyTcpHandler)  # 绑定服务端IP和PORT，并产生并发方法对象
    print('等待连接请求中...')
    server.serve_forever()  # 服务端一直开启