
################################################################################
#                                                                              #
#                           CONTROLE DE ESTACIONAMENTOS                        #
#                              SERVIDOR DISTRIBUÍDO                            #
#                           TRABALHO 1 - FSE - 2024.1                          #
#                          Hugo Rocha e Samuel Bacelar                         #
#                                                                              #
################################################################################

import RPi.GPIO as GPIO
import sys
from typing import Dict, Literal, Union
import json
import time
import socket
import threading
import signal

# Variáveis globais
carros = 0
ordem = []
contadorSensor = 0

# Definição dos nomes dos pinos GPIO
pin_nomes = Literal['ENDERECO_01',
                    'ENDERECO_02',
                    'ENDERECO_03',
                    'SENSOR_DE_VAGA',
                    'SINAL_DE_LOTADO_FECHADO',
                    'SENSOR_DE_PASSAGEM_1',
                    'SENSOR_DE_PASSAGEM_2',
                    'MOTOR_CANCELA_ENTRADA',
                    ]

# Função para lidar com o sinal SIGINT (Ctrl+C)
def handle_sigint(signal, frame):
    global encerrarPrograma
    print("\nCtrl+C pressionado. Encerrando o programa...")
    encerrarPrograma = True

# Configura o sinal SIGINT para chamar a função handle_sigint quando recebido
signal.signal(signal.SIGINT, handle_sigint)

# Inicialização de variável para indicar se o programa deve ser encerrado
encerrarPrograma = False

# Classe para representar um pino GPIO
class GPIOPin:
    def __init__(self, name: str, gpio: int, direction: Literal["INPUT", "OUTPUT"]):
        self.name = name
        self.gpio = gpio
        self.direction = direction
        # Configura o pino GPIO com a direção especificada
        gpio_direction = GPIO.IN if direction == 'INPUT' else GPIO.OUT
        if direction == 'INPUT':
            GPIO.setup(gpio, gpio_direction, pull_up_down=GPIO.PUD_DOWN )
        else:
            GPIO.setup(gpio, gpio_direction, initial=GPIO.LOW)

    def output(self, value: Union[Literal[0, 1], bool, list[Union[Literal[0, 1], bool]], tuple[Union[Literal[0, 1], bool], ...]]):
        # Define o valor de saída para o pino GPIO
        if self.direction != 'OUTPUT':
            raise Exception(
                f"Não é possível enviar um sinal pois o Pino {self} está marcado como {self.direction}")
        GPIO.output(self.gpio, value)

    def input(self) -> bool:
        if self.direction != 'INPUT':
            raise Exception(
                f"Não é possível receber um sinal pois o Pino {self} está marcado como {self.direction}")
        return GPIO.input(self.gpio)

    def wait_for_edge(self, edge: int) -> (Union[int, None]):
        return GPIO.wait_for_edge(self.gpio, edge)

    def __repr__(self) -> str:
        return f"{self.name}\tgpio: {self.gpio}"

# Definição de um tipo de dados para representar um índice de vaga
vaga_index = Literal[0, 1, 2, 4, 5, 6, 7]

