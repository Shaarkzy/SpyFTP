#-------------------------------------------------------------------------

# import libraries 
import os
from os import system
import datetime
import socket
import subprocess
from os.path import exists
import time

#------------------------------------------------------------------------

# print out a character in prefered length
class global_sv:

    def __init__(self, charac):
        self.charac = charac
        self.flag = False

    def print_out(self, num):
        print(self.charac*num)

#------------------------------------------------------------------------


# server communication
class server_comms:

    # initialize constants and starting socket
    def __init__(self, port):
        self.flag = False
        self.dict = {}
        self.char = '='
        self.num = 64
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind(('0.0.0.0', int(port)))
        except:
            global_sv(self.char).print_out(self.num)
            print(f'[x] PORT {port} ADDRESS ALREADY IN USE OR INVALID PORT')
            print('[*] CLOSING SERVER: PLEASE TRY DIFFERENT PORT OR \nKILL THE PROCESS USING THE PORT <kill -9 process_pid>')
            global_sv(self.char).print_out(self.num) 
            os._exit(0)

        global_sv(self.char).print_out(self.num)
        print(f'[*] SERVER STARTED @ {server_relay().time_log()}')
        global_sv(self.char).print_out(self.num)
        time.sleep(1)
        print('[!] IT\'S NOT ADVISABLE TO SEND OR RECEIVE FILE WITHIN THE SAME\nDIRECTORY ON THE SAME MACHINE TO AVOID FILE CORRUPTION')
        global_sv(self.char).print_out(self.num)
        sock.listen(5)
        try:
            con, addr = sock.accept()
        except:
            os._exit(0)

        print(f'[*] CLIENT CONNECTED @ {server_relay().time_log()}')
        global_sv(self.char).print_out(self.num)
        self.con = con
        self.sock = sock
        print('---------------------SERVER REALTIME LOG------------------------')
    
    # close server communication and program
    def close_socket(self):
        print('[*] SERVER CLOSED')
        self.sock.close()
        self.con.close()
        os._exit(0)

#   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -

    # receive incoming data from the server
    def receive_data(self, code):
        con = self.con
        if code:
            # mode to receive static data
            length = int.from_bytes(con.recv(4), byteorder='big')
            data = con.recv(length).decode()
        else:
            # mode to receive streaming data
            data = con.recv(4096)
        return data


    # send data to the client
    def send_data(self, data, code):
        con = self.con
        if code:
            # mode to send static data
            con.send(len(data).to_bytes(4, byteorder='big'))
            con.send(data.encode())
        else:
            # moden to send streaming data
            con.send(data)


#-------------------------------------------------------------------------


# client communication
class client_comms:
    
    # initialize constants and start client socket
    def __init__(self, ip, port):
        self.flag = False
        self.dict = {}
        self.num = 23
        self.char = '='
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((ip, int(port)))
        except:
            global_sv(self.char).print_out(64)
            print(f'[x] ADDRESS {ip}:{port} NOT REACHABLE: PLEASE SEEK\nFOR THE SERVER ADDRESS BY RUNNING <ifconfig / ip addr>')
            global_sv(self.char).print_out(64)
            os._exit(0)
        global_sv(self.char).print_out(self.num)
        print('[*] CONNECTED TO SERVER')
        global_sv(self.char).print_out(self.num)
        self.sock = sock

    # close client communication and program
    def close_socket(self):
        print('[*] SESSION TERMINATED')
        self.sock.close()
        os._exit(0)


#   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -

    # receive incoming data from the server
    def receive_data(self, code):
        sock = self.sock
        if code:
            # mode to receive static data
            length = int.from_bytes(sock.recv(4), byteorder='big')
            data = sock.recv(length).decode()
        else:
            # mode to receive streaming data
            data = sock.recv(4096)
        return data


    # send data to the server
    def send_data(self, data, code):
        sock = self.sock
        if code:
            # mode to send static data
            sock.send(len(data).to_bytes(4, byteorder='big'))
            sock.send(data.encode())
        else:
            # mode to send static data
            sock.send(data)


