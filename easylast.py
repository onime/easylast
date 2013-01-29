#!/usr/bin/python

import socket
import lxml
import re
from lxml import etree

port = 2345
host = "192.168.0.101"

def read_last_xml():

    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((host,port))
    
    sock.sendall(b"last_seen -d -w\n")
    xml = sock.recv(4096).decode('utf-8')
    
    while re.search('/root',xml) == None:
        xml +=sock.recv(4096).decode('utf-8')

    sock.close()
       
    xml = xml.replace('\n','')

    return xml

def infos_last_dl(type_infos,sep):
    
    root_xml = etree.fromstring(read_last_xml())
    infos = root_xml.xpath("//info")
    list_infos = []

    for i in infos:
        i.attrib["name"] = i.attrib["name"].replace(".",sep)
        if i.attrib["type"] == type_infos:
            list_infos.append([i.attrib["name"],int(i.attrib["num_chap"]),int(i.attrib["num_season"]),int(i.attrib["num_episode"])])

    return list_infos

def upd_last_manga_dl(nom_manga,num_chap):
    
    list_manga = infos_last_dl("MANGA",".")
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((host,port))

    for manga in list_manga:
        if re.search(manga[0],nom_manga,re.IGNORECASE) != None and num_chap > manga[1]:
            print(nom_manga + " "+ manga[0])
            num_chap = str(num_chap)
            sock.sendall(b"last_seen -d -u "+manga[0].encode()+b" -c "+num_chap.encode() +b"\n")
 
def format_number_zero(number_list):
    
    new_list = []
    for n in number_list:

        if int(n) < 10:
            new_list.append("0"+str(int(n)))
        else:
            new_list.append(str(n))

    return new_list


        

__version__ = '0.1'
