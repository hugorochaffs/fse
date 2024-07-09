################################################################################
#                                                                              #
#                       CONTROLE DE ESTACIONAMENTOS                            #
#                              SERVIDOR CENTRAL                                #
#                           TRABALHO 1 - FSE - 2024.1                          #
#                          Hugo Rocha e Samuel Bacelar                         #
#                                                                              #
################################################################################

# Importacao de bibliotecas 
import sys
import signal
import threading
import socket
import json
import uuid
from datetime import datetime
import time



# Dicionário que armazena o estado inicial das vagas por andar
vagas = {'AT': {'T1': 0, 'T2': 0, 'T3': 0, 'T4': 0, 'T5': 0, 'T6': 0, 'T7': 0, 'T8': 0},
         'A1': {'A1': 0, 'A2': 0, 'A3': 0, 'A4': 0, 'A5': 0, 'A6': 0, 'A7': 0, 'A8': 0},
         'A2': {'B1': 0, 'B2': 0, 'B3': 0, 'B4': 0, 'B5': 0, 'B6': 0, 'B7': 0, 'B8': 0}
}

# Conjuntos que armazenam as vagas com tipos especiais
vagasDeficiente = {'T1', 'A1', 'B1'}
vagasIdoso = {'T2','T3','A2','A3','B2','B3'}

# Variáveis globais para controle de quantidade de carros e status dos andares
quantidadeCarrosAndarTerreo = 0
quantidadeCarrosAndar1 = 0
quantidadeCarrosAndar2 = 0

# Listas que armazenam informações sobre vagas ocupadas e carros
vagasOcupadasAndarTerreo = []
vagasOcupadasAndar1 = []
vagasOcupadasAndar2 = []

# Listas para armazenar carros aguardando estacionamento e saída
carrosAguardandoEstacionamento = []
carrosAguardandoSaida = []

# Lista de conexões para armazenar clientes conectados ao servidor
conexoes = []

# Buffers para armazenar temporariamente vagas ocupadas e valores
bufferVagasOcupadasAndarTerreo = []
bufferVagasOcupadasAndar1 = []
bufferVagasOcupadasAndar2 = []
carrosEstacionados = []
bufferValor = 0

# Variáveis para controle de status dos andares e encerramento do programa
estacionamentoFechado = False
andar1Fechado = False
andar2Fechado = False
statusAndarTerreo = "aberto"
statusAndar1 = "aberto"
statusAndar2 = "aberto"
encerrarProgramaViaSinal = False
paraPainel = False

# Função para encerrar o servidor
def encerraServidor():
    global encerrarProgramaViaSinal, conexao, server
    
    encerrarProgramaViaSinal = True
    time.sleep(1)
    for conexao in conexoes:
        conexao.close()
    time.sleep(1)
    server.close()

# Função para tratar o sinal SIGINT (Ctrl+C) e encerrar o programa
def handle_sigint(signal, frame):
    print("\nCtrl+C pressionado. Encerrando o programa...")
    encerraServidor()

# Define o sinal SIGINT para chamar a função handle_sigint ao pressionar Ctrl+C
signal.signal(signal.SIGINT, handle_sigint)

# Função para gerar um ID único para cada carro
def geraId():
    return str(uuid.uuid4())

# Classe para representar um carro estacionado
class Carro:
    def __init__(self,id,horaInicio):
        self.id = id
        self.horaInicio = horaInicio

# Função para ler as configurações do servidor a partir de um arquivo JSON
def get_json_from_argv():
    n = len(sys.argv)
    if n < 2:
        raise Exception("Deve-se inserir o nome de um arquivo de configuracao .json \n")
    json_file_name = sys.argv[1]
    parsed_data = {}
    with open(json_file_name, 'r') as json_file:
        parsed_data = json.load(json_file)
    return parsed_data

