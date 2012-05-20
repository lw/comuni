import urllib
import json
import re

def getWiki(name):
    query = 'http://it.wikipedia.org/w/api.php?action=query&prop=templates&format=json&tllimit=2&tltemplates=Template:Divisione amministrativa&titles=%s' % name
    templ = json.load(urllib.urlopen(query.encode('utf-8')))['query']['pages'].popitem()[1]
    if 'templates' not in templ or len(templ['templates']) != 1:
        # print "Non e' una divisione amministrativa"
        return None
    query = 'http://it.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=json&titles=%s' % name
    text = json.load(urllib.urlopen(query.encode('utf-8')))['query']['pages'].popitem()[1]['revisions'][0].popitem()[1]
    results = {}
    for i in ["Nome", "Stato", "Grado amministrativo", "Divisione amm grado 1", "Divisione amm grado 2", "Codice statistico", "Codice catastale", "Targa", "Codice ISO"]:
        l = re.findall("^\|\s*%s\s*=[ \t\r\f\v]*([^$]*?)[ \t\r\f\v]*$" % i, text, re.MULTILINE | re.UNICODE)
        if len(l) > 1:
            print "Found %d times %s in %s" % (len(l), i, name)
            continue
        if len(l) == 1 and l[0] != '':
            results[i] = unicode(l[0])
    if "Codice ISO" in results:
        try:
            results["Codice ISO"] = re.findall("(IT-[A-Z]{2}|IT-[0-9]{2})", results["Codice ISO"])[0]
        except:
            print "Wrong ISO code in %s" % name
    if "Stato" in results:
        if results["Stato"] != "ITA":
            print "%s non ha lo stato ITA" % name
        del results["Stato"]
    return results


def getWikiSuggestion(name):
    query = 'http://it.wikipedia.org/w/api.php?action=query&list=search&format=json&srsearch=%s&srinfo=suggestion&srprop=score&srlimit=10' % name
    results = json.load(urllib.urlopen(query.encode('utf-8')))['query']['search']
    l = list()
    for i, j in enumerate(results):
        l.append(j["title"])
        print "%d : %s" % (i, j['title'])
    choice = int(raw_input("Scegline uno : "))
    if choice == -1:
        return None
    else:
        return l[choice]


def getWikiProvincia(sigla):
    query = 'http://it.wikipedia.org/w/api.php?action=parse&prop=links&text={{IT-%s}}&format=json' % sigla
    link = json.load(urllib.urlopen(query))['parse']['links'][0]['*']
    return link
