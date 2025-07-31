import socket
import threading

running = True
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('46.249.99.69', 9999))

def receive_messages(conn):
    global running
    while running:
        print('in thread')
        try:
            msg = conn.recv(1024).decode()
            print('\n', msg)
            if msg == '':
                print('[Disconnected]')
                raise ValueError('Disconnect')
        except:
            print('\n\nBYE')
            conn.close()
            running = False
            return


thread = threading.Thread(target=receive_messages, args=(client, ))
thread.start()
while running:
    msg = input('message: ')
    if not running:
        break
    client.send(msg.encode())
    if msg == 'exit':
        break
client.close()

