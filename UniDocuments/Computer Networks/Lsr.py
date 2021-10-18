#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 15:18:54 2019

@author: z5186797
"""

#TODO if return, just display alive ones, so I need to keep to send packet or when receive append to neighbor !!
#Key board interput make exception

import socket
from socket import AF_INET,SOCK_DGRAM
import sys
import time
import threading
import pickle
from collections import defaultdict

IP = "127.0.0.1"
UPDATE_INTERVAL = 1.0
ROUTE_UPDATE_INTERVAL = 5.0

class RP:
    def __init__(self,file_name):
        try:
            with open(file_name,'r') as f:
                data = [v.split() for v in f.readlines() if v != '\n']
        except FileNotFoundError:
            print('Sorry, there is no such file.')
            sys.exit()
        #print(data)
        self.name = data[0][0]
        self.identity = int(data[0][1])
        self.n_neighbor = int(data[1][0])
        self.neighbor = [data[i + 2][0] for i in range(self.n_neighbor)]
        print(self.neighbor)
        self.g_neighbor = self.neighbor.copy()
        #self.g_neighbor.append(self.name)
        self.g_map = defaultdict(list)
        self.dist = defaultdict()
        self.dist[self.name] = 0
        self.pred = defaultdict(str)
        self.pred[self.name] = "unk"
        self.hearbeat = {}
        self.timer = {}
        self.logouter = 0
        self.deadlist = []
        self.seq = 0
        self.ack = {}
        for i in range(self.n_neighbor):
            self.g_map[data[2 + i][0]] = [(data[2 + i][1]),int(data[2 + i][2])]
            self.dist[data[2 + i][0]] = (data[2 + i][1])
            self.pred[data[2 + i][0]] = "unk"
            self.hearbeat[self.neighbor[i]] = 0
        self.g_data = [(data[0][0], i, float(self.g_map[i][0])) for i in self.g_map if i != data[0][0]]
        self.graph = [(data[0][0], i, float(self.g_map[i][0])) for i in self.g_map if i != data[0][0]]
        self.o_map = self.g_map.copy()
        print(self.neighbor)
        #print(self.g_neighbor)
        print(self.g_map)
        
    def UDPServer(self):
        ServerSocket = socket.socket(AF_INET,SOCK_DGRAM)
        ServerSocket.bind((IP,self.identity))
        message = str(self.identity)
        message = message.encode()
        while 1:
            try:
                ServerSocket.settimeout(1.0)
                data,addr= ServerSocket.recvfrom(1024)
                data = pickle.loads(data)
                d_flag = data[0]
                data = data[1:]
                if d_flag == "logout":
                    if data[0] not in self.deadlist:
                        #print(data[0])
                        print(f"{data[0]} is logouted")
                        self.logouter = data[0]
                        self.remover()
                        msg = ["logout",self.logouter]
                        msg = pickle.dumps(msg)
                        for i in self.neighbor:
                            port_num = self.g_map[i][1]
                            ServerSocket.sendto(msg, (IP,port_num))
                else:
                    seq = data[0][1]
                    starter = data[0][0]
                    datagram = data[1:]
                    self.timer[d_flag] = time.time()
                    if starter in self.deadlist:
                        self.deadlist.remove(starter)
                        if starter in self.o_map:
                            self.g_map = self.o_map
                            self.neighbor.append(starter)
                            self.n_neighbor += 1
                    #print(len(self.timer),self.n_neighbor)
                    if len(self.timer) == self.n_neighbor:
                        for i in self.neighbor:
                            gap = time.time() - self.timer[i]
                            if gap > 5.0:
                                print(f"{i} is logouted")
                                self.logouter = i
                                self.remover()
                                msg = ["logout",self.logouter]
                                msg = pickle.dumps(msg)
                                for i in self.neighbor:
                                    port_num = self.g_map[i][1]
                                    ServerSocket.sendto(msg, (IP,port_num))

                    for i in datagram:
                        flag = 1
                        #print(i)
                        if i[0] not in self.deadlist and i[1] not in self.deadlist:
                            for j in self.graph:
                                if {i[0],i[1]} == {j[0],j[1]}:
                                    flag = 0
                            if flag == 1:
                                self.graph.append(i)
                            if i[0] not in self.g_neighbor and i[0] != self.name:
                                self.g_neighbor.append(i[0])
                                self.dist[i[0]] = 10000
                                self.pred[i[0]] = "unk"
                            if i[1] not in self.g_neighbor and i[1] != self.name:
                                self.g_neighbor.append(i[1])
                                self.dist[i[1]] = 10000
                                self.pred[i[1]] = "unk"
                    if starter not in self.ack:
                        self.ack[starter] = seq
                        send_data = [self.name] + data
                        send_data = pickle.dumps(send_data)
                        for i in self.neighbor:
                            if i != d_flag:
                                port_num = self.g_map[i][1]
                                ServerSocket.settimeout(1.0)
                                ServerSocket.sendto(send_data, (IP,port_num))
                    
                    else:
                        if self.ack[starter] >= seq:
                            pass
                        else:
                            send_data = [self.name] + data
                            send_data = pickle.dumps(send_data)
                            for i in self.neighbor:
                                if i != d_flag:
                                    port_num = self.g_map[i][1]
                                    ServerSocket.settimeout(1.0)
                                    ServerSocket.sendto(send_data, (IP,port_num))
                            self.ack[d_flag] = seq  
            except socket.timeout:
                print(f'time out')
                #self.hearbeat[d_flag] = self.hearbeat[d_flag] + 1
                #print(f"sender is {d_flag} hearbeat is {self.hearbeat[d_flag]}")
                #ServerSocket.close()
                
    def UDPClient(self):
        ServerSocket = socket.socket(AF_INET,SOCK_DGRAM)
        #bload cast use for loop
        while 1:
            try:
                send_data = self.g_data
                send_data = [self.name] + [(self.name,self.seq)] + send_data
                send_data = pickle.dumps(send_data)
                for i in self.neighbor:
                    port_num = self.g_map[i][1]
                    ServerSocket.settimeout(1.0)
                    ServerSocket.sendto(send_data, (IP,port_num))
                self.seq += 1
                time.sleep(UPDATE_INTERVAL)
                        
            except socket.timeout:
                print(f'time out')
                #ServerSocket.close()
            
    def dijkstraSSSP(self):
        while 1:
            for j in self.g_neighbor:
                self.pred[j] = "unk"
                self.dist[j] = 10000
            c_neighbor = self.g_neighbor.copy()
            c_neighbor.append(self.name)
            while c_neighbor != []:
                #make tmp dic each time
                tmp_dist = {}
                for j in c_neighbor:
                    tmp_dist[j] = self.dist[j]
                source = min(tmp_dist,key = tmp_dist.get)
                for i in self.graph:
                    if i[2] != 10000 and source == i[0]:
                        #print(self.graph)
                        if self.dist[source] + i[2] < self.dist[i[1]]:
                            self.dist[i[1]] = i[2] + self.dist[source]
                            self.pred[i[1]] = source
                    elif i[2] != 10000 and source == i[1]:
                        if self.dist[source] + i[2] < self.dist[i[0]]:
                            self.dist[i[0]] = i[2] + self.dist[source]
                            self.pred[i[0]] = source
                c_neighbor.remove(source)
            print(f"I am Router {self.name}")
            for k in self.g_neighbor:
                path = k
                tmp = k
                p = 0
                while p != self.name:
                    p = self.pred[tmp]
                    path = p + path
                    tmp = p
                self.dist[k] = round(self.dist[k],1)
                print(f"Least cost path to router {k}: {path} and the cost is {self.dist[k]}")
            time.sleep(ROUTE_UPDATE_INTERVAL)
            print(self.deadlist)
            #self.deadlist = []
            #print(self.deadlist)
            
    def remover(self):
        print(f"remove all {self.logouter} information")
        #remove form self.neighbor self.g_neighbor self.g_map self.dist self.dist
        self.deadlist.append(self.logouter)
        if self.logouter in self.neighbor:
            self.n_neighbor -= 1
            self.neighbor.remove(self.logouter)
        if self.logouter in self.g_neighbor:
            self.g_neighbor.remove(self.logouter)
        if self.logouter in self.g_map:
            del self.g_map[self.logouter]
        if self.logouter in self.timer:
            del self.timer[self.logouter]
        del self.pred[self.logouter]
        del self.dist[self.logouter]
        del self.ack[self.logouter]
        self.graph = [x for x in self.graph if x[0] != self.logouter and x[1] != self.logouter]
        self.g_data = [x for x in self.g_data if x[0] != self.logouter and x[1] != self.logouter]

        

if __name__ == "__main__":
    rp = RP(sys.argv[1])
    thread_1 = threading.Thread(target = rp.UDPServer,args = ())
    thread_2 = threading.Thread(target = rp.UDPClient,args = ())
    thread_3 = threading.Thread(target = rp.dijkstraSSSP,args = ())
    thread_1.start()
    thread_2.start()
    thread_3.start()
