# Exercício 4 - Servidor de Hora com Threads (UDP)

## Descrição

Neste exercício foi criado um servidor UDP que recebe pedidos dos clientes e envia a hora atual.

O servidor usa threads para atender vários clientes ao mesmo tempo e um Lock para controlar a contagem de atendimentos.

## Arquivos

- `servidor.py` - Código do servidor
- `cliente.py` - Código do cliente
- `README.md` - Instruções de execução

## Dependências

Para executar é necessário ter o Python 3 instalado.

Para verificar se já está instalado:

```bash
python3 --version
```

Caso não esteja, no Linux Mint:

```bash
sudo apt update
sudo apt install python3
```

Não é necessário instalar outras bibliotecas, pois todas já fazem parte do Python.

## Como executar

**1. Iniciar o servidor**

Abra o terminal na pasta do exercício e execute:

```bash
python3 servidor.py 7000
```

O servidor vai ficar aberto esperando os clientes se conectarem.

**2. Iniciar o cliente**

Abra outro terminal na mesma pasta e execute:

```bash
python3 cliente.py 127.0.0.1 7000
```

O endereço `127.0.0.1` é o IP do próprio computador e `7000` é a porta usada pelo servidor.

**3. Solicitar a hora**

No terminal do cliente, digite `hora` e pressione Enter.

Exemplo:

```text
sent >> hora
Hora >> 13:36:25
```

É possível pedir a hora outras vezes sem precisar fechar o programa.

**4. Testar com vários clientes**

Para testar mais de um cliente, abra outros terminais e execute o mesmo comando:

```bash
python3 cliente.py 127.0.0.1 7000
```

No terminal do servidor será mostrado o horário enviado e a quantidade total de atendimentos realizados.

**5. Encerrar os programas**

- Para fechar o cliente, digite `\sair`
- Para fechar o servidor, pressione `Ctrl + C`

## Funcionamento

O servidor fica esperando conexões na porta 7000. Quando um cliente se conecta, ele cria uma thread para atender aquele pedido.

O cliente envia a mensagem `HORA` e o servidor usa o `datetime` para pegar o horário atual e devolver no formato `HH:MM:SS`.

A cada pedido atendido, o contador aumenta. O `Lock` serve para evitar problemas quando mais de uma thread tenta alterar o contador ao mesmo tempo.

Depois de enviar a hora, a conexão com aquele cliente é fechada, mas o servidor continua funcionando para receber novos pedidos.
