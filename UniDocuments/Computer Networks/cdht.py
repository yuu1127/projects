#z5186797 Python ver3.7
import socket
from socket import AF_INET,SOCK_DGRAM,SOCK_STREAM
import sys
import time
import random
import struct
import threading
import pickle
global hash_value
import math
#any time delete procesor

IP = "127.0.0.1"
timeout = 1.0
frequency = 5.0


class DHT:
    #make variable
    def __init__(self):
        self.identity = int(sys.argv[1])
        self.s_peer = []
        self.s_peer.append(int(sys.argv[2]))
        self.s_peer.append(int(sys.argv[3]))
        self.pre = []
        self.MSS = int(sys.argv[4])
        self.drop_p = float(sys.argv[5])
        self.q_flag = 0
        self.k1_flag = 0
        self.k2_flag = 0
        self.d_flag = 0
        self.seq = 0
        self.ack = 0
        self.ACK_flag = 0
        self.start_time = 0

    def Initialization(self):
        try:
            if self.drop_p < 0 or self.drop_p > 1:
                raise ValueError
            if self.identity < 0 or self.identity > 255:
                raise ValueError
        except ValueError:
            print('Sorry,input file does not store valid data.')

    def TCPServer(self):
        #inside TCP server use client call
        ServerSocket = socket.socket(AF_INET,SOCK_STREAM)
        ServerSocket.bind((IP,50000 + self.identity))
        ServerSocket.listen(5)
        #print('TCP Server Start')
        while 1:
            conn,addr = ServerSocket.accept()
            #print("aaaaa")
            data = conn.recv(1024).decode()
            #if data:
                #print(data)
                #print(f"before {self.s_peer[0]} {self.s_peer[1]}")
            data = data.split(" ")
            if data[0] == "quit":
                print(f"Peer {data[1]} will depart from the network")
                data[1] = int(data[1])
                data[2] = int(data[2])
                data[3] = int(data[3])
                if self.s_peer[0] == data[1]:
                    self.s_peer[0] = data[2]
                    self.s_peer[1] = data[3]
                elif self.s_peer[1] == data[1]:
                    self.s_peer[1] = data[2]
                print(f"My first successor is now peer {self.s_peer[0]}")
                print(f"My second successor is now peer {self.s_peer[1]}")

            if data[0] == "kill":
                #print("aaaaa")
                message = str(self.s_peer[0])
                #print(f"kill send {self.s_peer[0]}")
                message = message.encode()
                conn.send(message)

            # data[1] is hash_value data[2] where request from
            if data[0] == "find":
                #print("ffffff")
                if self.file_check(int(data[2]),int(data[3])):
                    print(f"File {data[2]} is here.")
                    print(f"A response message, destined for peer {data[1]}, has been sent.")
                    data[0] = "found"
                    data[3] = str(self.identity)
                    data_content = str(data[1]) + " " + str(data[2])
                    data = data[0] + " " + data[1] + " " + data[2] + " " + data[3]
                    self.FoundTCPClient(data)
                    print("We now start sending the file .......")
                    self.start_time = time.time()
                    self.FileUDPClient(data_content)
                    print("The file is sent.")
                    #message = str(self.s_peer[0])
                    #print(f"kill send {self.s_peer[0]}")
                    #message = message.encode()
                    #conn.send(message)
                else:
                    print(f"File {data[2]} is not stored here.")
                    print(f"File request message has been forward to my successor.")
                    data[3] = str(self.identity)
                    data = data[0] + " " + data[1] + " " + data[2] + " " + data[3]
                    self.FindTCPClient(data)

            if data[0] == "found":
                print(f"Received a response message from peer {data[3]}, which has the file {data[2]}.")
                print("We now start receiving the file .......")
                self.start_time = time.time()
                print("The file is received.")
            #conn.send(data)

    def TCPDropClient(self,port):
        ServerSocket = socket.socket(AF_INET,SOCK_STREAM)
        #ServerSocket.bind((IP,50000 + self.identity))
        #message = "Hello This is TCPClient"
        #message = message.encode()
        request = "quit"
        #ServerSocket.connect((IP,50000 + self.identity))
        #ServerSocket.send(message)
        #print(f"send quit;{port}")
        ServerSocket.connect((IP,50000 + port))
        message = request + " " + str(self.identity) + " " + str(self.s_peer[0]) + " " + str(self.s_peer[1])
        message = message.encode()
        ServerSocket.send(message)
        ServerSocket.close()
                #self.pre = []

        #data = ServerSocket.recv(1024)
        #ServerSocket.close()
        #print(f"success receive {data}")
        #print("file not here")
    def KillTCPClient(self,port):
        ServerSocket = socket.socket(AF_INET,SOCK_STREAM)
        request = "kill"
        #print(f"send quit;{port}")
        ServerSocket.connect((IP,50000 + port))
        message = request + " " + str(self.identity)
        message = message.encode()
        ServerSocket.send(message)
        new_s = ServerSocket.recv(1024).decode()
        #print(new_s)
        #print(f'From Server:{new_s}')
        self.s_peer[1] = int(new_s)
        ServerSocket.close()

    def FindTCPClient(self,message):
        ServerSocket = socket.socket(AF_INET,SOCK_STREAM)
        #h_value = h_value.split(" ")
        #request = "find"
        #print(f"send find;{self.s_peer[0]}")
        ServerSocket.connect((IP,50000 + self.s_peer[0]))
        #message = request + " " + str(self.identity) + " " + str(self.identity) + " " + str(h_value)
        #message[3] = h_content + " " + str(self.identity)
        message = message.encode()
        ServerSocket.send(message)
        ServerSocket.close()


    def FoundTCPClient(self,message):
        ServerSocket = socket.socket(AF_INET,SOCK_STREAM)
        port = int(message.split(" ")[1])
        ServerSocket.connect((IP,50000 + port))
        message = message.encode()
        ServerSocket.send(message)
        ServerSocket.close()

    def UDPServer(self):
        ServerSocket = socket.socket(AF_INET,SOCK_DGRAM)
        ServerSocket.bind((IP,50000 + self.identity))
        message = str(self.identity)
        message = message.encode()
        file_name = "received_file.pdf"
        while 1:
            data,addr= ServerSocket.recvfrom(1024)
            #print(type(data))
            #print(len(data))
            if len(data) < 10:
                #print(data[0])
                data1 = data.decode()
                print(f'A ping request message was received from Peer {data1}.')
                ServerSocket.sendto(message,addr)
                if len(self.pre) < 2 and int(data1) not in self.pre:
                    self.pre.append(int(data1))
                if len(self.pre) == 2 and int(data1) not in self.pre:
                    self.pre = []
                    #self.pre = sorted(self.pre)
                #print(self.pre)
            else:
                request_log = open("requesting_log.txt",'a+')
                #print(len(data))
                data = pickle.loads(data)
                #print(data)
                if data[0] == "f_ack" and data[2] == self.ack:
                    with open(file_name.strip(),'ab') as f:
                        #print(data[:20])
                        #print(data)
                        f.write(data[4])
                    event = "rcv"
                    timen = str(time.time() - self.start_time)
                    seqn = str(self.seq)
                    num_data = str(len(data[4]))
                    ackn = str(self.ack)
                    log_data = event + " " + timen + " " + seqn + " " + num_data + " " + ackn + "\n"
                    request_log.write(log_data)

                    #data[0] = "ack"
                    data = ['ack',self.seq,self.ack,self.MSS]
                    data = pickle.dumps(data)
                    ServerSocket.sendto(data,addr)
                    event = "Snd"
                    timen = str(time.time() - self.start_time)
                    seqn = str(self.seq)
                    num_data = str(len(data))
                    ackn = str(self.ack)
                    log_data = event + " " + timen + " " + seqn + " " + num_data + " " + ackn + "\n"
                    request_log.write(log_data)
                    self.seq += 1
                    self.ack += 1
                request_log.close()


    def UDPClient(self):
        ServerSocket = socket.socket(AF_INET,SOCK_DGRAM)
        message = str(self.identity)
        message = message.encode()
        #ServerSocket.connect((IP, 50000 + self.identity))
        while 1:
            #ServerSocket.sendto(message, (IP,50000 + self.s_peer2))
            try:
                port_num1 = self.s_peer[0]
                ServerSocket.settimeout(10.0)
                ServerSocket.sendto(message, (IP,50000 + port_num1))
                #time.sleep(1.0)
                data1,addr= ServerSocket.recvfrom(1024)
                if data1:
                    data1 = data1.decode()
                    print(f'A ping response message was received from Peer {data1}.')
                    self.k1_flag = 0
            except socket.timeout:
                #print(f'time out')
                self.k1_flag += 1

            try:
                port_num2 = self.s_peer[1]
                ServerSocket.settimeout(10.0)
                ServerSocket.sendto(message, (IP,50000 + port_num2))
                #time.sleep(1.0)
                data2,addr= ServerSocket.recvfrom(1024)
                if data2:
                    data2 = data2.decode()
                    print(f'A ping response message was received from Peer {data2}.')
                    self.k2_flag = 0
            except socket.timeout:
                #print(f'time out')
                self.k2_flag += 1

            if(self.k1_flag > 2):
                print(f"Peer {self.s_peer[0]} is no longer alive")
                self.s_peer[0] = self.s_peer[1]
                print(f'My first successor is now peer {self.s_peer[0]}')
                self.KillTCPClient(self.s_peer[0])
                print(f"My second successor is now peer {self.s_peer[1]}")

            if(self.k2_flag > 2):
                print(f"Peer {self.s_peer[1]} is no longer alive")
                #self.s_peer[0] = self.s_peer[1]
                print(f'My first successor is now peer {self.s_peer[0]}')
                self.KillTCPClient(self.s_peer[0])
                print(f"My second successor is now peer {self.s_peer[1]}")

            if self.q_flag == 1:
                ServerSocket.close()
                break
            time.sleep(5.0)

    #data = d_port number + file_name
    def FileUDPClient(self,message):
        message = message.split(" ")
        #print(message)
        FileSocket = socket.socket(AF_INET,SOCK_DGRAM)
        file_name = message[1] + ".pdf"
        with open(file_name,"rb") as f:
                file_data = f.read()
                f.close()
        #self.start_time = time.time()
        responding_log = open("responding_log.txt",'a+')
        times = math.ceil(len(file_data)/self.MSS)

        while times:
            random_p = random.uniform(0,1)
            try:
                #print(times)
                if self.ACK_flag == 0:
                    FileSocket.settimeout(1.0)
                    if self.d_flag == 0:
                        if(len(file_data) > self.MSS):
                            send_data = file_data[0:self.MSS]
                            file_data = file_data[self.MSS:]
                        else:
                            send_data = file_data
                    #add_mss = str(seq) + " " + str(ack) + " " + str(self.MSS)
                    #send_data = add_mss.decode() + send_data
                        data_size = len(send_data)
                        send_data = ['f_ack',self.seq,self.ack,self.MSS,send_data]
                        send_data = pickle.dumps(send_data)
                    #random de okurukadouka murinara drop
                    if random_p > self.drop_p:
                        FileSocket.sendto(send_data, (IP,50000 + int(message[0])))
                        event = "Snd"
                        timen = str(time.time() - self.start_time)
                        seqn = str(self.seq)
                        num_data = str(data_size)
                        ackn = str(self.ack)
                        log_data = event + " " + timen + " " + seqn + " " + num_data + " " + ackn + "\n"
                        responding_log.write(log_data)

                    else:
                        event = "drop"
                        timen = str(time.time() - self.start_time)
                        seqn = str(self.seq)
                        num_data = str(data_size)
                        ackn = str(self.ack)
                        log_data = event + " " + timen + " " + seqn + " " + num_data + " " + ackn + "\n"
                        responding_log.write(log_data)
                        self.ACK_flag = 1
                        self.d_flag = 1

                data1,addr= FileSocket.recvfrom(1024)
                data1 = pickle.loads(data1)
                #print(data1)
                    #self.ACK_flag = 1
                if data1[0] == "ack" and data1[2] == self.ack:
                    self.ACK_flag = 0
                    event = "rcv"
                    timen = str(time.time() - self.start_time)
                    seqn = str(self.seq)
                    num_data = str(len(data1))
                    ackn = str(self.ack)
                    log_data = event + " " + timen + " " + seqn + " " + num_data + " " + ackn + "\n"
                    responding_log.write(log_data)
                    self.seq += 1
                    self.ack += 1
                    self.d_flag = 0
                    times -= 1

                else:
                    continue
            except socket.timeout:
                #rtm
                event = "RTX"
                timen = str(time.time() - self.start_time)
                seqn = str(self.seq)
                num_data = str(data_size)
                ackn = str(self.ack)
                log_data = event + " " + timen + " " + seqn + " " + num_data + " " + ackn + "\n"
                responding_log.write(log_data)
                self.ACK_flag = 0
                self.d_flag = 1
        responding_log.close()
        FileSocket.close()
        #ServerSocket.connect((IP, 50000 + self.identity))

    def input_request(self):
        #file ha list ni site okuru
        global hash_value
        #int num_kill = 0
        while True:
            request = input("")
            request = request.split(" ")
            #self.hash_function(int(request[1]))
            if request[0] == "request":
                try:
                    if int(request[1]) >= 0 and len(request[1]) == 4:
                        print(f"File request message for {request[1]} has been sent to my successor.")
                        h_value = int(request[1])
                        #print(h_value)
                        file_content = "find" + " " + str(self.identity) + " " + str(h_value) + " " + str(self.identity)
                        self.FindTCPClient(file_content)

                    else:
                        print(f"invalid file {request[1]}")
                except:
                    print(f"invalid file {request[1]}")
                #self.TCPClient(self.s_peer1)
            elif request[0] == "quit":
                #TCPClient(port,messagenisurubeki)
                self.TCPDropClient(self.pre[0])
                self.TCPDropClient(self.pre[1])
                self.q_flag = 1
                #self.TCPClient(request[0])
                #self.TCPClient(self.s_peer1)
                #self.TCPClient(self.s_peer2)

            #time.sleep(15)
    def hash_function(self,num):
        global hash_value
        hash_value = num % 256
        return hash_value

    def file_check(self,h_value,p_identity):
        h_value = self.hash_function(h_value)
        if self.identity < p_identity and p_identity < h_value:
            return True
        elif p_identity < h_value and h_value <= self.identity:
            return True
        else:
            return False


if __name__ == "__main__":
    ping = DHT()
    thread_1 = threading.Thread(target = ping.UDPServer,args = ())
    thread_2 = threading.Thread(target = ping.UDPClient,args = ())
    #thread_3 = threading.Thread(target = ping.UDPClient,args = (ping.s_peer2,))
    thread_3 = threading.Thread(target = ping.input_request,args = ())
    thread_4 = threading.Thread(target = ping.TCPServer,args = ())
    #thread_5 = threading.Thread(target = ping.TCPClient,args = (None,))
    thread_1.start()
    thread_2.start()
    thread_3.start()
    thread_4.start()
    #thread_5.start()
    #thread_4.start()
   #thread_1.join()
    #tread_2.join()
   #thread_3.join()
