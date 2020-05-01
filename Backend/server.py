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
key_locations = []
game_statuses = []

database = ['Bank', 'Hospital', 'Military unit', 'Casino',
            'Hollywood', 'Titanic', 'The Death Star', 'Hotel',
            'Russian Railways', 'Malibu Beach', 'Police Station',
            'Restaurant', 'University', 'Lyceum', 'SPA', 'Plane']

def createLobby():
    # Генерируем токен и загадываем локацию
    token = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(4))
    key_location = database[random.randint(0,15)]
    token_role_keyLocation_locations = []
    
    # Добавляем токен, статус игры, загаданную локацию, число шпионов и игроков в соответствующие массивы
    tokens.append(token)
    game_statuses.append('true')
    key_locations.append(key_location + ' ' + token)
    spy_amount.append(int(data[1]))
    players_amount.append(int(data[2]))
    token_role_keyLocation_locations.append(token)

    # Генерируем роль
    role = random.randint(0,1)
    if role == 1:
        token_role_keyLocation_locations.append('spy')
        spy_amount[-1] -= 1
    elif role == 0:
        token_role_keyLocation_locations.append('peaceful')
        players_amount[-1] -= 1

    # Создаем посылку с токеном, ролью, загаданными и оставшимися локациями
    token_role_keyLocation_locations.append(key_location)
    token_role_keyLocation_locations.append(database)
    # Сериализуем объект и отправляем его клиенту
    connection.send(pickle.dumps(token_role_keyLocation_locations))

def connectToLobby(data):
    data = ''.join(data)
    # Находим конкретное лобби по указанному токену
    spy_amount_current = spy_amount[tokens.index(data)]
    players_amount_current = players_amount[tokens.index(data)]
    key_location_current = key_locations[tokens.index(data)].split()[0]

    # Генерируем роль мазефакеру и добавляю его в посылку
    role = random.randint(0,1)
    role_keyLocation_locations = []
    if role == 1 and spy_amount_current != 0:
        role_keyLocation_locations.append('spy')
        spy_amount_current -= 1
    elif role == 0 and players_amount != 0:
        role_keyLocation_locations.append('peaceful')
        players_amount_current -= 1
    
    # Добавляем загаданную и оставшиеся локации в посылку
    role_keyLocation_locations.append(key_location_current)
    role_keyLocation_locations.append(database)
    # Отправляем посылку клиенту в двоичном формате
    connection.send(pickle.dumps(role_keyLocation_locations))

def isCorrectLocation(data):
    if data[1] in tokens:
        game_statuses[tokens.index(data[1])] = 'false'
    if data[1] in tokens and ''.join(data[0] + ' ' + data[1]) in key_locations and tokens.index(data[1]) == key_locations.index(''.join(data[0] + ' ' + data[1])):
        connection.send(bytes('true', encoding='UTF-8'))
    else:
        connection.send(bytes('false', encoding='UTF-8'))

def checkGameStatuse(data):
    connection.send(bytes(game_statuses[tokens.index(data[1])], encoding='UTF-8'))

# Слушаем запросы
while True:

    connection, address = server_socket.accept()
    data = connection.recv(1024).decode().split('_')

    # Выдача токена пользователю
    if 'createLobby' in data:
        createLobby()

    # Подключение мазефакера к лобби и выдача ему роли
    elif ''.join(data) in tokens:
        connectToLobby(data) 

    # Проверка шпионом выбранной локации
    elif data[0] in database:
        isCorrectLocation(data)
    
    # Проверка статуса игры
    elif data[0] == 'knock-knock':
        checkGameStatuse(data)

    # Проверка на корректность токена
    elif ''.join(data) not in tokens:
        connection.send(pickle.dumps('invalid token'))
        
    # Закрываем сокет (бб мазафакер)
    connection.close()
