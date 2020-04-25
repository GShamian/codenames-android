import socket
import pickle

address_to_server = ('localhost', 5050)

def createLobby(players_amount, spy_amount):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(address_to_server)
    client.send(bytes("CREATE_LOBBY {players_amount} {spy_amount}".format(players_amount = players_amount, spy_amount = spy_amount), encoding='UTF-8'))
    data = pickle.loads(client.recv(1024))
    return (data[0], data[1], data[2:]) 

def connect(token):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(address_to_server)
    client.send(bytes(token, encoding='UTF-8'))
    data = pickle.loads(client.recv(1024))
    return (data[0], data[1])

def checkLocation(role, location):
    if role == 'spy':
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(address_to_server)
        client.send(bytes(location, encoding='UTF-8'))
        # Получаем ответ от сервера является ли эта локация верной
        response = client.recv(1024).decode()
        return response
    elif role == 'peaceful':
        return 'invalid role'



token = createLobby(5,2)
print(token)
print(connect(token[0]))
