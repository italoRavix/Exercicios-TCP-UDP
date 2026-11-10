# Exercicio 03 - client
# Italo Tadeu Pereira Almeida
# Hendryl Figueiredo Miranda

import sys
import argparse
import socket
import threading

# valor de sentinela que para o recebimento de mensagens
STOP_RECEIVE = False

#define o argparse
parser = argparse.ArgumentParser(prog = 'Cliente TCP', description='Um cliente TCP que se conecta no endereço IP e porta passados por linha de comando e recebe mensagens de outros clientes.')
parser.add_argument("address", help="Endereço IP onde o cliente irá se conectar", type=str)
parser.add_argument("port", help="Porta onde o endereço IP irá se conectar", type=int)
args = parser.parse_args()

IP_ADDRESS_SERVER = args.address
PORT_SERVER = args.port

def receive_broadcast(conn):
    """ Gerencia a escuta das mensagens de outros clientes enviadas pelo servidor: escuta até receber o valor de sentinela para parar
    
    Parâmetros:
    conn: conexão
    """
    while True:
        if STOP_RECEIVE:
            return

        answer = conn.recv(1024)
        print(answer.decode())

# cria o socket tcp e o conecta ao endpoint do servidor passado como argumento
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((IP_ADDRESS_SERVER, PORT_SERVER))

# encerra o programa se não houver endpoint no endereço passado como argumento    
except ConnectionRefusedError:
    print(f'Servidor {IP_ADDRESS_SERVER}:{PORT_SERVER} indisponível.')
    sys.exit()

else:
    print(f'Cliente conectado em {IP_ADDRESS_SERVER}:{PORT_SERVER}')
    print('Use \'\\sair\' para encerrar a conexão.\n')

    # cria a thread de escuta
    t = threading.Thread(target=receive_broadcast, args=(client,))
    t.start()

    # fluxo principal que pega a entrada do usuário enquanto ele nao digitar o valor de sentinela e então o envia ao servidor
    while True:
        try:
            message = input()

        except KeyboardInterrupt:
            print()
            client.sendall(b'\\sair')
            break

        # validação para mensagens vazias
        if message == '':
            message =  ' '

        message = message.encode()
        client.sendall(message)
        if message == b'\\sair':
            print('Encerrando conexão...')
            break

    # atualiza o valor de sentinela e encerra a thread de escuta de forma segura
    STOP_RECEIVE = True
    t.join()
    
    # encerra o endpoint do cliente
    client.close()
    print('Conexão encerrada.')
