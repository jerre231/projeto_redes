import PySimpleGUI as sg
import socket

HEADER = 64
PORT = 18000
FORMAT = 'utf-8'
SERVER = 'localhost'
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
    sg.theme('DarkBlue2')

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
