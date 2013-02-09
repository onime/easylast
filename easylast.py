#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import re
from lxml import etree

port_remote = 2345
host_remote = "192.168.0.101"
re_nseason_nep = "S([0-9]+)E([0-9]+)|([0-9]+)x([0-9]+)|([0-9]{3})"
parserHTML =  etree.HTMLParser( recover=True,encoding='utf-8')

def connect_remote():
    """ Return a socket connect to host_remote on port_remote """
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((host_remote,port_remote))

    return sock

def choose_bd(bd):
    """ Return a string who determine the argument in the command line
    the argument is DL or VU """
    arg = b" "    
    if bd == "DL":
        arg = b"-d"
    return arg

def find_real_name_in_bd(name,infos):

    """ Return the infos which correspond to the real name in the bd """    
    ret = None
    for info in infos:
        if re.search(name,info[0],re.IGNORECASE) != None :
            ret = info
    return ret


def read_last_xml(bd):

    """ Return the xml send by last_seen, the argument is DL or VU """
    sock = connect_remote()
    sock.sendall(b"last_seen "+choose_bd(bd) +b"-w \n")
    xml = sock.recv(4096).decode('utf-8')
    
    while re.search('root>',xml) == None and re.search('/>',xml) == None:
            xml +=sock.recv(4096).decode('utf-8')
    
    sock.close()       
    xml = xml.replace('\n','')

    return xml

def infos_last(type_infos,sep,bd):
    """ The function get the info in the bd
    Params
    type_infos -- can either be MANGA or SHOW or * 
    sep        -- is the separtor between the name in the bd
    bd         -- can be DL or VU 
    
    the function return a list of list of info  """

    root_xml = etree.fromstring(read_last_xml(bd))
    infos = root_xml.xpath("//info")
    list_infos = []
    for i in infos:
        i.attrib["name"] = i.attrib["name"].replace(".",sep)
        if i.attrib["type"] == type_infos:
            if type_infos == "SHOW":
                list_infos.append([i.attrib["name"],int(i.attrib["num_season"]),int(i.attrib["num_episode"])])
            elif type_infos == "MANGA":
                list_infos.append([i.attrib["name"],int(i.attrib["num_chap"])])
        elif type_infos == "*":
            list_infos.append([i.attrib["name"],int(i.attrib["num_chap"]),int(i.attrib["num_season"]),int(i.attrib["num_episode"])])
    return list_infos

def upd_last_manga(nom_manga,num_chap,bd):
    """ The function update a nom_manga to the num_chap in the bd  """ 
    list_infos = infos_last(type_info,".",bd)
    sock = connect_remote()

    manga_info = find_real_name_in_bd(nom_manga,list_infos)
    
    if manga_info == None:
        sock.close()
        return None

    if num_chap > manga_info[1]:
        num_chap = str(num_chap)
        sock.sendall(b"last_seen "+choose_bd(bd)+ b" -u "+manga_info[0].encode()+b" -c "+num_chap.encode() +b"\n")

    sock.close()

def upd_last_show(name_show,num_season,num_episode,bd):
    """ The function update a name_show to the num_season and num_episode in the bd  """ 
    list_show = infos_last("SHOW",".",bd)
    sock = connect_remote()

    show_info = find_real_name_in_bd(name_show,list_show)

    if show_info == None:
        sock.close()
        return None
    
    if num_season > show_info[2] or (num_season == show_info[2] and num_episode > show_info[1]):
        num_episode = str(num_episode)
        num_season = str(num_season)
        sock.sendall(b"last_seen "+choose_bd(bd)+b" -u "+show_info[0].encode() + b" -s "+num_season.encode() + b" -e " + num_episode.encode())

def incr_last(name,bd):
    """ The function incremente the name in the bd """
    infos = infos_last("*",".",bd)
    sock = connect_remote()

    infos = find_real_name_in_bd(name,infos)
    sock.sendall(b"last_seen "+choose_bd(bd) + b" -i "+infos[0].encode())

    sock.close()
    
def add_manga(name,chap,bd):
    """ The function add a manga name with the chap in the bd """
    sock = connect_remote()

    sock.sendall(b"last_seen "+choose_bd(bd) + b" -a "+name.encode()+ b" -c "+str(chap).encode())

    sock.close()

def add_show(name,season,episode,bd):
    """ The function add a show name with the season and episode in the bd """
    sock = connect_remote()
    
    sock.sendall(b"last_seen "+choose_bd(bd) + b" -a "+name.encode() + b" -s "+str(season).encode() + b" -e "+str(episode).encode())

    sock.close()

def suppr_info(name,bd):
    """ The function delete the line whith name in the bd """
    list_info = infos_last("*",".",bd)
    sock = connect_remote()

    infos = find_real_name_in_bd(name,list_info)

    if infos != None:
        sock.sendall(b"last_seen " +choose_bd(bd) + b" -x " + infos[0].encode())
                 
    sock.close()    

def format_number_zero(number_list):
    """ The function format correctly a the number in number_list and returns a str list correctly formated
    the list number_list can contains str or int, it adds a 0 to the number lesser than 10 """
    new_list = []
    for n in number_list:

        if int(n) < 10:
            new_list.append("0"+str(int(n)))
        else:
            new_list.append(str(n))

    return new_list

def parse_regex(res_regex):
    """ The function parse the regex to get the numero of the season and the numero of the episode
    Return a the num_season and the num_episode in a list or the num_chap"""
    if(res_regex.group(1) != None):
        num_season_cur = res_regex.group(1)
        num_episode_cur = res_regex.group(2)
    elif res_regex.group(3) != None:
        num_season_cur = res_regex.group(3)
        num_episode_cur = res_regex.group(4)
    else:
        return format_number_zero([res_regex.group(5)])
    
    return format_number_zero([num_season_cur,num_episode_cur])

def format_name(name,sep):
    """ The function format the name to be the name of the file 
    sep  -- is separator who will be replace by a '.' 
    Return a name separated by '.' and whith first letter of each word upper
    """
    name_f = '.'.join(word[0].upper() + word[1:] for word in name.lower().split(sep))    
    return name_f


__version__ = '0.1'
