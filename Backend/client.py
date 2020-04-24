import socket

address_to_server = ('localhost', 5050)

def createLobby(players_amount, spy_amount):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(address_to_server)
    client.send(bytes("CREATE_LOBBY {players_amount} {spy_amount}".format(players_amount = players_amount, spy_amount = spy_amount), encoding='UTF-8'))
    token = client.recv(1024).decode()
    return token[:5] 

def connect(token):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(address_to_server)
    client.send(bytes(token, encoding='UTF-8'))
    data = client.recv(1024).decode()
    if 'invalid token' in data:
        return 'invalid token'
    else:
        role = 'peaceful' if 'peaceful' in data else 'spy'
        return role
