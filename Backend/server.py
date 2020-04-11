import socket
import random
import string

# Задаем адрес сервера
SERVER_ADDRESS = ('localhost', 5001)

# Настраиваем сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(SERVER_ADDRESS)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.listen(10)
print('server is running, please, press ctrl+c to stop')

# Слушаем запросы
countOfSpies = 1
countOfPlayers = 5
token = 'hui'
while True:
    connection, address = server_socket.accept()
    data = connection.recv(1024).decode()
    if 'CREATE' in data:
       #token = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(4))
        connection.send(bytes(token, encoding='UTF-8'))
    elif token in data:
        role = random.randint(0,1)
        if role == 0:
            connection.send(bytes('peaceful', encoding='UTF-8'))
        else:
            connection.send(bytes('spy', encoding='UTF-8'))
    connection.close()