#-------------------------------------------------------------------------


# server utility program
class server_utility:

    # initialize constants
    def __init__(self):
        self.flag = True
        self.dict = {}

#   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -

    # receive file from the client
    def receive_file(self, file, size):
        size = int(size)
        received = 0
        with open(file, "wb") as open_file:
            while received < size:
                chunk = server_com.receive_data(code=False)
                if not chunk:
                    break
                open_file.write(chunk)
                self.flag = True
                received += len(chunk)

        if self.flag:
            return True
        else:
            return False

 #  -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -       

    # send file to the client
    def send_file(self, file, size):
        buffer = 4096
        size = int(size)
        received = 0
        with open(file, "rb") as open_file:
            while received < size:
                chunk = open_file.read(buffer)
                if not chunk:
                    break
                server_com.send_data(chunk, code=False)
                self.flag = True
                received += len(chunk)

        if self.flag:
            return True
        else:
            return False


#   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -


    # get working directory
    def current_directory(self):
        data = subprocess.getoutput('pwd')
        server_com.send_data(data, code=True)
        self.flag = True
        return self.flag


#   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -



    # get folder content
    def folder_content(self):
        data = subprocess.getoutput('ls -la')
        server_com.send_data(data, code=True)
        self.flag = True
        return self.flag


#   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -



    # execute command line
    def cli_exec(self, cli):
        cli = cli.replace('^*^*^', ' ')

        #process command line input
        if cli.startswith('cd') and cli != 'cd':
            try:
                # change directory to string after cd
                os.chdir(cli.split(' ')[1])
                self.flag = True
            except:
                return '0x51'
        elif cli == 'cd':
            try:
                # change directory to home directory
                os.chdir(os.path.expanduser('~'))
                self.flag = True
            except:
                return '0x51'
        else:
            try:
                # process command line
                data = subprocess.run(
                    cli,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    stdin=subprocess.DEVNULL,
                    timeout=0.5,
                    text=True
                )
                self.flag = True
            except subprocess.TimeoutExpired:
                # quit if process stuck
                return '0x51'

        if self.flag:
            return cli
        else:
            return '0x50'







#-------------------------------------------------------------------------



# client utility program
class client_utility:

    # initialize constants
    def __init__(self):
        self.flag = False
        self.dict = {}
        self.num = 23
        self.char = '='


    # receive file from the server
    def receive_file(self, file, size):
        size = int(size)
        received = 0
        with open(file, 'wb') as open_file:
            while received < size:
                chunk = client_com.receive_data(code=False)
                if not chunk:
                    break
                open_file.write(chunk)
                received += len(chunk)


                # progress bar calculation
                total = len(str(size))+1
                current_s_f = round(received/(1024 * 1024), 2)
                total_s_f = round(size/(1024 * 1024), 2)

                percentage_f = int((100 * received) / size)

                length_c = len(str(current_s_f))
                length_p = len(str(percentage_f))

                space_c_v = total - length_c
                space_p_v = 4 - length_p
                print(f'[!] RECEIVING: {current_s_f}{' '*space_c_v}of {total_s_f} | {percentage_f}{' '*space_p_v}of 100% ', end='\r', flush=True)

        print('')
        global_sv(self.char).print_out(self.num)
        print('[*] FILE RECEIVED')
        global_sv(self.char).print_out(self.num)


