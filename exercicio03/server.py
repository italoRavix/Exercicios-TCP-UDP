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
conn_list = []

# trava para impedir as threads de alterar partes criticas so programa ao mesmo tempo
lock = threading.Lock()

def send_broadcast(conn, conn_list, message):
    """ Envia uma mensagem para todos os usuários conectados com exceçao de quem a enviou 

       Parâmetros: 
       conn: conexão que enviou a mensagem
       conn_list: lista de todas as conexões
       message: mensagem a ser transmitida
    """
    with lock:
        for c in conn_list:
            if c != conn:
                c.sendall(message.encode())

def manage_connection(conn, ip, port, conn_list):
    """ Gerencia as conexoes: recebe mensages do clientes, envia para todos os outros e encerra a conexão com esse cliente quado solicitado
    
    Parâmetros:
        conn: conexão
        addr: endereço do cliente
        conn_list: lista com todas as conexoes dos clientes conectados
    """
    message = conn.recv(1024)
    goodbye_message = f'Usuário {ip}:{port} saiu do chat.' # mensagem que indica que o dono desta conexão da thread saiu do chat

    while message != b'\\sair\n' and message != b'\\sair':
        print(f'({datetime.now()}). Cliente {ip}:{port} >> {message.decode()}')
        message = f'{ip}:{port} >> ' + message.decode()

        send_broadcast(conn, conn_list, message)        
        message = conn.recv(1024)

    # avisa a todos os outros usuários que um dado usuário saiu
    send_broadcast(conn, conn_list, goodbye_message)            

        # encerra a conexão e remove o dono desta conexão
    with lock:
        conn.close()
        conn_list.remove(conn)

    print(f'Cliente {ip}:{port} encerrou a conexão.')

# fluxo da thread principal: aceita conexões, adiciona os clinetes e threadas nas listas, e gerencia as chamadas às threads filhas
while True:
    try:
        conn, addr = server.accept()
    except KeyboardInterrupt:
        print('\nEncerrando conexões...')
        if len(threads_connections) > 0:
            print('Aguardando todos os clientes se desconectarem.')
        break
    
    IP_ADDRESS_CLIENT, PORT_CLIENT = addr
    print(f'Cliente {IP_ADDRESS_CLIENT}:{PORT_CLIENT} iniciou a conexão.')
    
    # adiciona os clientes na lista
    with lock:
        conn_list.append(conn)

    welcome_message = f'Usuário {IP_ADDRESS_CLIENT}:{PORT_CLIENT} entrou no chat.'
    send_broadcast(conn, conn_list, welcome_message)            

    # cria as threads e adiciona na lista
    t = threading.Thread(target=manage_connection, args=(conn, IP_ADDRESS_CLIENT, PORT_CLIENT, conn_list))
    threads_connections.append(t)
    t.start()

for t in threads_connections:
    t.join()

print('Todas as threads encerradas.')
server.close()

print('Servidor encerrado. Até mais!')
