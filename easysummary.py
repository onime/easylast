#!/usr/bin/python
# -*- coding: utf-8 -*-

from pymongo import Connection
from easylast import *

def connect_to_summary():
    connect = Connection("localhost",12345)
    db = connect["summary_mangas_shows"]
    return  db["summary"]


def find_summary(name):
    """ infos is the result of the function infos_of_name """
    
    print(summary.find_one({"name_manga":"/"+name+"/i"}))

def make_contrainst(infos):
    if(is_manga(infos)):
       name = "name_manga"
       num = "num_chap"       

def add_summary(info,summary):
#    info["summary"] = "gros fuck"
    doc = {}
    doc["name"] = info["name"]
    hash_num = info["num"]

    for k,h in hash_num.items():
        doc[k] = h

    print(doc)

info = infos_of_name("how.i.met.your","VU")

add_summary(info,"grodfgfsdhdfs")


print(summary.find_one())
