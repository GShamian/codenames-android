import socket
import random
import string
import pickle

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
database = ['Bank', 'Hospital', 'Military unit', 'Casino',
            'Hollywood', 'Titanic', 'The Death Star', 'Hotel',
            'Russian Railways', 'Malibu Beach', 'Police Station',
            'Restaurant', 'University', 'Lyceum', 'SPA', 'Plane']

# Слушаем запросы
while True:

    connection, address = server_socket.accept()
    data = connection.recv(1024).decode().split()
    #print(data)

    # Выдача токена пользователю
    if 'CREATE_LOBBY' in data:
        
        token = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(4))
        tokens.append(token)
        print(tokens)
        
        spy_amount.append(int(data[1]))
        players_amount.append(int(data[2]))
        
        token_role_locations = []
        token_role_locations.append(token)

        role = random.randint(0,1)
        if role == 1:
            token_role_locations.append('spy')
            spy_amount[-1] -= 1
        elif role == 0:
            token_role_locations.append('peaceful')
            players_amount[-1] -= 1

        
        token_role_locations.append(database)
        #connection.send(bytes(token, encoding='UTF-8'))
        connection.send(pickle.dumps(token_role_locations))
        
    
    # Подключение мазефакера к лобби и выдача ему роли
    elif "".join(data) in tokens: 
        data = "".join(data)
        # Находим конкретное лобби по указанному токену
        spy_amount_current = spy_amount[tokens.index(data)]
        players_amount_current = players_amount[tokens.index(data)]

        # Определяю роли
        role = random.randint(0,1)
        if role == 1 and spy_amount_current != 0:
            role_locations = []
            role_locations.append('spy')
            role_locations.append(database)
            print(role_locations)
            connection.send(pickle.dumps(role_locations))
            spy_amount_current -= 1
        elif role == 0 and players_amount != 0:
            role_locations = []
            role_locations.append('peaceful')
            role_locations.append(database)
            print(role_locations)
            connection.send(pickle.dumps(role_locations))
            players_amount_current -= 1
            
    # Закрываем сокет (бб мазафакер)
    connection.close()