# Exercicio 02 - client
# Italo Tadeu Pereira Almeida
# Hendryl Figueiredo Miranda
# João Victor Silva Soares

import sys
import argparse
import socket
import random

# limite maximo de uma mensagem
MAX_LIMIT = 65507

# limite máximo de tempo de espera (segundos)
MAX_TIME_LIMIT = 5

# limites do intervalo de portas onde o cliente pode criar um socket
MIN_LIMIT_PORT = 8000
MAX_LIMIT_PORT = 10000

# cria o socket udp e o usa para enviar mensagens para o servidor passado como argumento
parser = argparse.ArgumentParser(prog = 'Cliente UDP', description='Um cliente UDP que se conecta no endereço IP e porta passados por linha de comando.')
parser.add_argument("address", help="Endereço IP para onde o cliente irá enviar mensagens", type=str)
parser.add_argument("port", help="Porta onde o endereço IP irá se conectar", type=int)
args = parser.parse_args()

IP_ADDRESS_SERVER = args.address
PORT_SERVER = args.port

# cria o socket e o vincula a uma porta aleatoria
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(('127.0.0.1', random.randint(MIN_LIMIT_PORT, MAX_LIMIT_PORT)))
client.settimeout(MAX_TIME_LIMIT) # evita espera indefinida por repostas do servidor

print(f'Cliente conectado em {IP_ADDRESS_SERVER}:{PORT_SERVER}')
print('Use \'\\sair\' para encerrar o cliente.\n')

# fluxo principal que pega a entrada do usuário enquanto ele nao digitar o valor de sentinela, a envia ao servidor e captura a resposta
while True:
    try:
        message = input('sent >> ')

    except KeyboardInterrupt:
        print()
        break

    # valida o tamanho da mensagem
    if len(message) > MAX_LIMIT:
        print(f'Mensagem muito longa. Limite max {MAX_LIMIT}.')

    else:
        # validação para mensagens vazias
        if message == '':
            message =  ' '

        if message == '\\sair':
            print('Encerrando...')
            break

        message = message.encode()
        client.sendto(message, (IP_ADDRESS_SERVER, PORT_SERVER))

        try:
            answer = client.recv(1024)

        except TimeoutError:
            print('O servidor não respondeu. Ele está ativo?')

        except KeyboardInterrupt: # trata o caso do usuário tentar interromper durante a espera da reposta do servidor
            print()
            break

        else:
            print('echo >>', answer.decode())

client.close()
print('Cliente encerrado.')
