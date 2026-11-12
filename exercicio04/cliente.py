# Exercicio 04 - client
# Italo Tadeu Pereira Almeida
# Hendryl Figueiredo Miranda
# João Victor Silva Soares

import argparse
import socket

parser = argparse.ArgumentParser(
    prog='Cliente TCP',
    description='Cliente TCP que solicita a hora ao servidor.'
)

# define argparse
parser.add_argument("address", help="Endereço IP do servidor", type=str)
parser.add_argument("port", help="Porta do servidor", type=int)
args = parser.parse_args()

print(f'Cliente configurado para {args.address}:{args.port}')
print("Digite 'hora' para consultar ou '\\sair' para encerrar.\n")

# fluxo principal que pega a entrada do usuário, avalia e recebe a resposta do servidor
while True:
    try:
        message = input('sent >> ')

    except KeyboardInterrupt:
        print()
        break

    if message == '\\sair':
        print('Encerrando conexão...')
        break

    if message.lower() == 'hora':
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(5)

        try:
            client.connect((args.address, args.port))
            client.sendall('HORA'.encode())

            answer = client.recv(1024)
            print('Hora >>', answer.decode())

        except OSError:
            print('O servidor não respondeu. Ele está ativo?')

        finally:
            client.close()

    else:
        print('Comando inválido.')

print('Cliente encerrado.')