# Função principal para iniciar o servidor central
def servidorCentral():
    global statusAndar1,statusAndar2, statusAndarTerreo, estacionamentoFechado
    global encerrarProgramaViaSinal, conexoes, server
    if encerrarProgramaViaSinal:
        sys.exit()
    try:
        server_configs = get_json_from_argv()
    except:
        return print('Deve-se inserir o nome de um arquivo de configuracao .json \n')

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        
        server.bind((server_configs['ip_servidor_central'], server_configs['porta_servidor_central']))
        server.listen()
    except:
        return print('\n Erro ao iniciar servidor!\n')

    while not encerrarProgramaViaSinal:
        if encerrarProgramaViaSinal:
            sys.exit()
        try:
            conexao, addr = server.accept()
            print(f"Novo cliente: {addr}/n")
            conexoes.append(conexao)
            thread = threading.Thread(target=tratamentoDeMensagens, args=[conexao])
            thread.start()

        except socket.timeout:
            # Se nenhum cliente se conectar dentro do tempo limite, continua a execução
            continue
        except Exception as e:
            if not encerrarProgramaViaSinal:
                print("Erro ao aceitar conexão:", e)
            else:
                print("SERVIDOR ENCERRADO!\n")
            break
        

        
        
# Função para retornar o número de conexões ativas
def numero_conexoes_ativas():
    global conexoes
    return len(conexoes)

