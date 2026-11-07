import argparse
import socket
import threading

parser = argparse.ArgumentParser(prog = 'Servidor UDP', description='Um servidor UDP que fica em escuta esperando conxeões de clientes na porta passada como argumento.')

parser.add_argument("port", help="Porta onde o socket de escuta será aberto", type=int)
args = parser.parse_args()

''' cria o socket udp para a escuta e o vincula a uma porta '''
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("127.0.0.1", args.port))
print(f'Socket aberto na porta {args.port}')
print('Digite Ctrl + C para encerrar o servidor')
print('Aguardando conexões...')

# threads_connections = []

def manage_connection(server):
    message, client_addr = server.recvfrom(1024)
    print(f'Cliente {client_addr[0]}:{client_addr[1]} >> {message.decode()}')
    server.sendto(message, client_addr)

while True:
    try:
        manage_connection(server)

    except KeyboardInterrupt:
        print()
        print('Encerrando servidor...')
        break

# por hora esse codigo nao eh alcancavel, mas ja esta pronto caso o loop acima deixe de ser infinito
#for t in  threads_connections:
#    t.join()

#print('Todas as threads encerradas.')
server.close()
print('Servidor encerrado. Até mais!')
