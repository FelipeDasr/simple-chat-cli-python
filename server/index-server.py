import threading
import socket

clients = []


def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Cooloca o servidor online
    server.bind(('localhost', 7777))
    server.listen()

    # Fica escutando conexões
    while True:
        clientSock, addr = server.accept()

        username = clientSock.recv(1024)
        username = username.decode('utf-8')

        clientObj = {
            "username": username,
            "sock": clientSock
        }

        # Verifica se o nome de usuário está disponível
        if (not usernameIsValid(username)):
            print('Fechando conexão')
            clientSock.send('Nome de usuário indisponível'.encode('utf-8'))
            clientSock.close()

        else:
            # Adiciona na lista de clientes
            clients.append(clientObj)

            # Confirma ao usuário que ele está conectado
            clientSock.send('Connectado'.encode('utf-8'))
            # Log do servidor
            print(clientObj["username"], 'is Connected')

            # Cria um thread para o usuário poder enviar mensagens
            thread = threading.Thread(target=messageTreatment, args=[clientObj])
            thread.start()


def usernameIsValid(username):
    for client in clients:
        if username == client["username"]:
            return False
    return True


def messageTreatment(clientObj):

    username = clientObj["username"]
    client = clientObj["sock"]

    # Recebe as mensagens enviadas pelo cliente e as envia para todos os outros clientes
    while True:
        try:
            msg = client.recv(2048)
            msg = msg.decode('utf-8')
            broadcast(msg, username)

        except:
            # Deleta o usuário, caso ele não estaja disponível
            deleteClient(clientObj)
            break


def broadcast(msg, username):
    # Envia para todos os clientes a mensagem, menos para quem a enviou
    for client in clients:
        if client["username"] != username:
            try:
                client["sock"].send(f'{username} -> {msg}'.encode('utf-8'))
            except:
                deleteClient(client)


def deleteClient(clientObj):
    clients.remove(clientObj)
    msg = f'{clientObj["username"]} foi desconectado!\n'
    broadcast('\n'+msg, 'Sistema')

    # Log do servidor
    print(msg)


# Inicia
main()
