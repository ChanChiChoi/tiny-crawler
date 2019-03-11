#-*- coding: utf-8 -*-

import re
import time
import math
import secrets
import itertools
import requests
import os.path as osp
from bs4 import BeautifulSoup as bs

clean_pat = re.compile('<!--[^<>]*-->',re.M)
gHeaders = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'}
gArchives = [#'astro-ph',
             #'cond-mat',
             'cs',
             #'econ',
             'eess',
             #'gr-qc',
             #'hep-ex',
             #'hep-lat',
             #'hep-ph',
             #'hep-th',
             'math',
             #'math-ph',
             'nlin',
             #'nucl-ex',
             #'nucl-th',
             #'physics',
             #'q-bio',
             #'q-fin',
             #'quant-ph',
             'stat']

def get_lasttime(filename):

  if not osp.exists(filename): return 0
  with open(filename,'rb') as fr:
    lines = fr.readlines()
    numlines = len(lines)
    start = math.ceil(numlines/50)

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
    abstract = abs.find('blockquote', {'class':"abstract mathjax"}).text
    abstract = abstract.replace('\n',' ').replace('\t',' ')
    ans = '\t'.join([id,title,subject,authors,abstract])
    ans += '\n'

    print('\t'.join([id,title,subject]))

    return ans


def requestsGet(url,tryTime = 5):

    for i in range(tryTime):
        try:
            time.sleep(3+secrets.randbelow(4))
            res = requests.get(url = url,headers=gHeaders,timeout = 60)
            break
        except Exception as e:
            print(f'[{url}] {str(e)}')
            res = None
    return res

def get_year(archive):
    url = f'https://arxiv.org/archive/{archive}'
    res = requestsGet(url)
    page = bs(res.text,'lxml')
    yearStart = page.find_all('h1')[1].text

    yearPattern = re.compile('\d+')
    yearS = yearPattern.findall(yearStart)[0]
    return int(yearS)

def get_yearNum(archive,year):
    url = f'https://arxiv.org/list?year={year}&month=all&archive={archive}&submit=Go'
    res = requestsGet(url)
    res = bs(res.text,'lxml')
    small = res.find('small').text
    totalNum = re.compile('total of (\d+) entries')
    totalNum = totalNum.findall(small)[0]

    lessTotal = re.compile(f'(\d+)-{totalNum}')
    try:
        lessTotal = lessTotal.findall(small)[0]
    except:
        lessTotal = totalNum
    return int(lessTotal),int(totalNum)

def get_list_result(archive,year,skip):
    url = f'https://arxiv.org/list/{archive}/{year}?skip={skip}&show=50'
    res = requestsGet(url)
    if not res: raise SystemExit('='*50+'meet anti scrapy policy or network error')

    res = bs(res.text,'lxml')
    dts = res.find_all('dt')

    stringsLi = []
    for dt in dts:
        try:
            paperId = dt.find('a').text
        except:
            print(f'[error] {url} {ind} {dt}')
            continue
        paperUrl = dt.find('a',{'href':True})['href']

        meta = dt.next_sibling.next_sibling
        title = meta.find('div',{"class":"list-title mathjax"}).find('span').next_sibling
        title = title.strip()

        author = meta.find('div',{"class":"list-authors"}).text
        author = author.strip().replace('\n',' ')
        authors = clean_pat.sub('',authors)
        
        subject = meta.find('div',{"class":"list-subjects"}).text
        subject = subject.strip().replace('\n',' ')

        string = '\t'.join([paperId,paperUrl,title,author,subject])
        string += '\n'
        stringsLi.append(string)
    return stringsLi

def _access(archive,year):

    filename = f'paperMeta4arxiv_byArchive/arxiv-{archive.replace("-","_")}-{year}.txt'
    start = get_lasttime(filename)
    if start == 'done': return 'done'

    endCount = 0
    anti = 0

    lessTotal,totalNum = get_yearNum(archive,str(year)[-2:])

    for i in range(start,math.ceil(totalNum/50)):

        res = get_list_result(archive,str(year)[-2:],i*50)
        print(f'{archive} {year} {lessTotal}-{totalNum} [{i+1}/{math.ceil(lessTotal/50)}]')

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
            fa.writelines(res)

if __name__== '__main__':

    for archive in gArchives:
        start = get_year(archive)
        for year in range(start,2019):
            print(year)
            _access(archive,year)
