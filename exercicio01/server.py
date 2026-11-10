# Exercicio 01 - server
# Italo Tadeu Pereira Almeida
# Hendryl Figueiredo Miranda

import argparse
import socket
import threading
from datetime import datetime

# define o argparser
parser = argparse.ArgumentParser(prog = 'Servidor TCP', description='Um servidor TCP que fica em escuta esperando conxões de clientes na porta passada ou 567676 por padrão.')
parser.add_argument('port', help='Porta onde o socket de escuta será aberto', type=int)
parser.add_argument('--network', '-n', help='Define se o socket de escuta será aberto para toda as redes locais. Opcional, usa localhost como default.', action='store_true')
args = parser.parse_args()

IP_ADDRESS = '127.0.0.1'
PORT = args.port
if args.network:
    IP_ADDRESS = '0.0.0.0'
    
# cria o socket tcp para a escuta e o vincula a uma porta
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP_ADDRESS, PORT))
server.listen()
print(f'Socket aberto na porta {PORT}')
print('Digite Ctrl + C para encerrar o servidor')
print('Aguardando conexões...')

# lista que armazena as threads com as conexões
threads_connections = []

def manage_connection(conn, addr):
    """ Gerencia as conexoes: recebe mensagens do cliente, envia uma confirmações e fecha a conexão do lado do servidor
    
    Parâmetros:
        conn: conexão
        addr: endereço do cliente
    """
    message = conn.recv(1024)

    while message != b'\\sair\n' and message != b'\\sair':
        print(f'({datetime.now()}). Cliente {addr[0]}:{addr[1]} >> {message.decode()}')
        confirmed = f'Mensagem recebida. {datetime.now()}.'
        confirmed = confirmed.encode()
        conn.sendall(confirmed)
        message = conn.recv(1024)

    conn.close()
    print(f'Cliente {addr[0]}:{addr[1]} encerrou a conexão.')

# fluxo da thread principal
while True:
    try:
        conn, addr = server.accept()
    except KeyboardInterrupt:
        print('\nEncerrando conexões...')
        if len(threads_connections) > 0: # verifica se todos os clientes se conectaram antes de encerrar o servidor
            print('Aguardando todos os clientes se desconectarem.')
        break

    print(f'Cliente {addr[0]}:{addr[1]} iniciou a conexão.')
    
    # cria as threads e as adiciona a lista
    t = threading.Thread(target=manage_connection, args=(conn, addr))
    threads_connections.append(t)
    t.start()

# pede a thread principal que espere o encerramento seguro de cada thread filha
for t in  threads_connections:
    t.join()

print('Todas as threads encerradas.')
server.close()
print('Servidor encerrado. Até mais!')
