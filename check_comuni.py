#!/usr/bin/env python
# -*- coding: utf-8 -*-

from check_util import *

from check_regioni import *
from check_province import *

class Comune:
    # istat
    # ref (e.g. A944)
    # reg (istat)
    # prv (istat)
    # name-it
    # name-de
    # name-fr
    # wiki

    def check_wiki(self):
        dati = getWiki(self.wiki)

        if not dati:
            for suffix in [" (Italia)", " (comune)"]:
                other = self.wiki + suffix
                dati = getWiki(other)
                if dati:
                    self.wiki = other
                    break

        if not dati:
            print "%s NON ha una pagina wiki!!" % self.name_it
            other = getWikiSuggestion(self.name_it)
            if other:
                dati = getWiki(other)
                if dati:
                    self.wiki = other
                else:
                    return
            else:
                return

        mappa = {"Nome": "name_it",
                 "Codice statistico": "istat",
                 "Codice catastale": 'ref',
                 "Targa": None,
                 "Codice ISO": None}

        if dati["Grado amministrativo"] != '3':
            print "%s ha un grado amministrativo di %s" % (self.name_it, dati["Grado amministrativo"])
        del dati["Grado amministrativo"]

        if "Divisione amm grado 1" in dati:
            if regioni[self.reg].name_it != dati["Divisione amm grado 1"]:
                print "%s ha la regione sbagliata: %s / %s" % (self.name_it, dati["Divisione amm grado 1"], regioni[self.reg].name_it)
            del dati["Divisione amm grado 1"]

        if "Divisione amm grado 2" in dati:
            if dati["Divisione amm grado 2"] == "Verbania":
                dati["Divisione amm grado 2"] = "Verbano-Cusio-Ossola"
            if dati["Divisione amm grado 2"] == "no" and self.prv == '007':
                dati["Divisione amm grado 2"] = "Aosta"
            if dati["Divisione amm grado 2"] == "Massa-Carrara":
                dati["Divisione amm grado 2"] = "Massa e Carrara"
            if province[self.prv].name_it != dati["Divisione amm grado 2"]:
                print "%s ha la provincia sbagliata: %s / %s" % (self.name_it, dati["Divisione amm grado 2"], province[self.prv].name_it)
            del dati["Divisione amm grado 2"]

        if "Targa" in dati:
            if province[self.prv].ref != dati["Targa"]:
                print "%s ha la targa sbagliata: %s / %s" % (self.name_it, dati["Targa"], province[self.prv].ref)
            del dati["Targa"]

        for k, v in dati.items():
            if mappa[k] is None or mappa[k] not in self.__dict__:
                print "%s ha %s settato a %s" % (self.name_it, k, v)
            else:
                if v != self.__dict__[mappa[k]]:
                    print "%s ha %s diverso: %s / %s" % (self.name_it, k, v, self.__dict__[mappa[k]])

import csv

comuni = dict()

def read_comuni():
    r = csv.reader(open('comuni.csv', 'rb'), delimiter=';')
    headers = None
    for i, c in enumerate(r):
        if i == 0:
            headers = c
        else:
            if len(c) != len(headers):
                print "errore riga %d" % i+1
                break

            com = Comune()
            for j in range(len(headers)):
                com.__dict__[headers[j]] = c[j].decode('utf-8')
            comuni[com.istat] = com

            com.check_wiki()

def write_comuni():
    w = csv.writer(open('comuni2.csv', 'wb'), delimiter=';')
    whead = ['istat','ref','reg','prv','name_it','name_de','name_fr','wiki']
    w.writerow(whead)
    for com in sorted(comuni.values(), key = lambda a: a.istat):
        w.writerow(list(com.__dict__[i].encode('utf-8') for i in whead))
