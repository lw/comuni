import urllib
import json
import csv

regione_istat = "08"
province_istat = {
    33: 'Piacenza',
    34: 'Parma',
    35: "Reggio nell'Emilia",
    36: 'Modena',
    37: 'Bologna',
    38: 'Ferrara',
    39: 'Ravenna',
    40: 'Forl\xc3\xac-Cesena',
    99: 'Rimini'}
comuni_istat = {}

def gen_comuni_istat():
    r = csv.reader(open('comuni_istat.csv', 'rb'), delimiter=';')
    for c in r:
        comuni_istat[c[3]] = c[4]

gen_comuni_istat()


def checkExistence(title):
    query = 'http://it.wikipedia.org/w/api.php?action=query&titles=%s&format=json' % title
    page = urllib.urlopen(query)
    return '"missing"' not in page


def getWikiProvincia(sigla):
    query = 'http://it.wikipedia.org/w/api.php?action=parse&prop=links&text={{IT-%s}}&format=json' % sigla
    link = json.load(urllib.urlopen(query))['parse']['links'][0]['*']
    return link    


def filterTags(attrs):
    if not attrs: return

    tags = {'source': 'Regione Emilia-Romagna'}

    if 'TY_E' in attrs:
        tags['boundary'] = 'administrative'

        if attrs['TY_E'] == 'REG':
            tags['admin_level'] = '4'
            tags['name'] = attrs['NM_REG']
            tags['ref:istat'] = regione_istat

            # Per le Regioni verifichiamo semplicemente che sulla Wiki italiana
            # esista una pagina con quel nome (potremmo anche usare il template
            # {{IT-XYZ}}, dove XYZ e' la sigla della regione...).
            if checkExistence(tags['name']):
                tags['wikipedia'] = 'it:%s' % tags['name']
            else:
                print "Pagina wiki per la regione %s non trovata" % tags['name']

        if attrs['TY_E'] == 'PRV':
            tags['admin_level'] = '6'
            tags['name'] = province_istat[int(attrs['ISTAT'])]
            tags['ref'] = attrs['SG_PRV']
            tags['ref:istat'] = '%03d' % int(attrs['ISTAT'])

            # Per le Province usiamo il template {{IT-XY}} (dove XY e' la sigla
            # della provincia) per ottenere il link alla pagina.
            tags['wikipedia'] = 'it:%s' % getWikiProvincia(tags['ref'])

        if attrs['TY_E'] == 'COM':
            tags['admin_level'] = '8'
            tags['name'] = comuni_istat[attrs['ISTAT']]
            tags['ref'] = attrs['CD_BLF']
            tags['ref:istat'] = attrs['ISTAT']

            # Per i Comuni verifichiamo semplicemente che sulla Wiki italiana
            # esista una pagina con quel nome.
            if checkExistence(tags['name']):
                tags['wikipedia'] = 'it:%s' % tags['name']
            else:
                print "Pagina wiki per il comune %s non trovata" % tags['name']

    return tags

translateAttributes = filterTags

