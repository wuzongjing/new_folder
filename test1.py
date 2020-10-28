from socket import *

s=socket()
s.bind(("0.0.0.0",9999))
s.listen(5)


c,addr =s.accept()
print("Connect from ",addr)


data=c.recv(1024*10).decode()
tmp=data.split(" ")
if tmp[1]=="/python":
    with open("/home/tarena/month2/day17/day17-1/day17/Python.html")as f:
        content=f.read()
    response= "HTTP/1.1 200 ok\r\n"
    response+="Content-Type:text/html\r\n"
    response+="\r\n"
    response+=content
else:
    response="HTTP/1.1 404 NotFound\r\n"
    response += "Content-Type:text/html\r\n"
    response += "\r\n"
    response += "Sorry...."

c.send(response.encode())

c.close()
s.close()