# Função para tratar as mensagens recebidas dos clientes (THREAD)
def tratamentoDeMensagens(conexao):
    global carrosAguardandoEstacionamento, carrosEstacionados, carrosAguardandoSaida
    global vagas, vagasIdoso, vagasDeficiente
    global quantidadeCarrosAndarTerreo, quantidadeCarrosAndar1, quantidadeCarrosAndar2
    global vagasOcupadasAndarTerreo, vagasOcupadasAndar1, vagasOcupadasAndar2
    global bufferVagasOcupadasAndarTerreo, bufferVagasOcupadasAndar1, bufferVagasOcupadasAndar2, bufferValor
    global statusAndar1, statusAndar2, statusAndarTerreo
    global estacionamentoFechado, andar1Fechado, andar2Fechado
    global encerrarProgramaViaSinal, paraPainel
    global conexoes

    while not encerrarProgramaViaSinal:
        if encerrarProgramaViaSinal:
            sys.exit()
        try:
            time.sleep(0.2)
            msg = conexao.recv(2048).decode('utf-8')
            msgJson =  json.loads(msg)
            #print(f"Recebido{msgJson}\n")
            if not msg:
                raise ConnectionError("Cliente desconectado")
            # broadcast(msg, client)
            if msgJson["from"] != "servidorCentral":
                if msgJson["from"] == "Terreo":
                    if msgJson["event"] == "novoCarro":
                        #print("Novo carro entrando...\n")
                        carrosAguardandoEstacionamento.append(Carro(geraId(),datetime.now()))
                        quantidadeCarrosAndarTerreo+=  1

                    elif msgJson["event"] == "carroSaindo":
                        try:
                            quantidadeCarrosAndarTerreo-= 1
                            carroSaindo = carrosAguardandoSaida.pop(0)
                            tempo = datetime.now() - carroSaindo.horaInicio
                            tempoMin = tempo.total_seconds() / 60
                            valorTotal = tempoMin * 0.10
                            bufferValor += valorTotal
                            for indice, (carro, vaga) in enumerate(carrosAguardandoSaida):
                                if carro.id == carroSaindo.id:  
                                    del carrosAguardandoSaida[indice]
                                    break  
                            print(f" O Carro  {carroSaindo.id} saiu e o preço é: R$ {valorTotal:.2f} e o total {bufferValor:.2f}")
                        except IndexError:
                            print("Lista de carros aguardando saída está vazia.")
                        
                    elif msgJson["event"] == "leitura_vagas":
                        #print(f'{msgJson["data"]["vagas"]}')
                        vagasOcupadasAndarTerreo = [f"T{indice+1}" for indice, ocupada in enumerate(msgJson["data"]["vagas"]) if ocupada == 1]
                        #print(vagasOcupadasAndarTerreo)

                        carrosQueSairam = list(set(bufferVagasOcupadasAndarTerreo) - set(vagasOcupadasAndarTerreo))

                        for i in carrosQueSairam:
                            vagaAtual = i

                            for indice, (carro, vaga) in enumerate(carrosEstacionados):
                                if vaga == vagaAtual:
                                    carrosAguardandoSaida.append(carro)
                                    del carrosEstacionados[indice]

                        bufferVagasOcupadasAndarTerreo = vagasOcupadasAndarTerreo

                        for i in vagasOcupadasAndarTerreo:

                            if  i in vagas['AT'].keys():
                                if vagas['AT'][i] == 0:
                                    carroAtual = carrosAguardandoEstacionamento.pop(0)
                                    print(f"O carro {carroAtual.id} acabou de chegar e estacionou na vaga {i}.")

                                    carrosEstacionados.append((carroAtual, i))
                                    for indice, (carro) in enumerate(carrosAguardandoEstacionamento):
                                        if carro.id == carroAtual.id:  
                                            del carrosAguardandoEstacionamento[indice]
                                            break  
                                    vagas['AT'][i] = 1
                    


                elif msgJson["from"] == "Andar1":
                    if msgJson["event"] == "sensorSubindo":
                        quantidadeCarrosAndarTerreo -=1
                        quantidadeCarrosAndar1 +=1
                        print("CARRO SUBINDO DO ANDAR T P/ 1")

                    elif msgJson["event"] == "sensorDescendo":
                        quantidadeCarrosAndarTerreo +=1
                        quantidadeCarrosAndar1 -=1
                        print("CARRO DESCENDO DO ANDAR 1 P/ T")

                    elif msgJson["event"] == "leitura_vagas":
                        vagasOcupadasAndar1 = [f"A{indice+1}" for indice, ocupada in enumerate(msgJson["data"]["vagas"]) if ocupada == 1]
                        carrosQueSairam = list(set(bufferVagasOcupadasAndar1) - set(vagasOcupadasAndar1))

                        for i in carrosQueSairam:
                            vagaAtual = i
                            for indice, (carro, vaga) in enumerate(carrosEstacionados):
                                if vaga == vagaAtual:
                                    carrosAguardandoSaida.append(carro)
                                    del carrosEstacionados[indice]

                        bufferVagasOcupadasAndar1 = vagasOcupadasAndar1

                        for i in vagasOcupadasAndar1:

                            if  i in vagas['A1'].keys():
                                if vagas['A1'][i] == 0:
                                    carroAtual = carrosAguardandoEstacionamento.pop(0)
                                    print(f"O carro {carroAtual.id} acabou de chegar e estacionou na vaga {i}.")

                                    carrosEstacionados.append((carroAtual, i))
                                    for indice, (carro) in enumerate(carrosAguardandoEstacionamento):
                                        if carro.id == carroAtual.id:  
                                            del carrosAguardandoEstacionamento[indice]
                                            break  
                                    vagas['A1'][i] = 1

                    

                elif msgJson["from"] == "Andar2":
                    if msgJson["event"] == "sensorSubindo":
                        quantidadeCarrosAndar1 -=1
                        quantidadeCarrosAndar2 +=1
                        print("CARRO SUBINDO DO ANDAR 1 P/ 2")
                    elif msgJson["event"] == "sensorDescendo":
                        quantidadeCarrosAndar1 +=1
                        quantidadeCarrosAndar2 -=1
                        print("CARRO DESCENDO DO ANDAR 2 P/ 1")

                    elif msgJson["event"] == "leitura_vagas":
                        vagasOcupadasAndar2 = [f"B{indice+1}" for indice, ocupada in enumerate(msgJson["data"]["vagas"]) if ocupada == 1]
                        carrosQueSairam = list(set(bufferVagasOcupadasAndar2) - set(vagasOcupadasAndar2))

                        for i in carrosQueSairam:
                            vagaAtual = i
                            for indice, (carro, vaga) in enumerate(carrosEstacionados):
                                if vaga == vagaAtual:
                                    carrosAguardandoSaida.append(carro)
                                    del carrosEstacionados[indice]

                        bufferVagasOcupadasAndar2 = vagasOcupadasAndar2

                        for i in vagasOcupadasAndar2:

                            if  i in vagas['A2'].keys():
                                if vagas['A2'][i] == 0:
                                    carroAtual = carrosAguardandoEstacionamento.pop(0)
                                    print(f"O carro {carroAtual.id} acabou de chegar e estacionou na vaga {i}.")

                                    carrosEstacionados.append((carroAtual, i))
                                    for indice, (carro) in enumerate(carrosAguardandoEstacionamento):
                                        if carro.id == carroAtual.id:  
                                            del carrosAguardandoEstacionamento[indice]
                                            break  
                                    vagas['A2'][i] = 1
                    
                else:
                    print("ANDAR INVÁLIDO\n")
                    break 
                if len(vagasOcupadasAndar1) >=8 or andar1Fechado == True:
                        statusAndar1 = "fechado"
                else:
                     statusAndar1 = "aberto"
                if len(vagasOcupadasAndar2) >=8 or andar2Fechado == True:
                        statusAndar2 = "fechado"
                else:
                    statusAndar2 = "aberto"
                
                if (statusAndar1 == "fechado" and statusAndar2 == "fechado" and len(vagasOcupadasAndarTerreo) >= 8) or estacionamentoFechado == True:

                    envia_evento_servidor(conexao,'status', {'Terreo': "fechado", 'Andar1': "fechado", 'Andar2': "fechado"})
                else:
                    envia_evento_servidor(conexao,'status', {'Terreo':statusAndarTerreo, 'Andar1': statusAndar1, 'Andar2': statusAndar2})   
        except ConnectionError:
            print("Cliente desconectado:", conexao)
            deleteClient(conexao)
            break
        except Exception as e:
            print("Erro ao receber mensagem:", e)
            deleteClient(conexao)
            break

