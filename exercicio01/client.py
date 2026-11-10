# Exercicio 01 - client
# Italo Tadeu Pereira Almeida
# Hendryl Figueiredo Miranda

import sys
import argparse
import socket

# define o argparser
parser = argparse.ArgumentParser(prog = 'Cliente TCP', description='Um cliente TCP que se conecta no endereço IP e porta passados por linha de comando.')
parser.add_argument("address", help="Endereço IP onde o cliente irá se conectar", type=str)
parser.add_argument("port", help="Porta onde o endereço IP irá se conectar", type=int)
args = parser.parse_args()

# cria o socket tcp e o conecta ao endpoint do servidor passado como argumento
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((args.address, args.port))

# encerra o programa se não houver endpoint no endereço passado como argumento    
except ConnectionRefusedError:
    print(f'Servidor {args.address}:{args.port} indisponível.')
    sys.exit()

print(f'Cliente conectado em {args.address}:{args.port}')
print('Use \'\\sair\' para encerrar a conexão.\n')

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

    answer = client.recv(1024)
    print(answer.decode())

client.close()
print('Conexão encerrada.')
