#!/usr/bin/python
from http.server import HTTPServer, BaseHTTPRequestHandler
from scapy.all import *
import scapy_http.http as http
import threading
# import socket
import json
global qq_dict
import json
qq_dict=dict()
# qq_dict={'1285870531': 344035, '1247923389': 276, '3337250176': 2485, '1476515122': 3, '905038020': 36585, '9050380208': 300, '9050380209': 3, '9050380203': 1, '1292653345': 91, '1922313484': 15, '436058754': 15753, '961702947': 105, '1743468744': 105, '977348018': 133386, '2146171956': 10, '9773480184': 1, '2629249493': 132355, '7468271526': 1, '746827152': 3, '435077898': 136, '2441626919': 666, '3141775021': 180901, '849725403': 51360, '8497254035': 1176, '1776091942': 36, '1099147431': 406, '3388078568': 2278, '1796520408': 28, '366135188': 561, '3661351886': 6, '758832720': 21, '1017697157': 595, '895543892': 15400, '1137621610': 36046, '1044535234': 15, '5013169929': 66, '3292507': 1}

#qq_dict={'1343267422':'321213','3213213':'','1099147431':'','455774025':''}
PORT_NUMBER = 8080
host = ('0.0.0.0', 8881)

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
        return 



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
iface='wlan0'
sniff_thread = threading.Thread(target=sniff,kwargs={'iface':iface,'prn':prn,'lfilter':foo})
sniff_thread.setDaemon(True)
sniff_thread.start()


server = HTTPServer(host, Resquest)
print("Starting server, listen at: %s:%s" % host)
server.serve_forever()
