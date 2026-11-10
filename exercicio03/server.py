# Exercicio 03 - server
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

# lista que armazena os clientes
clients_list = []

# trava para impedir as threads de alterar partes criticas so programa ao mesmo tempo
lock = threading.Lock()

def manage_connection(conn, addr, conn_list):
    """ Gerencia as conexoes: recebe mensages do clientes, envia para todos os outros e encerra a conexão com esse cliente quado solicitado
    
    Parâmetros:
        conn: conexão
        addr: endereço do cliente
        conn_list: lista com todas as conexoes dos clientes conectados
    """
    message = conn.recv(1024)
    goodbye_message = f'Usuário {addr[0]}:{addr[1]} saiu do chat.' # mensagem que indica que o dono desta conexão da thread saiu do chat

    while message != b'\\sair\n' and message != b'\\sair':
        print(f'({datetime.now()}). Cliente {addr[0]}:{addr[1]} >> {message.decode()}')
        message = f'{addr[0]}:{addr[1]} >> ' + message.decode()

        # envia a mensagem para todos os usuarios, exceto a quem enviou
        with lock:
            for c in conn_list:
                if c[0] != conn:
                    c[0].sendall(message.encode())

        message = conn.recv(1024)

    # avisa a todos os outros usuários que um dado usuário saiu
    with lock:
        for c in conn_list:
            if c[0] != conn:
                c[0].sendall(goodbye_message.encode())

        # encerra a conexão e remove o dono desta conexão
        conn.close()
        conn_list.remove((conn, addr))

    print(f'Cliente {addr[0]}:{addr[1]} encerrou a conexão.')

# fluxo da thread principal: aceita conexões, adiciona os clinetes e threadas nas listas, e gerencia as chamadas às threads filhas
while True:
    try:
        conn, addr = server.accept()
    except KeyboardInterrupt:
        print('\nEncerrando conexões...')
        if len(threads_connections) > 0:
            print('Aguardando todos os clientes se desconectarem.')
        break
        
    print(f'Cliente {addr[0]}:{addr[1]} iniciou a conexão.')
    
    # adiciona os clientes na lista
    with lock:
        clients_list.append((conn, addr))

    welcome_message = f'Usuário {addr[0]}:{addr[1]} entrou no chat.'
    with lock:
        for c in clients_list:
            if c[0] != conn:
                c[0].sendall(welcome_message.encode())

    # cria as threads e adiciona na lista
    t = threading.Thread(target=manage_connection, args=(conn, addr, clients_list))
    threads_connections.append(t)
    t.start()

for t in threads_connections:
    t.join()

print('Todas as threads encerradas.')
server.close()

print('Servidor encerrado. Até mais!')
