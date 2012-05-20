#!/usr/bin/env python
# -*- coding: utf-8 -*-

from check_util import *

class Regione:
    # iso
    # istat
    # ref (e.g. EMR)
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
                 "Targa": None,
                 "Codice ISO": "iso"}

        if dati["Grado amministrativo"] != '1':
            print "%s ha un grado amministrativo di %s" % (self.name_it, dati["Grado amministrativo"])
        del dati["Grado amministrativo"]

        if "Divisione amm grado 1" in dati:
            print "%s ha la regione: %s" % (self.name_it, dati["Divisione amm grado 1"])
            del dati["Divisione amm grado 1"]

        if "Divisione amm grado 2" in dati:
            print "%s ha la provincia: %s" % (self.name_it, dati["Divisione amm grado 2"])
            del dati["Divisione amm grado 2"]

        for k, v in dati.items():
            if mappa[k] is None:
                print "%s ha %s settato a %s" % (self.name_it, k, v)
            else:
                if v != self.__dict__[mappa[k]]:
                    print "%s ha %s diverso: %s / %s" % (self.name_it, k, v, self.__dict__[mappa[k]])

import csv

regioni = dict()

def read_regioni():
    r = csv.reader(open('regioni.csv', 'rb'), delimiter=';')
    headers = None
    for i, c in enumerate(r):
        if i == 0:
            headers = c
        else:
            if len(c) != len(headers):
                print "errore riga %d" % i+1
                break

            reg = Regione()
            for j in range(len(headers)):
                reg.__dict__[headers[j]] = c[j].decode('utf-8')
            regioni[reg.istat] = reg

def write_regioni():
    w = csv.writer(open('regioni2.csv', 'wb'), delimiter=';')
    whead = ['iso','istat','ref','name_it','name_de','name_fr','wiki']
    w.writerow(whead)
    for reg in sorted(regioni.values(), key = lambda a: a.istat):
        w.writerow(list(reg.__dict__[i].encode('utf-8') for i in whead))
