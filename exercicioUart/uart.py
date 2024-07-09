import termios
import os
from time import sleep
import struct
## FINAL MATRICULA 6925

##PARTE 01 - SOLICITACAO DE DADOS #######################################################

def enviaLeInt():
    print("Enviando solicitacao de INT............")
    uarto_filestream = os.open(
        "/dev/serial0", os.O_RDWR | os.O_NOCTTY | os.O_NDELAY)

    # DEFINIÇÃO DAS FLAGS DO ARQUIVO (fonte: termios.tcgetattr(fd))

    #    Get the tty attributes for file descriptor fd.
    #    Returns a list [iflag, oflag, cflag, lflag, ispeed, ospeed, cc] where cc is a list of the tty special characters (each a string of length 1, except the items with indices VMIN and VTIME, which are integers when these fields are defined). The interpretation of the flags and the speeds as well as the indexing in the cc array must be done using the symbolic constants defined in this module.

    # Pega valor das flags
    [iflag, oflag, cflag, lflag] = [0, 1, 2, 3]

    attrs: termios._Attr = termios.tcgetattr(uarto_filestream)

    attrs[cflag] = termios.B9600 | termios.CS8 | termios.CLOCAL | termios.CREAD
    attrs[iflag] = termios.IGNPAR
    attrs[oflag] = 0
    attrs[lflag] = 0

    termios.tcflush(uarto_filestream, termios.TCIFLUSH)
    termios.tcsetattr(uarto_filestream, termios.TCSANOW, attrs)

    envia = [161,6,9,2,5]
    print(f"Escreveu {envia} ({len(envia)} bytes)")
    os.write(uarto_filestream, bytes(envia))

    sleep(1)

    leitura = os.read(uarto_filestream, 4)
    inteiro = int.from_bytes(leitura, byteorder='little')
    print(f"Leu {len(leitura)} bytes")
    print(f"Bytes da leitura: {inteiro}")

    os.close(uarto_filestream)

def enviaLeFloat():
    print("Enviando solicitacao de FLOAT..........")
    uarto_filestream = os.open(
        "/dev/serial0", os.O_RDWR | os.O_NOCTTY | os.O_NDELAY)

    # DEFINIÇÃO DAS FLAGS DO ARQUIVO (fonte: termios.tcgetattr(fd))

    #    Get the tty attributes for file descriptor fd.
    #    Returns a list [iflag, oflag, cflag, lflag, ispeed, ospeed, cc] where cc is a list of the tty special characters (each a string of length 1, except the items with indices VMIN and VTIME, which are integers when these fields are defined). The interpretation of the flags and the speeds as well as the indexing in the cc array must be done using the symbolic constants defined in this module.

    # Pega valor das flags
    [iflag, oflag, cflag, lflag] = [0, 1, 2, 3]

    attrs: termios._Attr = termios.tcgetattr(uarto_filestream)

    attrs[cflag] = termios.B9600 | termios.CS8 | termios.CLOCAL | termios.CREAD
    attrs[iflag] = termios.IGNPAR
    attrs[oflag] = 0
    attrs[lflag] = 0

    termios.tcflush(uarto_filestream, termios.TCIFLUSH)
    termios.tcsetattr(uarto_filestream, termios.TCSANOW, attrs)

    envia = [162,6,9,2,5]
    print(f"Escreveu {envia} ({len(envia)} bytes)")
    os.write(uarto_filestream, bytes(envia))

    sleep(1)

    leitura = os.read(uarto_filestream, 4)
    float_value =  struct.unpack('f', leitura)[0]
    print(f"Leu {len(leitura)} bytes")
    print(f"Bytes da leitura: {float_value}")

    os.close(uarto_filestream)

def enviaLeString():
    print("Enviando solicitacao de String.............")
    uarto_filestream = os.open(
        "/dev/serial0", os.O_RDWR | os.O_NOCTTY | os.O_NDELAY)

    # DEFINIÇÃO DAS FLAGS DO ARQUIVO (fonte: termios.tcgetattr(fd))

    #    Get the tty attributes for file descriptor fd.
    #    Returns a list [iflag, oflag, cflag, lflag, ispeed, ospeed, cc] where cc is a list of the tty special characters (each a string of length 1, except the items with indices VMIN and VTIME, which are integers when these fields are defined). The interpretation of the flags and the speeds as well as the indexing in the cc array must be done using the symbolic constants defined in this module.

    # Pega valor das flags
    [iflag, oflag, cflag, lflag] = [0, 1, 2, 3]

    attrs: termios._Attr = termios.tcgetattr(uarto_filestream)

    attrs[cflag] = termios.B9600 | termios.CS8 | termios.CLOCAL | termios.CREAD
    attrs[iflag] = termios.IGNPAR
    attrs[oflag] = 0
    attrs[lflag] = 0

    termios.tcflush(uarto_filestream, termios.TCIFLUSH)
    termios.tcsetattr(uarto_filestream, termios.TCSANOW, attrs)

    envia = [163,6,9,2,5]
    print(f"Escreveu {envia} ({len(envia)} bytes)")
    os.write(uarto_filestream, bytes(envia))

    sleep(1)

    leitura = os.read(uarto_filestream, 255).decode("UTF-8")
    print(f"Leu {len(leitura)} bytes")
    print(f"Bytes da leitura: {leitura}")

    os.close(uarto_filestream)

########################################################################

##PARTE 02 - ESCRITA DE DADOS


