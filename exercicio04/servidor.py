# Exercicio 04 - server
# Italo Tadeu Pereira Almeida
# Hendryl Figueiredo Miranda
# João Victor Silva Soares

import argparse
import socket
import threading
from datetime import datetime

#define o argparser
parser = argparse.ArgumentParser(prog='Servidor TCP', description='Servidor TCP que retorna a hora atual para os clientes.')
parser.add_argument("port", help="Porta do servidor", type=int)
args = parser.parse_args()

total_clientes = 0
lock = threading.Lock()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("127.0.0.1", args.port))
server.listen()

print(f'Socket aberto na porta {args.port}')
print('Digite Ctrl + C para encerrar o servidor')
print('Aguardando conexões...')

def manage_connection(connection, client_addr):
    global total_clientes

    try:
        message = connection.recv(1024).decode()

        if message == 'HORA':
            hora = datetime.now().strftime('%H:%M:%S')
            connection.sendall(hora.encode())

            # lock evita que as threads alterem o contador juntas
            with lock:
                total_clientes += 1
                print(f'Cliente {client_addr[0]}:{client_addr[1]} | Hora: {hora} | Total: {total_clientes}')

    except OSError as erro:
        with lock:
            print(f'Erro: {erro} | Total: {total_clientes}')

    finally:
        connection.close()

# fluxo principal: da a cada usuario uma thread 
while True:
    try:
        connection, client_addr = server.accept()

        # cada cliente recebe uma thread
        t = threading.Thread(
            target=manage_connection,
            args=(connection, client_addr),
            daemon=True
        )
        t.start()

    except KeyboardInterrupt:
        print()
        print('Encerrando servidor...')
        break

server.close()
print('Servidor encerrado.')
