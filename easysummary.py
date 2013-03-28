#!/usr/bin/python
# -*- coding: utf-8 -*-

from pymongo import Connection
from easylast import *

def connect_to_summary():
    connect = Connection("localhost",12345)
    db = connect["summary_mangas_shows"]
    return  db["summary"]


def find_summary(query):
    """ infos is the result of the function infos_of_name """
    collect_summary = connect_to_summary()
    doc_find = collect_summary.find(query)

    for doc in doc_find:
        print(doc["summary"])
    
def add_summary(info,summary):   

    info["summary"] = summary
    collect_summary = connect_to_summary()
    collect_summary.save(info)






