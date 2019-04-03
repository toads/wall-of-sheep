#!/usr/bin/python
from http.server import HTTPServer，BaseHTTPRequestHandler
from scapy.all import *
import threading
import json


global qq_dict
qq_dict=dict()
IFACE = 'wlan0'
PORT_NUMBER = 8080
host = ('0.0.0.0', 8881)        

def prn(pkt):
    t=''
    qq=[]
    qq_lib=[]
    raw_data = pkt[Raw].load
    # filter out qq number
    for x in raw_data:
        if x <= ord('9') and x >= ord('0'):
            t+=chr(x)
        elif 6<len(t)<11:
            qq.append(t)
        elif len(t)<6:
            t=''
    # conter 
    if qq:
        if qq[0] not in qq_lib:
            qq_lib.append(qq[0])
            qq_dict.update({qq[0]:qq_dict.get(qq[0],0)+qq_lib.count(qq[0])})
            print(qq_dict)
            

def foo(x):
    if x.haslayer(IP) and x.haslayer(TCP) and x.haslayer(Raw):
        if x[TCP].sport == 14000 or x[TCP].dport == 14000 or x[TCP].sport == 8080 or x[TCP].dport == 8080:
            return x
    return None


sniff_thread = threading.Thread(target=sniff,kwargs={'iface':IFACE,'prn':prn,'lfilter':foo})
sniff_thread.setDaemon(True)
sniff_thread.start()



class Resquest(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        li = []
        if qq_dict:
            for i in qq_dict.keys():
                li.append({"qq":"{}".format(i)})
            self.wfile.write((json.dumps({'data':(li)})).encode('utf-8'))

            
server = HTTPServer(host, Resquest)
print("Starting server, listen at: %s:%s" % host)
server.serve_forever()
