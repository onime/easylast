#!/usr/bin/python

import configparser
from easylast import *

config = config = configparser.ConfigParser()
config.read(path_file_info+".DL")

sections = config.sections()

#print(infos_last("SHOW"," ","DL"))
#print(infos_last("MANGA"," ","DL"))

#upd_last_manga("One.Piece",89,"DL")
#upd_last_show("American.Dad",5,10,"DL")
#incr_last("Bleach","DL")
#add_manga("manga_test",555,"DL")
suppr_info("manga_TEST","DL")
