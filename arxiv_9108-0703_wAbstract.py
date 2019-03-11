#-*- coding: utf-8 -*-
import re
import time
import secrets
import itertools
import requests
import os.path as osp
from bs4 import BeautifulSoup as bs

clean_pat = re.compile('<!--[^<>]*-->',re.M)
gHeaders = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'}
gArchives = ['astro-ph',
             'cond-mat',
             'cs',
             'econ',
             'eess',
             'gr-qc',
             'hep-ex',
             'hep-lat',
             'hep-ph',
             'hep-th',
             'math',
             'math-ph',
             'nlin',
             'nucl-ex',
             'nucl-th',
             'physics',
             'q-bio',
             'q-fin',
             'quant-ph',
             'stat']
gOldArchives = ['acc-phys',
                'adap-org',
                'alg-geom',
                'ao-sci',
                'atom-ph',
                'bayes-an',
                'chao-dyn',
                'chem-ph',
                'cmp-lg',
                'comp-gas',
                'dg-ga',
                'funct-an',
                'mtrl-th',
                'patt-sol',
                'plasm-ph',
                'q-alg',
                'solv-int',
                'supr-con']

def time9108_0703():
    months91 = '9108,9109,9110,9111,9112'.split(',')
    months07 = '0701,0702,0703'.split(',')

    YEARS = list(range(1992,2007))
    MONTHS = list(range(1,13))
    newMonths = []
    for year_, month_ in itertools.product(YEARS,MONTHS):
        newMonths.append(f'{str(year_)[-2:]}{month_:02d}')

    newMonths = months91+newMonths+months07
    return newMonths[::-1]

months = time9108_0703()

def get_lasttime(filename):

  if not osp.exists(filename): return 1
  with open(filename,'rb') as fr:
    lines = fr.readlines()
    left5line = lines[-5:]
    isDone = sum([1 if '=========' in line.decode('utf-8') else 0 for line in lines])
    if isDone == 5: return 'done'

    numlines = len(lines)

    if lines and  '===' not in lines[-1].decode('utf-8'):
        col = lines[-1].decode('utf-8').strip().split('\t')[0]
        start = int(col.split('.')[1]) + 1
    else:
        start = numlines+1
    return start

def get_result(text,id):
    abs = bs(text,'lxml')
    try:
        h1 = abs.find_all('h1')[1].text
    except:
       return 'maybe meet antiscrapy'

    if 'doesn\'t exist' in h1: return 'doesn\'t exist'

    title = abs.find('h1',{'class':"title mathjax"}).text.split('\n')[1]
    subject = abs.find('span',{'class':"primary-subject"}).text
    authors = abs.find('div',{'class':"authors"}).text.replace('\n','')
    authors = clean_pat.sub('',authors)
    abstract = abs.find('blockquote', {'class':"abstract mathjax"}).text
    abstract = abstract.replace('\n',' ').replace('\t',' ')
    ans = '\t'.join([id,title,subject,authors,abstract])
    ans += '\n'

    print('\t'.join([id,title,subject]))

    return ans

def _access(archive,month):

    filename = f'paperMeta4arxiv_9108To0703/arxiv-{archive.replace("-","_")}-{month}.txt'
    start = get_lasttime(filename)
    if start == 'done': return 'done'

    endCount = 0
    anti = 0
    for i in range(start,999):

        time.sleep(3+secrets.randbelow(4))
        id = f'{month}{i:03d}'
        url = f'https://arxiv.org/abs/{archive}/{id}'
        res = requests.get(url = url,headers=gHeaders,timeout = 30)
        res = get_result(res.text,id)

        if res == 'doesn\'t exist':
            res = '='*50
            endCount += 1
            if endCount == 5: return 'done'
        elif res == 'maybe meet antiscrapy':
            anti += 1
            if anti ==5 : raise SystemExit('meet anti scrapy policy')
            continue
        else:
           endCount = 0

        with open(filename,'a') as fa:
            fa.write(res)

if __name__== '__main__':

    for month in months:
        for archive in gArchives:
            _access(archive,month)
