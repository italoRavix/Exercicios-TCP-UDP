# Exercício - Servidor Echo UDP

## Integrantes

- Italo Tadeu Pereira Almeida
- Hendryl Figueiredo Miranda
- João Victor Silva Soares

## Descrição

Neste exercício foi criado um servidor UDP que recebe mensagens dos clientes o as envia de volta.

## Arquivos

- `server.py` - Código do servidor
- `client.py` - Código do cliente
- `README.md` - Instruções de execução

## Dependências

Para executar é necessário ter o Python 3 instalado.

Para verificar se já está instalado:

```bash
python3 --version
```

Caso não esteja, no GNU/Linux Debian 13:

```bash
sudo apt update
sudo apt install python3
```

Não é necessário instalar outras bibliotecas, pois todas já fazem parte do Python.

## Como executar

**1. Iniciar o servidor**

Abra o terminal na pasta do exercício e execute:

```bash
python3 server <-n | --network> <porta>
```

O servidor vai ficar aberto esperando os clientes se conectarem.
A opção network faz o servidor ficar escutando em todas as interfaces de rede. Por padrão ele só escuta em 127.0.0.1

**2. Iniciar o cliente**

Abra outro terminal na mesma pasta e execute:

```bash
python3 client.py <ip do servidor> <porta do servidor>
```

**3. Enviar mensagens**

No terminal do cliente, digite a mensagem e pressione Enter.

Exemplo:

```text
user@myhost$ oi
```

A mensagem será enviada de volta para aquele cliente

**4. Testar com vários clientes**

Para testar mais de um cliente, abra outro terminais e execute o mesmo comando:

```bash
python3 client.py <ip do servidor> <porta do servidor>
```

No terminal do servidor será mostrado o horário enviado, o ip e a porta do cliente de origem, além da mensagem enviada.

Uma mensagem irá ser exibida se o tempo limite para recebimento de uma mensagem for exibido

**5. Encerrar os programas**

- Para fechar o cliente, digite `\sair`
- Para fechar o servidor, pressione `Ctrl + C`

## Funcionamento

O servidor fica esperando dataagramas na porta especificada. Quando um cliente envia um datagrma, ele a envia de volta.

O cliente envia uma mensagem e o servidor usa o `datetime` para pegar o horário, `socket` para pegar o ip e a porta do cliente e assim gera seu log. Ainda usando socket ele encaminha a mensagem de volta para o usuário.
