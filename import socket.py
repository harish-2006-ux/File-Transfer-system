import socket

s = socket.socket()
s.bind(("127.0.0.1", 9999))
s.listen(1)
print("LISTENING on 9999")
input()
