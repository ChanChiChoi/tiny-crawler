# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs
import re
import math

keyword = 'AND+data+preprocess'# if two or more words, you need add AND before the words
keyword = 'segmentation'# this the single word

totalnums = re.compile('Showing results 1 through \d+ \(of (\d+) total\)')
# access the pagg for total number
url = f'https://arxiv.org/find/grp_cs/1/ti:+{keyword}/0/1/0/all/0/1?skip=0'
res = requests.get(url = url)
ans = bs(res.text,'lxml')
totalnums = int(totalnums.findall(res.text)[0])


for i in range(totalnums)[::25]:

  url = f'https://arxiv.org/find/grp_cs/1/ti:+{keyword}/0/1/0/all/0/1?skip={i}'
  res = requests.get(url = url)
  ans = bs(res.text,'lxml')

  for block in ans.find_all('dt'):
    dt = block.find('a',{"href":re.compile('/pdf/')})['href']#get the id of paper
    filename = block.next_sibling.next_sibling.find('span',{'class':"descriptor"}).next_sibling.strip()# get the filename of paper

    with open(f'arxiv-{keyword.replace("+","_")}.txt','a') as fa:
      fa.write(f'#{dt.split("/")[-1]}.pdf\t{filename.replace(" ","_")}.pdf\n')
      fa.write('https://arxiv.org'+dt+'.pdf\n')
  print(f'has down {i+25} links')
