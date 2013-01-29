#!/usr/bin/python

from easylast import *

#upd_last_manga_dl("manga.test",121)

ns = "03"
ne = 10

(ns,ne) = format_number_zero([ns,ne])

print(ns+" "+ne)
