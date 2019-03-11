# -*- coding: utf-8 -*-
import re
import time
import secrets
import itertools
import requests
import os.path as osp
from bs4 import BeautifulSoup as bs

gHeaders = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'}
clean_pat = re.compile('<!--[^<>]*-->',re.M)
months = sorted('0704,0705,0706,0707,0708,0709,0710,0711,0712'.split(','),reverse=True)

def time2008_2018():
    YEARS = list(range(2008,2018))
    MONTHS = list(range(1,13))
    newMonths = []
    for year_, month_ in itertools.product(YEARS,MONTHS):
        newMonths.append(f'{str(year_)[-2:]}{month_:02d}')

    newMonths.extend('1801,1802,1803,1804,1805'.split(','))

    return sorted(newMonths,reverse=True)

months.extend(time2008_2018())

def get_lasttime(filename):

  if not osp.exists(filename): return 1
  with open(filename,'rb') as fr:
    lines = fr.readlines()
    left5line = lines[-5:]
    isDone = sum([1 if '=========' in line.decode('utf-8') else 0 for line in lines])
    if isDone >= 5: return 'done'

    numlines = len(lines)

    if lines and  '===' not in lines[-1].decode('utf-8') and '---' not in lines[-1].decode('utf-8'):
        col = lines[-1].decode('utf-8').strip().split('\t')[0]
        start = int(col.split('.')[1]) + 1 
    else:
        start = numlines+1
    return start

def get_result(text,id):
    abs = bs(text,'lxml')
    try:
        h1 = abs.find_all('h1')[1].text
        if  ' not found' in h1:
            return '='*50
    except:
       return 'maybe meet antiscrapy'

    if 'doesn\'t exist' in h1: return 'doesn\'t exist'

    try:
        title = abs.find('h1',{'class':"title mathjax"}).text.replace('\n','').replace('Title:','')
    except:
        print(abs.find('h1',{'class':"title mathjax"}))
        return '='*50
    subject = abs.find('span',{'class':"primary-subject"}).text
    authors = abs.find('div',{'class':"authors"}).text.replace('\n','')
    authors = clean_pat.sub('',authors)
    abstract = abs.find('blockquote', {'class':"abstract mathjax"}).text
    abstract = abstract.replace('\n',' ').replace('\t',' ')
    ans = '\t'.join([id,title,subject,authors,abstract])
    ans += '\n'

    print('\t'.join([time.asctime(),id,title,subject]))
    
    return ans

def requestsGet(url,tryTime = 5):

    for i in range(tryTime):
        try:
            time.sleep(3+secrets.randbelow(4))
            res = requests.get(url = url,headers=gHeaders,timeout = 60)
            break
        except Exception as e:
            print(f'[{i}] [{url}] {str(e)}')
            time.sleep(7)
            res = None
    return res

def _access(month):

    filename = f'paperMeta4arxiv1/arxiv-{month}.txt'
    start = get_lasttime(filename)
    if start == 'done': return 'done'       
    
    endCount = 0
    anti = 0
    for i in range(start,13000):

        id = f'{month}.{i:05d}'
        url = f'https://arxiv.org/abs/{id}'

        print(url)
        res = requestsGet(url)
        
        if not hasattr(res,'ok') and  not res: raise SystemExit('='*50+'meet anti scrapy policy or network error')

        res = get_result(res.text,id)

        if res == 'doesn\'t exist':
            res = '='*50+'\n'
            endCount += 1
        elif res == 'maybe meet antiscrapy':
            anti += 1
            if anti == 5 : raise SystemExit(f'meet anti scrapy policy,has try {anti} times')
            continue
        elif '=====' in res:
            endCount += 1
            res += '\n'
        else:
           endCount = 0
           
        if endCount == 5: return 'done'

        with open(filename,'a') as fa:
            fa.write(res)

if __name__== '__main__':

    for month in months:
        _access(month)
