import socket
import random
import string

# Задаем адрес сервера
SERVER_ADDRESS = ('localhost', 5050)

# Настраиваем сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(SERVER_ADDRESS)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.listen(10)
print('server is running, please, press ctrl+c to stop')


spy_amount = []
players_amount = []
tokens = []


# Слушаем запросы
while True:

    connection, address = server_socket.accept()
    data = connection.recv(1024).decode().split()

    # Выдача токена пользователю
    if 'CREATE_LOBBY' in data:
        token = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(4))
        tokens.append(token)
        spy_amount.append(int(data[1])
        players_amount.append(int(data[2])
        connection.send(bytes(token, encoding='UTF-8'))
    
    # Подключение мазефакера к лобби и выдача ему роли
    elif data in tokens: 

        # Находим конкретное лобби по указанному токену
        spy_amount_current = spy_amount[tokens.index(data)]
        players_amount_current = players_amount[tokens.index(data)]

        # Определяем роли
        while (spy_amount_current != 0 and players_amount_current != 0):
            role = random.randint(0,1)
            if role == 1 and spy_amount_current != 0:
                connection.send(bytes('spy', encoding='UTF-8'))
                spy_amount_current -= 1
            elif role == 0 and players_amount != 0:
                connection.send(bytes('peaceful', encoding='UTF-8'))
                players_amount_current -= 1
        # Проверка на неверно введенный токен
        elif not token in data:
            connection.send(bytes('invalid token', encoding='UTF-8'))
            
    # Закрываем сокет (бб мазафакер)
    connection.close()