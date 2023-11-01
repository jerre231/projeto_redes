import PySimpleGUI as sg
import socket
import threading
import queue

sg.theme('DarkBlue2')

def get_port_ip():
    layout = [
        [sg.Text('Digite o IP para conectar:'), sg.InputText(key='ip')],
        [sg.Text('Digite a porta para conectar:'), sg.InputText(key='porta')],
        [sg.Button('Conectar')],
    ]

    window = sg.Window('Configuração de IP e Porta', layout)

    ip, porta = 'localhost', 18000  # Default values
    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            window.close()
            break
        elif event == 'Conectar':
            ip = values['ip']
            porta = values['porta']
            window.close()

    return ip, porta

ip, porta = get_port_ip()

if not porta:
    porta = 18000
else:
    try:
        porta = int(porta)
    except ValueError:
        porta = 18000

HEADER = 64
FORMAT = 'utf-8'
SERVER = ip
PORT = porta
ADDR = (SERVER, PORT)
DISCONNECT = ':D'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

message_queue = queue.Queue()

def send_message(msg):
    message = msg.encode(FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER - len(send_len))
    client.send(send_len)
    client.send(message)
    return client.recv(2048).decode(FORMAT)

def receive_message():
    while True:
        try:
            response = client.recv(2048).decode(FORMAT)
            message_queue.put(response)
        except:
            pass

def main():
    layout = [
        [sg.Text('Bate-Papo com o Servidor')],
        [sg.Output(size=(50, 10), key='-OUTPUT-')],
        [sg.InputText(key='input_text')],
        [sg.Button('Send')],
    ]

    window = sg.Window('Chat Cliente', layout)

    thread = threading.Thread(target=receive_message)
    thread.daemon = True
    thread.start()

    while True:
        event, values = window.read(timeout=100)

        if event == sg.WINDOW_CLOSED:
            send_message(DISCONNECT)
            break
        elif event == 'Send':
            message = values['input_text']
            if message == DISCONNECT:
                send_message(message)
                sg.popup('Desconectando...')
                break
            else:
                send_message(message)
                print(f'Você: {message}')

        try:
            while True:
                message = message_queue.get_nowait()
                print(f'Servidor: {message}')
        except queue.Empty:
            pass

    window.close()
    client.close()

if __name__ == '__main__':
    main()