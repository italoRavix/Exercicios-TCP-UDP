import sys
import argparse
import socket
import threading
from datetime import datetime

parser = argparse.ArgumentParser(prog = 'Cliente TCP', description='Um cliente TCP que se conecta no endereço IP e porta passados por linha de comando.')

parser.add_argument("address", help="Endereço IP onde o cliente irá se conectar", type=str)
parser.add_argument("port", help="Porta onde o endereço IP irá se conectar", type=int)
args = parser.parse_args()

''' cria o socket e o conecta a uma porta '''
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((args.address, args.port))

except ConnectionRefusedError:
    print(f'Servidor {args.address}:{args.port} indisponível.')
    sys.exit()

else:
    print(f'Cliente conectado em {args.address}:{args.port}')
    print('Use \'\\sair\' para encerrar a conexão.\n')

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

        answer = client.recv(1024)
        print(answer.decode())

    client.close()
    print('Conexão encerrada.')
