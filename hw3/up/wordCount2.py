import requests
import json
import re
import sys

title = sys.argv[1]



def wiki_get(title):
    url = 'http://en.wikipedia.org/w/api.php'
    values = {'action' : 'query',
          'prop' : 'revisions',
          'titles' : title,
          'rvprop' : 'content',
          'format' : 'json',
          'prop' : 'extracts',
          'exsectionformat' : 'plain',
          'continue':''}
    r = requests.get(url, params=values)
    return r


def strip_txt(string):
    string = re.sub(r'(?i)&nbsp;', ' ', string)
    string = re.sub(r'(?i)<br[ \\]*?>', '\n', string)
    string = re.sub(r'(?m)<!--.*?--\s*>', '', string)
    string = re.sub(r'(?i)<ref[^>]*>[^>]*<\/ ?ref>', '', string)
    string = re.sub(r'(?m)<.*?>', '', string)
    string = re.sub(r'(?i)&amp;', '&', string)
    #
    string = re.sub(r'\[\s\d+\s\]', '', string)
    string = re.sub(r'"', '', string)
    string = re.sub(r' +[.] +', '. ', string)
    string = re.sub(r' +[,] +', ', ', string)
    string = re.sub(r'\s*\[\s*edit\s*\]\s*', '\n', string)
    return string


def get_wrds(wrds, cmwds):
    wrdcnt = {}
    for w in wrds:
        if w not in cmwds and len(w) >= 4:
            if w in wrdcnt:
                wrdcnt[w] += 1
            else:
                wrdcnt[w] = 1
    sf =  sorted(wrdcnt.items(),key=lambda wrdcnt: wrdcnt[1],reverse=True)
    return sf

res = wiki_get(title)
js = res.json()
data = js['query']['pages']
c = res.content
j = json.loads(c)
wiki= strip_txt(c)
wrds = wiki.lower().strip().split()
cmwds = [c.split()[1] for c in  open("/home/local/CORNELL/public/hw3_files/common_words.txt")]
prepfile = '/home/local/CORNELL/asd223/hw3/prepositionts.txt'
preps = [p.strip() for p in open(prepfile)]
for p in preps:
    cmwds.append(p)

top_wrds = get_wrds(wrds, cmwds)

cw = get_wrds(wrds, cmwds)[0:9]

for c in cw:
    print '%s\t%i' %(c[0], c[1])

