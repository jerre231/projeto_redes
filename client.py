import PySimpleGUI as sg
import socket
import threading

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
    event = threading.Event()

    def send_thread():
        message = msg.encode(FORMAT)
        msg_len = len(message)
        send_len = str(msg_len).encode(FORMAT)
        send_len += b' ' * (HEADER - len(send_len))
        client.send(send_len)
        client.send(message)
        event.set()

    thread = threading.Thread(target=send_thread)
    thread.start()
    thread.join()

    return event.wait(1000)

def receive_message():
    while True:
        try:
            response = client.recv(2048).decode(FORMAT)
            
            #if "127.0.0.1" not in response:  ##Tentativa de tirar a duplicata de mensagens no cliente
            print(f'Servidor: {response}')

        except:
            break
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
                send_message(message)
                #window['-OUTPUT-'].update(f'Você: {message}\n', append=True)

    window.close()
    client.close()

if __name__ == '__main__':
    main()
