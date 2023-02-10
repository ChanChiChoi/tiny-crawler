# -*- coding: utf-8 -*-

'''
papers.txt is the file, which contans papers name
each line has one paper name,like:
==================
paper1name
paper2name
paper3name
=================
'''

import requests
import lxml
from bs4 import BeautifulSoup


def access(url:str):

    con = requests.get(url,timeout = 60)
    return con.text


def papercode(papername:str):
    meta_url = 'https://paperswithcode.com/search?q_meta=&q_type=&q={}'.format(papername)
#    url = "https://paperswithcode.com/paper/{}#code".format(papername.replace(' ','-'))
    con = access(meta_url)
    bs = BeautifulSoup(con,'lxml')


    authors = bs.find_all('p',{'class':'author-section'})
    href = ''
    text = ''
    if len(authors) ==1:
      author = authors[0].find('a')
      href = author.get('href')
      text = author.text
    else:
      for section in authors:
        author = section.find('a')
        href = author.get('href')
        paper = href.split('/')[-1].split('#')[0]
        oripapername = papername.replace('-',' ').replace('$','').replace('?','').replace('\\','').replace(':','').replace(',','').lower()
        papername1 = paper.replace('-',' ').replace('$','').replace('?','').replace('\\','').replace(':','').replace(',','')
        if oripapername.startswith(papername1): 
          text = author.text

    if text == '': 
       return ''
    #if int(text.split()[0]) == 0: return ''
    if text.split()[0].startswith('no'): return ''

#    li = bs.find_all('a',{'class':'badge badge-dark'})
#    ans = li[0]
#    href = ans.get('href')
#
#-----------------------------------
    print('【论文】:{}; 【code】:{}'.format(papername, href))
    new_url = 'https://paperswithcode.com{}'.format(href)
    con = access(new_url)
     
    bs = BeautifulSoup(con,'lxml')

    codes = bs.find_all('a',{'class':'code-table-link'})
    if len(codes) == 0: return ''
    code = codes[0].get('href')

    return code


def single(papername:str):
    code = papercode(papername)
    return code  
    



if __name__ == '__main__':
 
 with open('papers.txt','r') as fr, open('papers_code.txt','w') as fw: 
   for line in fr:
     papername = line.strip()
     code = single(papername)
     fw.write('{}\t{}\n'.format(papername,code))


