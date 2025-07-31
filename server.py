import socket
import threading
from time import sleep
PASSWORD = "qwer"
RUNNING = True

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 9999))
server.listen(1)

print('wait for clients')
clients = []
addr_map = {}
name_map = {}

def handle_client(conn, addr):
    try:
        global name_map
        conn.send(b'[LOGIN] To enter chatroom, enter the password')
        inp = conn.recv(1024).decode()
        while inp.lower() != 'qwer':
            sleep(1)
            conn.send(b'[WRONG] password was incorrect, try again.')
            inp = conn.recv(1024).decode()

        
        conn.send(b'[CORRECT]\nNow to enter chatroom, choose a proper username.')

        name = conn.recv(1024).decode()
        while name in name_map:
            sleep(1)
            conn.send(b'[USERNAME] your chosen name is not unique.')
            name = conn.recv(1024).decode().lower()

        name_map[name] = conn
        conn.send(b'[ENJOY] ..Welcome To The Internet..')
        brodcast_to_all(conn, f'[+] client {addr[1]} just came')
        while True:
            data = conn.recv(1024).decode()
            if data == 'exit':
                brodcast_to_all(conn, f'[-] client {addr[1]} gone')
                clients.remove(conn)
                conn.close()
                return
                

            brodcast_to_all(conn, f'[] {addr[1]}: {data}')
    except:
        return


def brodcast_to_all(cli, msg):
    for cli_con in clients:
        if cli_con != cli:
            cli_con.send(msg.encode())

def admin_commands():
    while True:
        com = input()
        if com == 'quit':
            brodcast_to_all('', '[ADMIN] The server is closed.\nBye Bye')
            for con in clients:
                con.close()
            RUNNING = False
            quit()


        if com.startswith('kick'):
            for i in map(int, com.split()[1:]):
                if addr_map.get(i):
                    addr_map[i].send(b'[ADMIN] you\'ve been kicked out')
                    clients.remove(addr_map[i])
                    addr_map[i].close()

                if name_map.get(i):
                    name_map[i].send(b'[ADMIN] you\'ve been kicked out')
                    clients.remove(name_map[i])
                    name_map[i].close()



thread = threading.Thread(target=admin_commands)
thread.start()

while RUNNING:
    cli_con, addr = server.accept()
    clients.append(cli_con)
    addr_map[addr] = cli_con
    thread = threading.Thread(target=handle_client, args=(cli_con, addr))
    thread.start()
