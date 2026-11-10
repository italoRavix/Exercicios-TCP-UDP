import argparse
import socket
import threading
from datetime import datetime

parser = argparse.ArgumentParser(prog = 'Servidor TCP', description='Um servidor TCP que fica em escuta esperando conxões de clientes na porta passada ou 567676 por padrão.')

parser.add_argument("port", help="Porta onde o socket de escuta será aberto", type=int)
args = parser.parse_args()

''' cria o socket tcp para a escuta e o vincula a uma porta '''
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", args.port))
server.listen()
print(f'Socket aberto na porta {args.port}')
print('Digite Ctrl + C para encerrar o servidor')
print('Aguardando conexões...')

threads_connections = []
clients_list = []
lock = threading.Lock()

def manage_connection(conn, addr, conn_list):
    message = conn.recv(1024)
    #with lock:
        #for c in conn_list:
            #c[0].sendall(welcome_message.encode())

    while message != b'\\sair\n' and message != b'\\sair':
        print(f'({datetime.now()}). Cliente {addr[0]}:{addr[1]} >> {message.decode()}')
        message = f'{addr[0]}:{addr[1]} >> ' + message.decode()
        message = message.encode()

        with lock:
            for c in conn_list:
                if c[0] != conn:
                    c[0].sendall(message)

        message = conn.recv(1024)

    with lock:
        goodbye_message = f'Usuário {addr[0]}:{addr[1]} saiu do chat.'

        for c in conn_list:
            if c[0] != conn:
                c[0].sendall(goodbye_message.encode())

        conn.close()
        conn_list.remove((conn, addr))

    print(f'Cliente {addr[0]}:{addr[1]} encerrou a conexão.')

while True:
    try:
        conn, addr = server.accept()
    except KeyboardInterrupt:
        print('\nEncerrando conexões...')
        if len(threads_connections) > 0:
            print('Aguardando todos os clientes se desconectarem.')
        break

    print(f'Cliente {addr[0]}:{addr[1]} iniciou a conexão.')
    clients_list.append((conn, addr))

    with lock:
        for c in clients_list:
            welcome_message = f'Usuário {addr[0]}:{addr[1]} entrou no chat.'
            if c[0] != conn:
                c[0].sendall(welcome_message.encode())

    t = threading.Thread(target=manage_connection, args=(conn, addr, clients_list))
    with lock:
        threads_connections.append(t)
    t.start()

# por hora esse codigo nao eh alcancavel, mas ja esta pronto caso o loop acima deixe de ser infinito
for t in threads_connections:
    t.join()

print('Todas as threads encerradas.')
server.close()

print('Servidor encerrado. Até mais!')