# Classe para representar o servidor de um andar do estacionamento, que não seja o térreo
class FloorServer:
    def __init__(self, name: str, host: str, port: int,  pinout: list[dict]):
        self.name = name
        self.port = port
        self.host = host
        self.pinout: Dict[pin_nomes, GPIOPin] = {}
        self.is_lotado = False
        self.gpio_setup(pinout)
        self.vagas = [0 for i in range(8)]
        self.socket: socket
        self.setup_socket()

    def setup_socket(self):
        global encerrarPrograma
        while True:
            if encerrarPrograma:
                sys.exit()
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((self.host, self.port))
                print("Conectado ao servidor central.")
                break
            except ConnectionRefusedError:
                print("Servidor Central não está conectado. Tentando Reconexão em 3s")
                time.sleep(3)
            except Exception as e:
                print("Ocorreu um erro durante a conexão:", e)
                print("Tentando Reconexão em 3s")
                time.sleep(3)


    def gpio_setup(self, pinout: list[dict]):
        # Configura os pinos GPIO com base na lista de configurações
        GPIO.setmode(GPIO.BCM)
        for pin in pinout:
            self.pinout[pin['name']] = GPIOPin(
                name=pin['name'], gpio=pin['gpio'], direction=pin['direction'])

            


        #self.pinout['SINAL_DE_LOTADO_FECHADO'].output(self.is_lotado)
        
    
    def read_sensor_vaga(self, endereco: vaga_index):
        # Lê o estado de um sensor de vaga específico
        if endereco > 7:
            raise Exception(f"Vaga de número {endereco} Inexistente.")
        self.pinout['ENDERECO_01'].output((endereco & 0b001) == 0b001)
        self.pinout['ENDERECO_02'].output((endereco & 0b010) == 0b010)
        self.pinout['ENDERECO_03'].output((endereco & 0b100) == 0b100)
        time.sleep(0.3)  # Espera para estabilização do sinal
        result = self.pinout['SENSOR_DE_VAGA'].input()
        return result

    def set_luz_lotado(self, valor: Union[bool, Literal[0, 1]]):
        # Define o estado da luz de lotação
        self.is_lotado = valor
        self.pinout['SINAL_DE_LOTADO_FECHADO'].output(valor)
        lotado_texto = "fechado " if not self.is_lotado else "aberto"
        print(f"{self} {lotado_texto}")

    def envia_evento_servidor(self, event: str, payload: dict):
        # Envia um evento para o servidor central
        message_to_send = {
            "from": self.__str__(),
            "event": event,
            'data': {**payload}
        }
        print(message_to_send)
        try:
            self.socket.send(json.dumps(message_to_send).encode())
        except BrokenPipeError:
            print("Erro de Broken Pipe ao enviar mensagem. Tentando reconectar...")
            self.setup_socket()  # Tentar reconectar
            self.socket.send(json.dumps(message_to_send).encode())


    def recebe_mensagem(self):
        # Aguarda por mensagens do servidor central
        global encerrarPrograma
        
        while True:
            if encerrarPrograma:
                sys.exit()
            try:
                time.sleep(0.1)
                message = self.socket.recv(2048).decode()
                msgJson =  json.loads(message)
                print(f"Recebido{msgJson}\n")
                if not message:
                    raise ConnectionError("Cliente desconectado")
                if msgJson["from"] == "servidorCentral" and msgJson["event"] == "encerrar_programa":
                    print("Recebido comando para encerrar o programa.")
                    encerrarPrograma = True
                    #sys.exit() INSERIR FORMA DE MATAR O PROGRAMA
                elif msgJson["from"] == "servidorCentral" and msgJson["event"] == "status":
                    for andar, status in msgJson["data"].items():
                        if andar == self.name:
                            if status == "aberto":
                                self.set_luz_lotado(valor=False)
                            else:
                                self.set_luz_lotado(valor=True)
                

            except socket.error as e:
                print(f"Erro de socket: {e}")
                print("Tentando Reconexão em 3s")
                time.sleep(3)
            except Exception as e:
                print(f"Ocorreu um erro: {e}")
    
    def handle_sensor(self, channel):
    # Lida com a ativação dos sensores de passagem
        global contadorSensor, carros
        if channel == self.pinout['SENSOR_DE_PASSAGEM_1'].gpio:
            if GPIO.input(self.pinout['SENSOR_DE_PASSAGEM_1'].gpio):  # Se a borda for de subida
                if contadorSensor < 2:
                    ordem.append(1)
                    contadorSensor+=1       
        elif channel == self.pinout['SENSOR_DE_PASSAGEM_2'].gpio:
            if GPIO.input(self.pinout['SENSOR_DE_PASSAGEM_2'].gpio):  # Se a borda for de subida
                if contadorSensor < 2:
                    ordem.append(2)
                    contadorSensor+=1
                
        if len(ordem) == 2:
            primeiro = ordem.pop(0)
            segundo = ordem.pop(0)
            if primeiro == 1 and segundo == 2:
                self.envia_evento_servidor('sensorSubindo', {'a': "a"})
                contadorSensor =0
            else:
                self.envia_evento_servidor('sensorDescendo', {'a': "a"})
                contadorSensor = 0


    def trata_mudanca_de_nivel(self, *args):
        # Trata a mudança de nível dos sensores de passagem
        global encerrarPrograma
        if encerrarPrograma:
            sys.exit()
        GPIO.add_event_detect(self.pinout['SENSOR_DE_PASSAGEM_1'].gpio, GPIO.BOTH, callback=self.handle_sensor)
        GPIO.add_event_detect(self.pinout['SENSOR_DE_PASSAGEM_2'].gpio, GPIO.BOTH, callback=self.handle_sensor)
        

    def verifica_vagas(self):
        # Verifica o estado das vagas do estacionamento
        global encerrarPrograma
        global carros
        while True:
            if encerrarPrograma:
                sys.exit()
            mudou_estado = False
            
            for endereco_vaga in range(8):
                estado_vaga = self.read_sensor_vaga(endereco_vaga)
                self.vagas[endereco_vaga] = estado_vaga
            print("Vagas: ", self.vagas)
            print("Enviando novo estado das vagas para o servidor central.")
            print(self.vagas)
            print(f"CARROS: {carros}")
            self.envia_evento_servidor('leitura_vagas', {'vagas': self.vagas})

    def __str__(self) -> str:
        return self.name

    def run(self):
        # Inicia as threads para execução das tarefas
        thread_vagas = threading.Thread(target=self.verifica_vagas)
        if self.name != "Terreo": 
            thread_mudar_nivel = threading.Thread(
            target=self.trata_mudanca_de_nivel)
        # thread_send = threading.Thread(target=self.send_message)
        thread_receive = threading.Thread(target=self.recebe_mensagem)

        # thread_send.start()
        thread_receive.start()
        thread_vagas.start()
        if self.name != "Terreo": 
            thread_mudar_nivel.start()


