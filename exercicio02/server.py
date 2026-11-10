# Exercicio 01 - server
# Italo Tadeu Pereira Almeida
# Hendryl Figueiredo Miranda

import argparse
import socket
import threading

parser = argparse.ArgumentParser(prog = 'Servidor UDP', description='Um servidor UDP que fica em escuta esperando conexões de clientes na porta passada como argumento.')

parser.add_argument("port", help="Porta onde o socket de escuta será aberto", type=int)
parser.add_argument('--network', '-n', help='Define se o socket de escuta será aberto para toda as redes locais. Opcional, usa localhost como default.', action='store_true')
args = parser.parse_args()

IP_ADDRESS = '127.0.0.1'
PORT = args.port
if args.network:
    IP_ADDRESS = '0.0.0.0'

# cria o socket udp para a escuta e o vincula a uma porta
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((IP_ADDRESS, PORT))
print(f'Socket aberto na porta {PORT}')
print('Digite Ctrl + C para encerrar o servidor')
print('Aguardando conexões...')

def manage_connection(server):
    """ Gerencia as conexoes: recebe mensagens do cliente e as envia de volta
    
    Parâmetros:
        server: endpoint do servidor
    """
    message, client_addr = server.recvfrom(1024)
    print(f'Cliente {client_addr[0]}:{client_addr[1]} >> {message.decode()}')
    server.sendto(message, client_addr)

# fluxo principal
while True:
    try:
        manage_connection(server)

    except KeyboardInterrupt:
        print()
        print('Encerrando servidor...')
        break

server.close()
print('Servidor encerrado. Até mais!')
