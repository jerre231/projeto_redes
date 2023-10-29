import socket 

HEADER = 64
PORT = 18000
FORMAT ='utf-8'
SERVER = 'localhost'
ADDR = (SERVER, PORT)
DISCONNECT = ':D'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):

        message = msg.encode(FORMAT)
        msg_len = len(message)
        send_len = str(msg_len).encode(FORMAT)
        send_len += b' ' * (HEADER - len(send_len))
        client.send(send_len)
        client.send(message)
        print(client.recv(2048).decode(FORMAT))
        
while True:
    entry = input('Sua mensagem: ')
    if entry == DISCONNECT:
        send(entry)
        print('Desconctando...')
        break
    
    else:
        send(entry)
    
# if __name__=='__main__':
#     quantidade = int(input('Quantas msgs vc vai mandar? '))
#     for i in range(quantidade):
#         entry = input('Sua mensagem: ')
#         send(entry)


