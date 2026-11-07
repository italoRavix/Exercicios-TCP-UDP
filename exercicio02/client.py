import sys
import argparse
import socket
import random

# limite maximo de uma mensagem
MAX_LIMIT = 65507
parser = argparse.ArgumentParser(prog = 'Cliente UDP', description='Um cliente UDP que se conecta no endereço IP e porta passados por linha de comando.')

parser.add_argument("address", help="Endereço IP onde o cliente irá se conectar", type=str)
parser.add_argument("port", help="Porta onde o endereço IP irá se conectar", type=int)
args = parser.parse_args()

''' cria o socket e o vincula a uma porta'''
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(('127.0.0.1', random.randint(8000, 10000)))
client.settimeout(5)

print(f'Cliente conectado em {args.address}:{args.port}')
print('Use \'\\sair\' para encerrar a conexão.\n')

while True:
    try:
        message = input('sent >> ')

    except KeyboardInterrupt:
        print()
        break

    if len(message) > MAX_LIMIT:
        print(f'Mensagem muito longa. Limite max {MAX_LIMIT}.')

    else:
        # validação para mensagens vazias
        if message == '':
            message =  ' '

        if message == '\\sair':
            print('Encerrando conexão...')
            break

        message = message.encode()
        client.sendto(message, (args.address, args.port))

        try:
            answer = client.recv(1024)

        except TimeoutError:
            print('O servidor não respondeu. Ele está ativo?')

        except KeyboardInterrupt:
            print()
            break

        else:
            print('echo >>', answer.decode())

client.close()
print('Cliente encerrado.')
