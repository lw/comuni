#!/usr/bin/env python
# -*- coding: utf-8 -*-

from check_province import *
from check_comuni import *

import string

def parseName (name):
    # Convertiamo i nomi in maiuscolo, togliamo tutta la punteggiatura
    # (compresi gli accenti) e speriamo che in questo modo i nomi diventino
    # univoci
    mappa2 = {'à':'a','á':'a','è':'e','é':'e','ì':'i','í':'i','ò':'o','ó':'o','ù':'u','ú':'u'}
    mappa = dict((k.decode('utf-8'), v.decode('utf-8')) for k, v in mappa2.iteritems())
    name = ''.join(mappa.get(i, i) for i in name)
    name = name.upper()
    name = ''.join(i if i in string.letters else '' for i in name)
    return name

def distanzaEdit(s, t):
    if len(s) > len(t):
        s, t = t, s
    r1 = [i for i in range(len(s) + 1)]
    r2 = [0 for i in range(len(s) + 1)]
    for i in range(1, len(t) + 1):
        r2[0] = i
        for j in range(1, len(s) + 1):
            if s[j-1] == t[i-1]:
                r2[j] = min(r2[j-1] + 1, r1[j] + 1, r1[j-1])
            else:
                r2[j] = min(r2[j-1] + 1, r1[j] + 1, r1[j-1] + 1)
        r1, r2 = r2, r1
    return r1[-1]

import csv

reader = csv.reader(open('ITALIA.csv', 'rb'), delimiter=';')

headers = None

catasto = dict()

for i, row in enumerate(reader):
    if i == 0:
        headers = row
    else:
        if row[4] == '' and row[5] == '' and row[6] == '' and row[7] == '' and row[8] == '':
            if row[2] not in catasto:
                catasto[row[2]] = dict()
            if '*' in row[3]:
                row[3] = row[3].split('*')[0]
            catasto[row[2]][parseName(row[3].decode('utf-8'))] = row[0].decode('utf-8')

nostri = dict()

for i in comuni.itervalues():
    if province[i.prv].ref not in nostri:
        nostri[province[i.prv].ref] = dict()
    nostri[province[i.prv].ref][parseName(i.name_it)] = i.ref


if len(catasto) != len(nostri):
    print "ERRORE il numero di province e' diverso: %d / %d" % (len(catasto), len(nostri))

for prv, c in catasto.iteritems():
    if prv not in nostri:
        print "ERRORE noi non abbiamo la provincia %s" % prv
        continue

    n = nostri[prv]

    if len(c) != len(n):
        print "ERRORE il numero di comuni in %s e' diverso: %d / %d" % (prv, len(c), len(n))

    for name in list(c.iterkeys()):
        if name in n:
            if c[name] != n[name]:
                print "%s : %s / %s" % (name, c[name], n[name])
            del c[name]
            del n[name]

    for name in list(c.iterkeys()):
        for o_name in list(n.iterkeys()):
            if name in o_name or o_name in name or distanzaEdit(name, o_name) <= 2:
                if c[name] != n[o_name]:
                    print "%s / %s : %s / %s" % (name, o_name, c[name], n[o_name])
                del c[name]
                del n[o_name]

    if len(c) == 1 and len(n) == 1:
        name, uno = c.popitem()
        o_name, due = n.popitem()
        if uno != due:
            print "%s / %s : %s / %s" % (name, o_name, uno, due)

    if len(c) + len(n) != 0:
        print prv
        if len(c) != 0:
            print "c : %s" % c
        if len(n) != 0:
            print "n : %s" % n
