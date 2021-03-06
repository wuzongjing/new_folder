from socket import *
from select import *
import re


# 封装所有web后端功能
class WebServer:
    def __init__(self, host="0.0.0.0", port=80, html=None):
        self.host = host
        self.port = port
        self.html = html
        self.map={}
        self.create_socket()
        self.bind()

    # 创建设置套接字:
    def create_socket(self):
        self.sock = socket()
        self.sock.setblocking(False)

    # 绑定地址:
    def bind(self):
        self.address = (self.host, self.port)
        self.sock.bind(self.address)

    # 启动整个服务
    def start(self):
        self.sock.listen(5)
        print("Listen the port %d" % self.port)
        # 先监控监听套接字
        ep=epoll()
        self.map={self.sock.fileno():self.sock}
        ep.register(self.sock,EPOLLIN)
        while True:
            events=ep.poll()
            print("你有新的IO需要处理哦",events)
            # 处理就绪的IO
            for fd,event in events:
                # 有客户端连接
                if fd==self.sock.fileno():
                    connfd, addr = self.map[fd].accept()
                    print("Connect from", addr)
                    # 将客户端连接套接字也监控起来
                    connfd.setblocking(False)
                    ep.register(connfd,EPOLLIN|EPOLLET)
                    self.map[connfd.fileno()]=connfd
                else:
                    try:
                        self.handle(fd)
                    except:
                        pass
                    # 处理浏览器端发的请求
                    del self.map[fd]
                    self.map[fd].close()


    # 处理客户端请求:
    def handle(self, connfd):
        # http请求
        request = connfd.recv(1024 * 10).decode()
        # 使用正则表达式匹配请求内容:
        pattern = r"[A-Z]+\s+(?P<info>/\S*)"
        result = re.match(pattern, request)
        if request:
            # 提取请求内容:
            info = result.group("info")
            print("请求内容:", info)
            self.send_html(connfd, info)
        # if not request:
        #     return
        # request.split(" ")

    def send_html(self, connfd, info):
        if info == "/":
            filename = self.html + "/index.html"
        else:
            filename = self.html + info
        # 打开判断文件是否存在
        try:
            file = open(filename, "rb")
        except:
            response = "HTTP/1.1 404 NotFound\r\n"
            response += "Content-Type:text/html\r\n"
            response += "\r\n"
            with open(self.html + "/404.html") as file:
                response += file.read()
            response = response.encode()
        else:
            data = file.read()  # 字节串
            response = "HTTP/1.1 200 ok\r\n"
            response += "Content-Type: text/html\r\n"
            response += "Content-Length:%d\r\n" % len(data)
            response += "\r\n"
            response = response.encode() + data
            file.close()
        finally:
            connfd.send(response)
        connfd.close()


if __name__ == '__main__':
    # 需要用户决定的:地址  网页
    httpd = WebServer(host="0.0.0.0",
                      port=9999,
                      html="/home/tarena/month2/Network/═°┬τ▓ó╖ó▒α│╠/info/static")
    # 启动服务
    httpd.start()