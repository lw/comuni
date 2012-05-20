#!/usr/bin/env python
# -*- coding: utf-8 -*-

from check_util import *

from check_regioni import *

class Provincia:
    # iso
    # istat
    # ref (e.g. BO)
    # reg (istat)
    # name-it
    # name-de
    # name-fr
    # wiki

    def check_wiki(self):
        dati = getWiki(self.wiki)

        if not dati:
            print "%s NON ha una pagina wiki!!" % self.name_it
            return

        mappa = {"Nome": "name_it",
                 "Codice statistico": "istat",
                 "Codice catastale": None,
                 "Targa": 'ref',
                 "Codice ISO": "iso"}

        if dati["Grado amministrativo"] != '2':
            print "%s ha un grado amministrativo di %s" % (self.name_it, dati["Grado amministrativo"])
        del dati["Grado amministrativo"]

        if "Divisione amm grado 1" in dati:
            if regioni[self.reg].name_it != dati["Divisione amm grado 1"]:
                print "%s ha la regione sbagliata: %s / %s" % (self.name_it, dati["Divisione amm grado 1"], regioni[self.reg].name_it)
            del dati["Divisione amm grado 1"]

        if "Divisione amm grado 2" in dati:
            print "%s ha la provincia: %s" % (self.name_it, dati["Divisione amm grado 2"])
            del dati["Divisione amm grado 2"]

        for k, v in dati.items():
            if mappa[k] is None or mappa[k] not in self.__dict__:
                print "%s ha %s settato a %s" % (self.name_it, k, v)
            else:
                if v != self.__dict__[mappa[k]]:
                    print "%s ha %s diverso: %s / %s" % (self.name_it, k, v, self.__dict__[mappa[k]])

import csv

province = dict()

def read_province():
    r = csv.reader(open('province.csv', 'rb'), delimiter=';')
    headers = None
    for i, c in enumerate(r):
        if i == 0:
            headers = c
        else:
            if len(c) != len(headers):
                print "errore riga %d" % i+1
                break

            pro = Provincia()
            for j in range(len(headers)):
                pro.__dict__[headers[j]] = c[j].decode('utf-8')
            province[pro.istat] = pro

def write_province():
    w = csv.writer(open('province2.csv', 'wb'), delimiter=';')
    whead = ['iso','istat','ref','reg','name_it','name_de','name_fr','wiki']
    w.writerow(whead)
    for pro in sorted(province.values(), key = lambda a: a.istat):
        w.writerow(list(pro.__dict__[i].encode('utf-8') for i in whead))
