import PySimpleGUI as sg
import socket

sg.theme('DarkBlue2')

def get_port_ip():
    layout = [
        [sg.Text('Digite o IP para conectar:'), sg.InputText(key='ip')],
        [sg.Text('Digite a porta para conectar:'), sg.InputText(key='porta')],
        [sg.Button('Conectar')],
    ]

    window = sg.Window('Configuração de IP e Porta', layout)

    ip, porta = 'localhost', 18000  # Valores padrão
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

def send_message(msg):
    message = msg.encode(FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER - len(send_len))
    client.send(send_len)
    client.send(message)
    return client.recv(2048).decode(FORMAT)

def main():

    layout = [
        [sg.Text('Digite uma mensagem:')],
        [sg.InputText(key='input_text')],
        [sg.Button('Send')],
    ]

    window = sg.Window('Chat Cliente', layout)

    while True:
        event, values = window.read()

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
                response = send_message(message)
                sg.popup(f'Resposta do servidor: {response}')

    window.close()
    client.close()

if __name__ == '__main__':
    main()