pin_nomes_terreo = Union[pin_nomes, Literal[
    "SENSOR_ABERTURA_CANCELA_ENTRADA",
    "SENSOR_FECHAMENTO_CANCELA_ENTRADA",
    "MOTOR_CANCELA_ENTRADA",
    "SENSOR_ABERTURA_CANCELA_SAIDA",
    "SENSOR_FECHAMENTO_CANCELA_SAIDA",
    "MOTOR_CANCELA_SAIDA"]]

# Classe para representar o servidor do térreo do estacionamento

class TerreoServer(FloorServer):
    
    def __init__(self, name: str, host: str, port: int, pinout: list[dict]):
        self.pinout: Dict[pin_nomes_terreo, GPIOPin] = {}
        super().__init__(name, host, port, pinout)

    def lida_cancela(self, cancela_type: Literal["MOTOR_CANCELA_ENTRADA", "MOTOR_CANCELA_SAIDA"], sinal: Literal[0, 1]):
        self.pinout[cancela_type].output(sinal)

    def trata_cancela_entrada(self):
        global encerrarPrograma
        
        while True:
            if encerrarPrograma:
                sys.exit()
            time.sleep(0.1)
            if self.pinout['SENSOR_ABERTURA_CANCELA_ENTRADA'].input() == GPIO.HIGH:
                # GPIO.output(MOTOR_CANCELA_ENTRADA, GPIO.HIGH)
                self.envia_evento_servidor(
                    'novoCarro', {})
                self.lida_cancela('MOTOR_CANCELA_ENTRADA', GPIO.HIGH)
                print("Veiculo entrando")

                if self.pinout['SENSOR_FECHAMENTO_CANCELA_ENTRADA'].wait_for_edge(GPIO.RISING):
                    # Desativa cancela
                    self.lida_cancela('MOTOR_CANCELA_ENTRADA', GPIO.LOW)
                    print("Cancela fechada")

    def trata_cancela_saida(self):
        global encerrarPrograma
        
        while True:
            if encerrarPrograma:
                sys.exit()
            time.sleep(0.1)
            if self.pinout['SENSOR_ABERTURA_CANCELA_SAIDA'].input() == GPIO.HIGH:
                time.sleep(3)
                self.envia_evento_servidor(
                    'carroSaindo', {})
                self.lida_cancela('MOTOR_CANCELA_SAIDA', GPIO.HIGH)
                print("Veiculo saindo")
                if self.pinout['SENSOR_FECHAMENTO_CANCELA_SAIDA'].wait_for_edge(GPIO.RISING):
                    time.sleep(0.4)
                    self.lida_cancela('MOTOR_CANCELA_SAIDA', GPIO.LOW)
                    print("Cancela fechada")

    def run(self):
        thread_cancela_entrada = threading.Thread(
            target=self.trata_cancela_entrada)
        thread_cancela_saida = threading.Thread(
            target=self.trata_cancela_saida)
        thread_cancela_entrada.start()
        thread_cancela_saida.start()
        super().run()


def get_args():
    n = len(sys.argv)
    if n < 2:
        raise Exception(
            "Deve-se inserir o arquivo de configuração json.")
    json_file_name = sys.argv[1]
    parsed_data = {}
    with open(json_file_name, 'r') as json_file:
        parsed_data = json.load(json_file)
    return parsed_data


def main():
    server_configs = get_args()
    if server_configs['nome'] == "Terreo":
        server = TerreoServer(name=server_configs['nome'],
                              host=server_configs['ip_servidor_central'],
                              port=server_configs['porta_servidor_central'],
                              pinout=server_configs['pinout'])
    else:
        server = FloorServer(name=server_configs['nome'],
                             host=server_configs['ip_servidor_central'],
                             port=server_configs['porta_servidor_central'],
                             pinout=server_configs['pinout'])
    server.run()

if __name__ == '__main__':
    main()
