[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/SmCo-Bsf)

## ▶️ Vídeo do projeto

Vídeo:

 [![Assista ao vídeo](https://img.youtube.com/vi/EY7vk2tB9ho/0.jpg)](https://www.youtube.com/watch?v=EY7vk2tB9ho)


</br>

Link do vídeo: [![Vídeo](https://img.shields.io/badge/-Vídeo-red)](https://youtu.be/EY7vk2tB9ho)



## ⚙️ Instruções de Execução

Para rodar o código, siga estas instruções:

### Servidor Central

1. Defina o endereço IP e a porta no arquivo:
   
   `central/configuracao_server_central.json`

2. No diretório `central`, execute o servidor central usando um dos seguintes comandos:

    ⚠️ Dependendo do sistema execute utilizando "python3"

   ```bash
   python servidorCentral.py configuracao_server_central.json
   ```

### Servidores Distribuídos

1. Configure o endereço IP e a porta do servidor central nos arquivos:

   - `distributed/configuracao_terreo.json`
   - `distributed/configuracao_andar_1.json`
   - `distributed/configuracao_andar_2.json`

2. No diretório `distributed`, execute os servidores distribuídos para cada andar usando os seguintes comandos:
    
    ⚠️ Dependendo do sistema execute utilizando "python3"

   **Andar Térreo:**

   ```bash
   python servidorDistribuido.py configuracao_terreo.json
   ```

   **Andar 1:**

   ```bash
   python servidorDistribuido.py configuracao_andar_1.json
   ```

   **Andar 2:**

   ```bash
   python servidorDistribuido.py configuracao_andar_2.json
   ```





# 🔨 Funcionalidades do Projeto

- `Servidor Central`: Mantém conexão com os servidores distribuídos (TCP/IP) e provê uma interface de usuário com as seguintes funcionalidades:
  - `Interface de Monitoramento`: Apresenta os seguintes dados:
    - Número de carros em cada andar.
    - Número total de carros no estacionamento.
    - Número de vagas disponíveis em cada andar por tipo (regular, deficiente ou idoso).
    - Valor total pago, calculado proporcionalmente aos minutos estacionados (taxa de R$0,10 por minuto).
  - `Interface de Comandos`: Permite:
    - Fechar o estacionamento manualmente, ativando ou desativando o sinal de lotado.
    - Bloquear o 1º e/ou 2º Andar, sinalizando o impedimento ao 2º Andar mesmo sem estar com todas as vagas ocupadas.
    
- `Servidores Distribuídos`: Cada servidor distribuído é responsável por um andar do estacionamento e tem as seguintes funcionalidades:
  - `Monitoramento das Vagas`: Detecta a ocupação de vagas individualmente e envia mudanças de estado ao servidor central.
  - `Controle das Cancelas`: Controla as cancelas de entrada e saída, abrindo e fechando de acordo com a presença de carros, caso servidor distribuido esteja configurado como Térreo.
  - `Sensor de Passagem de Carros`: Detecta a passagem de carros entre os andares, identificando a direção, caso esteja configurado como Andar 1 ou Andar 2


## ✔️ Técnicas e tecnologias utilizadas:

- **Python 3**: Linguagem de programação principal usada para desenvolver ambos os códigos.
  
- **RPi.GPIO**: Biblioteca Python usada para interagir com os pinos GPIO (General Purpose Input/Output) no Raspberry Pi.

- **Threading**: Técnica utilizada para lidar com múltiplas tarefas de forma concorrente, permitindo a execução de operações simultâneas em diferentes partes do código.

- **Socket Programming**: Utilizado para comunicação em rede, permitindo que os dispositivos se comuniquem uns com os outros por meio de conexões de socket.

- **JSON (JavaScript Object Notation)**: Utilizado para armazenar e transmitir dados estruturados entre diferentes partes do sistema, como configurações de pinos, mensagens entre servidores, etc.

- **Signal Handling (Tratamento de Sinais)**: Utilizado para capturar e lidar com sinais específicos do sistema, como o sinal `SIGINT`, gerado quando o usuário pressiona `Ctrl+C`.

- **Visual Studio Code**: Ambiente de desenvolvimento integrado (IDE) usado para escrever, depurar e executar o código Python. 


# 👥  Autores

| [<img loading="lazy" src="https://avatars.githubusercontent.com/u/54285732?v=4" width=115><br><sub>Hugo Rocha de Moura</sub>](https://github.com/hugorochaffs) |  [<img loading="lazy" src="https://avatars.githubusercontent.com/u/48574832?v=4" width=115><br><sub>Samuel Nogueira Bacelar</sub>](https://github.com/SamuelNoB) | |
| :---: | :---: | :---: |



## 🔖 Referências


#### Python 3
Python 3 é a linguagem de programação principal usada para desenvolver ambos os códigos.

- [Documentação Python 3 ](https://docs.python.org/3/)



#### RPi.GPIO
RPi.GPIO é uma biblioteca Python usada para interagir com os pinos GPIO (General Purpose Input/Output) no Raspberry Pi.

- [Documentação RPi.GPIO](https://sourceforge.net/p/raspberry-gpio-python/wiki/Examples/)

#### Threading
Threading é uma técnica utilizada para lidar com múltiplas tarefas de forma concorrente, permitindo a execução de operações simultâneas em diferentes partes do código.

- [Documentação Threading em Python](https://docs.python.org/3/library/threading.html)

#### Socket Programming
Socket Programming é utilizado para comunicação em rede, permitindo que os dispositivos se comuniquem uns com os outros por meio de conexões de socket.

- [Documentação Socket Programming em Python](https://docs.python.org/3/library/socket.html)

#### JSON (JavaScript Object Notation)
JSON (JavaScript Object Notation) é utilizado para armazenar e transmitir dados estruturados entre diferentes partes do sistema, como configurações de pinos, mensagens entre servidores, etc.

- [Documentação JSON em Python](https://docs.python.org/3/library/json.html)

#### Signal Handling (Tratamento de Sinais)
Signal Handling é utilizado para capturar e lidar com sinais específicos do sistema, como o sinal SIGINT, gerado quando o usuário pressiona Ctrl+C.

- [Documentação Signal Handling em Python](https://docs.python.org/3/library/signal.html)

#### Visual Studio Code
Visual Studio Code é um ambiente de desenvolvimento integrado (IDE) usado para escrever, depurar e executar o código Python.

- [Documentação do Visual Studio Code](https://code.visualstudio.com/docs)