# Funcao que envia os dados para os servidores distribuídos
def envia_evento_servidor(conexao, event: str, payload: dict):
        global encerrarProgramaViaSinal
        message_to_send = {
            "from": "servidorCentral",
            "event": event,
            'data': {**payload}
        }
        #print(message_to_send)
        if not encerrarProgramaViaSinal:
            try:
                conexao.send(json.dumps(message_to_send).encode())
            except BrokenPipeError:
                print("Erro de Broken Pipe ao enviar mensagem. Tentando reconectar...")
                conexao.send(json.dumps(message_to_send).encode())

# Funcao que remove uma determinada conexao de um cliente da lista de conexoes
def deleteClient(conexao):
    if conexao in conexoes:
        conexoes.remove(conexao)

# Exibe o painel em tempo real (THREAD)
def exibir_painel():
    global estacionamentoFechado, andar1Fechado, andar2Fechado, encerrarProgramaViaSinal, paraPainel, conexoes
    while not encerrarProgramaViaSinal:
        if encerrarProgramaViaSinal:
            sys.exit()
        
        # Limpa a tela
        print("\033[H\033[J")
        
        # Exibe as informações do estacionamento
        print("Painel em Tempo Real:")
        print("---------------------")
        print("Todos os andares:")
        print("Quantidade de carros no estacionamento:", quantidadeCarrosAndarTerreo + quantidadeCarrosAndar1 + quantidadeCarrosAndar2)
        print("Valor Arrecadado: R$", "{:.3f}".format(bufferValor))
        print("---------------------")
        print("Andar Terreo:")
        print("Quantidade de carros no andar:", quantidadeCarrosAndarTerreo)
        print("Vagas Regulares Disponíveis:", 5 - len([v for v in vagasOcupadasAndarTerreo if v not in vagasIdoso and v not in vagasDeficiente]))
        print("Vagas Idoso Disponíveis:", 2 - len([v for v in vagasOcupadasAndarTerreo if v in vagasIdoso]))
        print("Vagas Deficiente Disponíveis:", 1 - len([v for v in vagasOcupadasAndarTerreo if v in vagasDeficiente]))
        print("---------------------")
        print("Andar 1:")
        print("Quantidade de carros no andar:", quantidadeCarrosAndar1)
        print("Vagas Regulares Disponíveis:", 5 - len([v for v in vagasOcupadasAndar1 if v not in vagasIdoso and v not in vagasDeficiente]))
        print("Vagas Idoso Disponíveis:", 2 - len([v for v in vagasOcupadasAndar1 if v in vagasIdoso]))
        print("Vagas Deficiente Disponíveis:", 1 - len([v for v in vagasOcupadasAndar1 if v in vagasDeficiente]))
        print("---------------------")
        print("Andar 2:")
        print("Quantidade de carros no andar:", quantidadeCarrosAndar2)
        print("Vagas Regulares Disponíveis:", 5 - len([v for v in vagasOcupadasAndar2 if v not in vagasIdoso and v not in vagasDeficiente]))
        print("Vagas Idoso Disponíveis:", 2 - len([v for v in vagasOcupadasAndar2 if v in vagasIdoso]))
        print("Vagas Deficiente Disponíveis:", 1 - len([v for v in vagasOcupadasAndar2 if v in vagasDeficiente]))
        
        # Exibe informações adicionais, como valor acumulado
        print("---------------------")
        print("Informações Adicionais:")
        print("Número de clientes conectados:", numero_conexoes_ativas())
        print("---------------------")
        
        # Exibe opções para o usuário
        print("Comandos disponíveis (CMD + ENTER):")
        if estacionamentoFechado:
            print("1. Abrir estacionamento") 
        else:
            print("1. Fechar estacionamento")
        if andar1Fechado:
            print("2. Desbloquear Andar 1") 
        else:
            print("2. Bloquear Andar 1")
        if andar2Fechado:
            print("3. Desbloquear Andar 2") 
        else:
            print("3. Bloquear Andar 2")
        print("4. Encerrar servidor central")
        #print("5. Encerrar servidor central e distribuidos")
        
        # Aguarda 1 segundo antes de atualizar o painel novamente
        time.sleep(1)

