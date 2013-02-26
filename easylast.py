#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import re
from lxml import etree
import configparser
import os

path_file_info = "/home/yosholo/.config/utils/infos_last"
regex_infos = "S([0-9]+)E([0-9]+)|([0-9]+)x([0-9]+)|([0-9]{3})"
parserHTML =  etree.HTMLParser( recover=True,encoding='utf-8')

def write_info(info,dl_or_seen,cmd="ADD"):

    info_config = configparser.ConfigParser()
    info_config.read(path_file_info+"."+dl_or_seen)
    
    if cmd == "ADD":
        if len(info) == 2:
            info_config["MANGA"][info[0]] = str(info[1])
        else:
            info_config["SHOW"][info[0]] = str(info[1])+","+str(info[2])
    elif cmd == "DEL":
        if len(info) == 2:
            del(info_config["MANGA"][info[0]])
        else:
            del(info_config["SHOW"][info[0]])

    with open(path_file_info+"."+dl_or_seen, 'w') as configfile:
        info_config.write(configfile)

    
def find_info(name,infos):

    """ Return the infos which correspond to the real name in the bd """    
    ret = None
    for info in infos:
        if re.search(name,info[0],re.IGNORECASE) != None :
            ret = info
    return ret

def infos_last(type_infos,sep,dl_or_seen):

    info_config = configparser.ConfigParser()
    info_config.read(path_file_info+"."+dl_or_seen)
    
    ret = []
    
    for section in info_config.sections():
        
        for k in info_config[section].keys():
            if section == type_infos == "SHOW":
                
                num = info_config[section][k].split(',')
                elem = [k.replace('.',sep),int(num[0]),int(num[1])]
                ret.append(elem)

            if section == type_infos == "MANGA":
                ret.append([k.replace('.',sep),int(info_config[section][k])])
    return ret  


def upd_last_manga(nom_manga,num_chap,ext_config):
    """ The function update a nom_manga to the num_chap in the config_file.ext_config """ 
    
    list_infos = infos_last("MANGA",".",ext_config)
    manga_info = find_info(nom_manga,list_infos)
    
    if manga_info == None:
        return False
    
    manga_info[1] = str(num_chap)
    write_info(manga_info,ext_config)
    
    return True

def upd_last_show(name_show,num_season,num_episode,ext_config):
    """ The function update a name_show to the num_season and num_episode in the bd  """ 
    list_show = infos_last("SHOW",".",ext_config)
    show_info = find_info(name_show,list_show)

    if show_info == None:
        return False
    
    show_info[2] = str(num_episode)
    show_info[1] = str(num_season)
    write_info(show_info,ext_config)

def incr_last(name,ext_config):
    """ The function incremente the name in the bd """
    
    infos_all = infos_last("MANGA",".",ext_config) + infos_last("SHOW",".",ext_config)

    infos = find_info(name,infos_all)

    if len(infos) == 3:
        infos[2]+=1
    if len(infos) == 2:
        infos[1]+=1
    write_info(infos,ext_config)
    
def add_manga(name,chap,bd):
    """ The function add a manga name with the chap in the bd """
    write_info([name,chap],bd)
    

def add_show(name,season,episode,bd):
    """ The function add a show name with the season and episode in the bd """
    write_info([name,season,episode],bd)

def suppr_info(name,bd):
    """ The function delete the line whith name in the bd """
    list_info = infos_last("MANGA",".",bd)+infos_last("SHOW",".",bd)
    
    infos = find_info(name,list_info)
    
    write_info(infos,bd,"DEL")

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

def infos_of_name(name,ext):

    for info in  infos_last("MANGA",".",ext) + infos_last("SHOW",".",ext):
        if re.search(name,info[0],re.IGNORECASE):
            return info
    print(name,"Nothing to do")
    exit(0)

def format_SXXEXX(num_season,num_episode):
    num = format_number_zero([num_season,num_episode])
    return "S"+num[0]+"E"+num[1]

def send_inform(message):
    
    path_fifo = "/home/yosholo/.config/utils/.inform_fifo"
    if not os.path.exists(path_fifo):
        os.mkfifo(path_fifo)

    try:
        fifo = os.open(path_fifo,os.O_WRONLY | os.O_NONBLOCK)
        os.write(fifo,message.encode("utf-8"))
    except:
        print("There's no process to read the info")

def read_inform():

    path_fifo = "/home/yosholo/.config/utils/.inform_fifo"
    if not os.path.exists(path_fifo):
        os.mkfifo(path_fifo)

    fifo = os.open(path_fifo,os.O_RDONLY)
    message = os.read(fifo,4096)
    
    return message

__version__ = '0.2'
