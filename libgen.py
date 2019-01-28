# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 23:17:40 2018
@author: shouhuxianjian
"""
import multiprocessing as sp
import requests
import re
import time
import random
import secrets
import multiprocessing as sp
from bs4 import BeautifulSoup as bs
keyword = 'measure'
endpages = 2
curcolumn = ['title','series', 'def'][2]
sortmode = ['DESC','ASC'][0]


def get(url):
    time.sleep(secrets.choice(np.linspace(1,10,100)))
    ans = requests.get(url=url,timeout=300)
    return ans


def mirror_Genlibrusec(content,page):
    downloadlinks = []
    titles = content.find_all('a',{'title':'Gen.lib.rus.ec'})
    time.sleep(1)
    for indb,book in enumerate(titles):
        libgen = book['href']
        for indtry in range(5):
            name = author = ''

            try:
                res = get(url = libgen)
                content = bs(res.text,'lxml')
                if content.find('h1'):
                    name = content.find('h1').text
                if content.find('p',text=re.compile('Author.*')):
                    author = content.find('p',text=re.compile('Author.*')).text
                bookLink = content.find('a',{'href':re.compile('http://download.library.*')})
                download = bookLink['href']
                download = f'# {name}\t{author}\n{download}\n'
                downloadlinks.append(download)
                print(f'keyword:[{keyword}] column:[{curcolumn},{sortmode}] page:{page} subpage:{indb}')
                break
            except Exception as e:
                 print(f'try...{indtry}...page:{page} subpage:{indb} name:author=[{name}:{author}] {str(e)}, {libgen}')

                 time.sleep(2*indtry)

    return downloadlinks
        

def mirror_Libgenio(content,page):
    downloadlinks = []
    titles = content.find_all('a',{'title':'Libgen.io'})
    pass
def mirror_BOKcc(content,page):
    downloadlinks = []
    titles = content.find_all('a',{'title':'B-OK.cc'})
    pass


def mirror_libgenpw(content,page):

  downloadlinks = []
  titles = content.find_all('a',{'title':'Libgen.pw'})
  for indb,book in enumerate(titles):
    libgen = book['href']
    print(libgen)
    for indtry in range(5):
        name = author = ''
        try:
            res = get(url = libgen)
            content = bs(res.text,'lxml')
            if content.find('div',{'class':'book-info__title'}):
                name = content.find('div',{'class':'book-info__title'}).text
            if content.find('div',{'class':'book-info__lead'}):
                author = content.find('div',{'class':'book-info__lead'}).text
            bookLink = content.find('a',text='Open download')
            if not bookLink:
                bookLink = content.find('a',text='Get from vault')

            bookLink = 'https://libgen.pw'+bookLink['href']
            download = 'https://dnld.ambry.cx/download/book/'+bookLink.split('/')[-1]
            download = f'# {name}\t{author}\n{download}\n'
            downloadlinks.append(download)
            print(f'keyword:[{keyword}] column:[{curcolumn},{sortmode}] page:{page} subpage:{indb}')
            break

        except Exception as e:
             print(f'try...{indtry}...page:{page} subpage:{indb} {str(e)}')

  return downloadlinks


def mirror_BookFInet(content,page):
    downloadlinks = []
    titles = content.find_all('a',{'title':'BookFI.net'})
    pass

def handle(page):
  time.sleep(1+secrets.randbelow(10)+random.random())
  res = requests.get(url = f'http://gen.lib.rus.ec/search.php?&res=100&req={keyword}&phrase=1&view=simple&column={curcolumn}&sort=year&sortmode={sortmode}&page={page}&open=0',timeout=300,verify=False)
  content = bs(res.text,'lxml')

  downloadlinks = mirror_libgenpw(content,page)

  with open(f'libgen.io-{keyword.replace("+","_")}-{curcolumn}-{sortmode}-{page}.txt', 'a') as fa:
      fa.writelines(downloadlinks)
  
  return downloadlinks

if __name__ == '__main__':
    with sp.Pool(10) as p:
        ''' you need get the number of pages'''
        links = p.map(handle,range(1,1+endpages))
        #links = p.map(handle,[8,10])
        for ind,link in enumerate(links):
            print(f'page {ind+1}: has {len(link)}')