# Aguarda o recebimento de comandos via teclado (THREAD)
def input_listener():
    global estacionamentoFechado, andar1Fechado, andar2Fechado, encerrarProgramaViaSinal, paraPainel, conexoes
    
    while not encerrarProgramaViaSinal:
        if encerrarProgramaViaSinal:
            sys.exit()
        
        # Aguarda a entrada do usuário
        comando = input("Escolha uma opção: ")
        
        # Executa o comando escolhido pelo usuário
        if comando == '1':
            estacionamentoFechado = not estacionamentoFechado
        elif comando == '2':
            andar1Fechado = not andar1Fechado
        elif comando == '3':
            andar2Fechado = not andar2Fechado
        elif comando == '4':
            print("ENCERRANDO...")
            encerraServidor()
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

# Chama o listener do teclado, criando uma thread e iniciando-a
def listener():
    listener_thread = threading.Thread(target=input_listener)
    listener_thread.daemon = True
    listener_thread.start()

#Chama o painel e cria uma thread
def painel():
    painel_thread = threading.Thread(target=exibir_painel)
    painel_thread.daemon = True  # Define a thread como daemon para que seja interrompida quando o programa principal encerrar
    painel_thread.start()
    
# Roda o servidor central em uma thread separada
def runServidor():
    servidor_thread = threading.Thread(target = servidorCentral)
    servidor_thread.start()

if __name__ == '__main__':
    runServidor()
    painel()
    listener()
    
