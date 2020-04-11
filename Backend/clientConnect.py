import socket

address_to_server = ('localhost', 5001)
token = 'hui'
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(address_to_server)
client.send(bytes(token, encoding='UTF-8'))
data = client.recv(1024)
print(str(data))