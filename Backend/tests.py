import pytest
import client

# Здесь будут представлены юнит-тесты проверки работоспособности клиента

database = ['Bank', 'Hospital', 'Military unit', 'Casino',
            'Hollywood', 'Titanic', 'The Death Star', 'Hotel',
            'Russian Railways', 'Malibu Beach', 'Police Station',
            'Restaurant', 'University', 'Lyceum', 'SPA', 'Plane']

def test_createLobby():
    data = client.createLobby(5,2)
    assert len(data[0]) == 4
    assert data[1] in ['spy', 'peaceful']
    assert data[2] in database
    assert data[3] == database

def test_checkLocation():
    data = client.createLobby(5,2)
    checker = client.checkLocation(data[0], data[2])
    assert checker == 'true'

def test_checkGameStatus():
    data = client.createLobby(5,2)
    client.checkLocation(data[0], data[2])
    checker = client.checkGameStatus(data[0])
    assert checker == 'false'

def test_isCorrectToken():
    data = client.createLobby(5,2)
    checker = client.connect('I drunk AF')
    assert checker == 'invalid token'