#   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -

    # send file to the server
    def send_file(self, file, size):
        buffer = 4096
        size = int(size)
        received = 0
        with open(file, 'rb') as open_file:
            while received < size:
                chunk = open_file.read(buffer)
                if not chunk:
                    break
                client_com.send_data(chunk, code=False)
                received += len(chunk)

                
                # progress bar calculation
                total = len(str(size))+1
                current_s_f = round(received/(1024 * 1024), 2)
                total_s_f = round(size/(1024 * 1024), 2)

                percentage_f = int((100 * received) / size)

                length_c = len(str(current_s_f))
                length_p = len(str(percentage_f))

                space_c_v = total - length_c
                space_p_v = 4 - length_p
                print(f'[!] SENDING: {current_s_f}{' '*space_c_v}of {total_s_f} | {percentage_f}{' '*space_p_v}of 100%', end='\r', flush=True)

        print('')
        global_sv(self.char).print_out(self.num)
        print('[*] FILE SENT')
        global_sv(self.char).print_out(self.num)



#   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -



    # receive working directory from the server
    def get_directory(self):
        wd = client_com.receive_data(code=True)
        length = len(wd)+self.num
        global_sv(self.char).print_out(length)
        print(f'[*] WORKING DIRECTORY: {wd}')
        global_sv(self.char).print_out(length)


#   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -


    # receive folder content from the server
    def folder_list(self):
        fd = client_com.receive_data(code=True)
        length = len(fd.splitlines()[3])
        global_sv(self.char).print_out(length)
        print('[*] FOLDER LIST:')
        print(fd)
        global_sv(self.char).print_out(length)



#-------------------------------------------------------------------------


# server relay for utility program
class server_relay:

    # initialize constants
    def __init__(self):
        self.flag = False
        self.dict = {}


    # check if file exist
    def check_file(self, file):
        if exists(file) and file:
            return True
        else:
            return False

    # get file size in bytes
    def file_size(self, file):
        with open(file, 'rb') as open_file:
            open_file.seek(0, 2)
            size = open_file.tell()
        return size

    # get current time in year month day hour minute second
    def time_log(self):
        current_time = datetime.datetime.now()
        current_time = current_time.strftime('%y:%m:%d %H:%M:%S')
        return current_time



#   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -

    # main relay 
    def relay(self, method, method1, method2):
 
        server = server_utility()

        if method == 'rf':
            if server.receive_file(method1, method2):
                print(f'[*] FILE :{method1}: RECEIVED @ {self.time_log()}')
            else:
                print(f'[x] RECEIVING FILE :{method1}: FAILED @ {self.time_log()}')
        elif method == 'sf':
            if self.check_file(method1):
                size = self.file_size(method1)
                server_com.send_data('0x54', code=True)
                server_com.send_data(str(size), code=True)
                if server.send_file(method1, size):
                    print(f'[*] FILE :{method1}: SENT @ {self.time_log()}')
                else:
                    print(f'[x] SENDING FILE :{method1}: FAILED @ {self.time_log()}')
            else:
                server_com.send_data('0x50', code=True)

        elif method == 'wd':
            if server.current_directory():
                print(f'[*] SENT CURRENT WD @ {self.time_log()}')
            else:
                print(f'[x] SENDING CURRENT WD FAILED @ {self.time_log()}')
        elif method == 'fc':
            if server.folder_content():
                print(f'[*] FOLDER CONTENT SENT @ {self.time_log()}')
            else:
                print(f'[x] SENDING FOLDER CONTENT FAILED @ {self.time_log()}')
        elif method == 'c':
            data = server.cli_exec(method1)
            if data == '0x50':
                print(f'[x] FAILED TO RECEIVE COMMAND  @ {self.time_log()}')
            elif data == '0x51':
                print(f'[x] FAILED TO EXECUTE COMMAND @ {self.time_log()}')
            else:
                print(f'[*] EXECUTED :{data}: @ {self.time_log()}')
        elif method == 'ex':
            global_sv('-').print_out(64)
            print(f'[*] CLIENT TERMINATED SESSION @ {self.time_log()}')
            global_sv('-').print_out(64)
            server_com.close_socket()




#   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -


    # process client query and relay
    def process_client(self):
        data = server_com.receive_data(code=True).split(' ')
        method = data[0]
        method1 = data[1]
        method2 = data[2]
        self.relay(method, method1, method2)


