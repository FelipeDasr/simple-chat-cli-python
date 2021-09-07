import threading
import socket
import os


def main():

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    logo()
    username = input('Usuário: ')

    # Tenta se conectar ao servidor
    try:
        client.connect(('localhost', 7777))
    except:
        return print('\nErro ao tentar se conectar ao servidor')

    # Recebe uma resposta do servidor sobre o nome de usuário
    client.send(username.encode('utf-8'))
    response = client.recv(1048)
    response = response.decode('utf-8')

    if(response == 'Nome de usuário indisponível'):
        print(f'\n{response}\n')
        return client.close()
    print('\n'+response)

    # Cria threads para receber e enviar mensagens
    thread1 = threading.Thread(target=receiveMessages, args=(client,))
    thread2 = threading.Thread(target=sendMessages, args=[client, username])

    thread1.start()
    thread2.start()


def receiveMessages(client):
    # Recebe as mensagens
    while True:
        msg = client.recv(2048).decode('utf-8')
        print(msg+'\n')


def sendMessages(client, username):
    logo()
    # Pega a mensagem e envia
    while True:
        msg = input('\n').encode('utf-8')
        client.send(msg)


def logo():
    os.system('cls') 
    print(25*'=', 'SOCKET CHAT', 25*'=')

# inicia o programa
main()
