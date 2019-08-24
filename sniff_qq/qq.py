# ！/usr/bin/env python3
# -*- coding:utf-8 -*-
# !/usr/bin/python
from scapy.all import *
from sniff_qq.channels import set_channel
import sqlite3
import re

## 建立数据库
con = sqlite3.connect('qq_id.sqlite3')


def init_db():
    con.execute('CREATE TABLE QQ\n'
                 '             (ID INT PRIMARY KEY     NOT NULL,\n'
                 '             COUNT INT,\n'
                 '             TIMESTAMP DATETIME DEFAULT CURRENT_TIMESTAMP\n'
                 '             );')



def update(qq):
    qq = int(qq)
    print("qq:", qq)
    con = sqlite3.connect('qq_id.sqlite3')
    cur = con.cursor()
    cur.execute('SELECT * FROM QQ WHERE ID=?', (qq,))
    qq_record = cur.fetchone()
    print('qq_record: ', qq_record)
    if qq_record:
        # 更新时间\
        count = qq_record[1]
        con.execute("UPDATE QQ SET COUNT = ? WHERE ID = ?", (count + 1, qq,))
    else:
        con.execute("INSERT INTO QQ(ID,COUNT) VALUES (?,1)", (qq,))
    print(qq)
    
    con.commit()


def prn(pkt):
    raw_data = str(pkt)
#    print(pkt)
    # filter out qq number
    pattern = re.compile(r'\d{7,10}')
    try:
        qq = pattern.findall(raw_data)[0]
        update(qq)
    except IndexError:
        pass


"""
BFP 封包
https://serverfault.com/questions/217605/how-to-capture-ack-or-syn-packets-by-tcpdump
"""
bfp = 'tcp[tcpflags]&(tcp-push|tcp-ack) != 0 || tcp src port 8080 || tcp dst port 8080'
# bfp = 'tcp src port 8080 || tcp dst port 8080'

iface = ['wlan1', 'wlan2', 'wlan0']
channel = [1, 6, 11]


def start_sniffer():
    print('star_sniffer')
    set_channel(iface, channel)
    # offline_pcap = 'qq.pcap'
    # sniff(offline='qq.pcap',filter=bfp, prn=prn)
    sniff_thread = threading.Thread(target=sniff, kwargs={'iface': iface, 'prn': prn, 'filter': bfp, 'monitor': True})
    # sniff_thread = threading.Thread(target=sniff, kwargs={'offline': offline_pcap, 'prn': prn, 'filter': bfp})
    sniff_thread.daemon = True
    sniff_thread.start()

# init_db(conn)