#-------------------------------------------------------------------------



# client relay for utility program
class client_relay:

    # initialize constants
    def __init__(self):
        self.flag = False
        self.dict = {}
        self.num = 23
        self.char = '-'


    # check if file exist
    def check_file(self, file):
        if exists(file) and file:
            return True
        else:
            return False

    # get file size in bytes
    def file_size(self, file):
        with open(file, 'rb') as file:
            file.seek(0, 2)
            size = file.tell()
        return size




    # constructing query for server and relay data
    def relay(self):

        client = client_utility()
        global_sv(self.char).print_out(self.num)
        option = input('[?]-OPTION [1-6]: ')
        global_sv(self.char).print_out(self.num)
        if option == '2':
            file_name = input('[S]FILE NAME: ')
            if self.check_file(file_name):
                split_f = file_name.split('/')
                file_name_s = split_f[-1] if split_f else file_name

                size = self.file_size(file_name)
                config = ('rf', file_name_s, size)
                construct = ' '.join(map(str, config))
                client_com.send_data(construct, code=True)
                client.send_file(file_name, size)
            else:
                print('[x] NO SUCH FILE')

        elif option == '1':
            file_name = input('[R]FILE NAME: ')
            split_f = file_name.split('/')
            file_name_c = split_f[-1] if split_f else file_name

            config = ('sf', file_name, True)
            construct = ' '.join(map(str, config))
            client_com.send_data(construct, code=True)
            check = client_com.receive_data(code=True)
            if check == '0x54':
                size = client_com.receive_data(code=True)
                client.receive_file(file_name_c, size)
            elif check == '0x50':
                print('[x] NO SUCH FILE')
            else:
                print('[x] FAILED SOCKET SYNC')

        elif option == '3':
            config = ('wd', True, True)
            construct = ' '.join(map(str, config))
            client_com.send_data(construct, code=True)
            client.get_directory()

        elif option == '4':
            config = ('fc', True, True)
            construct = ' '.join(map(str, config))
            client_com.send_data(construct, code=True)
            client.folder_list()

        elif option == '5':
            cli = input('[C]CLI: ').replace(' ', '^*^*^')
            config = ('c', cli, True)
            construct = ' '.join(map(str, config))
            client_com.send_data(construct, code=True)
            global_sv('=').print_out(self.num)
            print('[*] CLI SENT')
            global_sv('=').print_out(self.num)
        elif option == '6':
            config = ('ex', True, True)
            construct = ' '.join(map(str, config))
            client_com.send_data(construct, code=True)
            print('[*] SESSION TERMINATED')
            global_sv(self.char).print_out(self.num)
            client_com.close_socket()




#-------------------------------------------------------------------------
# starting program for server or client mode based on user choice
try:
    serv_clie = input('[?]SERVER[1] CLIENT[2]: ')
    # start server mode
    if serv_clie == '1':
        port = input('[?]PORT: ')
        server_com = server_comms(port)
        server_r = server_relay()

        while True:
            try:
                server_r.process_client()
            except KeyboardInterrupt:
                server_com.close_socket()
            except:
                server_com.close_socket()

    # start client mode
    elif serv_clie == '2':
        ip = input('[?]IP: ')
        port = input('[?]PORT: ')
        client_com = client_comms(ip, port)
        client_r = client_relay()
        # options for client
        list_command = '''
------OPTION----------?
[1].RECEIVE FILE      |
[2].SEND FILE         |
[3].WORKING DIRECTORY |
[4].FOLDER CONTENT    |
[5].CLI               |
[6].EXIT SESSION      |
----------------------?'''
        print(list_command)

        while True:
            try:
                client_r.relay()
            except KeyboardInterrupt:
                client_com.close_socket()
            except:
                client_com.close_socket()

    else:
        print('[x] INVALID OPTION')
except:
    os._exit(0)


#-------------------------------------------------------------------------