def escreveLeInt():
    print("ESCREVENDO INT................")
    uarto_filestream = os.open(
        "/dev/serial0", os.O_RDWR | os.O_NOCTTY | os.O_NDELAY)

    # DEFINIÇÃO DAS FLAGS DO ARQUIVO (fonte: termios.tcgetattr(fd))

    #    Get the tty attributes for file descriptor fd.
    #    Returns a list [iflag, oflag, cflag, lflag, ispeed, ospeed, cc] where cc is a list of the tty special characters (each a string of length 1, except the items with indices VMIN and VTIME, which are integers when these fields are defined). The interpretation of the flags and the speeds as well as the indexing in the cc array must be done using the symbolic constants defined in this module.

    # Pega valor das flags
    [iflag, oflag, cflag, lflag] = [0, 1, 2, 3]

    attrs: termios._Attr = termios.tcgetattr(uarto_filestream)

    attrs[cflag] = termios.B9600 | termios.CS8 | termios.CLOCAL | termios.CREAD
    attrs[iflag] = termios.IGNPAR
    attrs[oflag] = 0
    attrs[lflag] = 0

    termios.tcflush(uarto_filestream, termios.TCIFLUSH)
    termios.tcsetattr(uarto_filestream, termios.TCSANOW, attrs)

    envia = [177,20,6,9,2,5]
    print(f"Escreveu {envia} ({len(envia)} bytes)")
    os.write(uarto_filestream, bytes(envia))

    sleep(2)

    leitura = os.read(uarto_filestream, 4)
    inteiro = int.from_bytes(leitura, byteorder='little')
    print(f"Leu {len(leitura)} bytes")
    print(f"Bytes da leitura: {inteiro}")

    os.close(uarto_filestream)

def escreveLeFloat():
    print("ESCREVENDO  FLOAT............")
    uarto_filestream = os.open(
        "/dev/serial0", os.O_RDWR | os.O_NOCTTY | os.O_NDELAY)

    # DEFINIÇÃO DAS FLAGS DO ARQUIVO (fonte: termios.tcgetattr(fd))

    #    Get the tty attributes for file descriptor fd.
    #    Returns a list [iflag, oflag, cflag, lflag, ispeed, ospeed, cc] where cc is a list of the tty special characters (each a string of length 1, except the items with indices VMIN and VTIME, which are integers when these fields are defined). The interpretation of the flags and the speeds as well as the indexing in the cc array must be done using the symbolic constants defined in this module.

    # Pega valor das flags
    [iflag, oflag, cflag, lflag] = [0, 1, 2, 3]

    attrs: termios._Attr = termios.tcgetattr(uarto_filestream)

    attrs[cflag] = termios.B9600 | termios.CS8 | termios.CLOCAL | termios.CREAD
    attrs[iflag] = termios.IGNPAR
    attrs[oflag] = 0
    attrs[lflag] = 0

    termios.tcflush(uarto_filestream, termios.TCIFLUSH)
    termios.tcsetattr(uarto_filestream, termios.TCSANOW, attrs)
    
    float_value = 3.1415

    # float para uma representação binária
    float_bytes = struct.pack('f', float_value)  # 'f' para float de precisão simples (4 bytes)

    # Lista de bytes para enviar
    envia = [178] + list(float_bytes) + [6, 9, 2, 5]
    print(f"Escreveu {envia} ({len(envia)} bytes)")
    os.write(uarto_filestream, bytes(envia))

    sleep(1)

    leitura = os.read(uarto_filestream, 4)
    float_value =  struct.unpack('f', leitura)[0]
    print(f"Leu {len(leitura)} bytes")
    print(f"Bytes da leitura: {float_value}")

    os.close(uarto_filestream)


def escreveLeString():
    print("Escrevendo  String................")
    uarto_filestream = os.open(
        "/dev/serial0", os.O_RDWR | os.O_NOCTTY | os.O_NDELAY)

    # DEFINIÇÃO DAS FLAGS DO ARQUIVO (fonte: termios.tcgetattr(fd))

    #    Get the tty attributes for file descriptor fd.
    #    Returns a list [iflag, oflag, cflag, lflag, ispeed, ospeed, cc] where cc is a list of the tty special characters (each a string of length 1, except the items with indices VMIN and VTIME, which are integers when these fields are defined). The interpretation of the flags and the speeds as well as the indexing in the cc array must be done using the symbolic constants defined in this module.

    # Pega valor das flags
    [iflag, oflag, cflag, lflag] = [0, 1, 2, 3]

    attrs: termios._Attr = termios.tcgetattr(uarto_filestream)

    attrs[cflag] = termios.B9600 | termios.CS8 | termios.CLOCAL | termios.CREAD
    attrs[iflag] = termios.IGNPAR
    attrs[oflag] = 0
    attrs[lflag] = 0

    termios.tcflush(uarto_filestream, termios.TCIFLUSH)
    termios.tcsetattr(uarto_filestream, termios.TCSANOW, attrs)

    stt = "HELLO iam Hugo" #STRING PARA SER ENVIADA

    stt_bytes = stt.encode("utf-8") #ENCODE DA STRING

    envia = [179, len(stt_bytes)] + list(stt_bytes) + [6, 9, 2, 5]

    print(f"Escreveu {envia} ({len(envia)} bytes)")
    os.write(uarto_filestream, bytes(envia))

    sleep(1)

    leitura = os.read(uarto_filestream, 255).decode("UTF-8")
    print(f"Leu {len(leitura)} bytes")
    print(f"Bytes da leitura: {leitura}")

    os.close(uarto_filestream)






########################################################################




## CHAMADA DAS FUNCOES
print("EXERCICIO 01 - UART")
enviaLeInt()
sleep(1)
enviaLeFloat()
sleep(1)
enviaLeString()
sleep(2)
escreveLeInt()
sleep(2)
escreveLeFloat()
sleep(2)
escreveLeString()
