# Exercícios de Redes: TCP, UDP e outros protocolos

## Integrantes

- Italo Tadeu Pereira Almeida
- Hendryl Figueiredo Miranda
- João Victor Silva Soares

## Sobre o projeto

Este repositório reúne atividades práticas sobre redes de computadores. Os primeiros exercícios usam programas em Python para demonstrar a comunicação entre cliente e servidor. Os demais analisam capturas de rede feitas com o Wireshark.

O objetivo é entender, com exemplos, como os dispositivos trocam mensagens e como alguns protocolos funcionam.

## Exercícios

| Pasta | Atividade |
| --- | --- |
| [exercicio01](./exercicio01/README.md) | Servidor TCP que confirma o recebimento de mensagens |
| [exercicio02](./exercicio02/README.md) | Servidor UDP que devolve as mensagens recebidas |
| [exercicio03](./exercicio03/README.md) | Chat TCP que envia mensagens aos outros clientes conectados |
| [exercicio04](./exercicio04/README.md) | Cliente e servidor TCP para consultar a hora |
| [exercicio05](./exercicio05/README.md) | Análise de uma requisição e resposta HTTP |
| [exercicio06](./exercicio06/README.md) | Análise da abertura e do encerramento de uma conexão TCP |
| [exercicio07](./exercicio07/README.md) | Análise de consultas e respostas DNS |
| [exercicio08](./exercicio08/README.md) | Análise de mensagens ICMP e do tempo de resposta do ping |
| [exercicio09](./exercicio09/README.md) | Análise da troca de mensagens DHCP |

Cada pasta tem seu próprio README com os passos, os arquivos e as observações daquela atividade. As pastas de análise também incluem capturas de rede e imagens usadas como evidência.

## Requisitos

- Python 3.10 ou superior para executar os exercícios de 1 a 4.
- Wireshark para abrir e analisar as capturas dos exercícios de 5 a 9.
- Para repetir algumas capturas, também podem ser necessários um navegador, `telnet`, `ping` ou um cliente DHCP, conforme indicado no README do exercício.

Os programas dos exercícios de 1 a 4 usam recursos que já vêm com o Python; não é necessário instalar bibliotecas Python adicionais.

Para conferir a versão do Python instalada:

```bash
python3 --version
```

## Executar os programas

Os exercícios de 1 a 4 funcionam no terminal. Em geral, abra dois terminais na pasta do exercício: inicie o servidor em um e depois execute o cliente no outro. O endereço e a porta informados ao cliente devem corresponder aos usados pelo servidor.

Por exemplo, para iniciar o servidor TCP do exercício 1 na porta `5000`:

```bash
cd exercicio01
python3 server.py 5000
```

Em outro terminal, na mesma pasta, inicie o cliente:

```bash
python3 client.py 127.0.0.1 5000
```

O endereço `127.0.0.1` serve para testar cliente e servidor no mesmo computador. Consulte o README de cada exercício para ver os comandos e as opções específicas. Alguns servidores aceitam a opção `-n` ou `--network` para receber conexões por outras interfaces; use-a somente quando precisar e em uma rede confiável.

## Analisar as capturas

Os arquivos `.pcapng` devem ser abertos no Wireshark. As imagens nas pastas mostram os pacotes e campos destacados em cada atividade. Os filtros e os passos para reproduzir as capturas estão descritos nos READMEs correspondentes.
