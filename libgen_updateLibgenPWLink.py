import re
import os
import sys
import time
import argparse
import concurrent.futures

import csv
import requests
from bs4 import BeautifulSoup as bs


def get(url,headers = {},allow_redirects=True):
   # await asyncio.sleep(secrets.choice(np.linspace(1,10,100)))
    ans = requests.get(url=url,headers=headers,timeout=300,allow_redirects=allow_redirects)
    return ans


def mirror_LibgenPW(zip2):
   ind,row = zip2
   for indtry in range(5):
       name = author = ''
       try:
           id1 = row[0]
           url = f'https://ambry.pw/item/detail/id/{id1}'
           res = get(url)
           content = bs(res.text,'lxml')
           bookLink = content.find('a',{'href':re.compile('https://d-m.bksdl.xyz/download/book/.*')})
           download = bookLink['href']
           title = row[1]
           authors = row[5]
           extra = download
           row[-1] = download
           print(f'[ok] [{ind}] [mirror_LibgenPW]  title:[{title}] [{download}]')
           return row
       except Exception as e:
            print(f'\033[31m [error] [{ind}] try...{indtry}... name:author=[{name}:{author}] {str(e)}, {url} \033[0m')
            #await asyncio.sleep(2*indtry)
            time.sleep(2*indtry)

   return row



def main(file,max_workers):

    dir,txt = os.path.split(file)
    with open(file) as fr, open(os.path.join(dir,'new_'+txt),'w') as fw:
        reader = csv.reader(fr)
        writer = csv.writer(fw)
        with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
            for row in executor.map(mirror_LibgenPW,enumerate(reader)):
                writer.writerow(row)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-f')
    parser.add_argument('-n')
    args = parser.parse_args()
    file = args.f
    max_workers = int(args.n) if args.n else 1
    main(file,max_workers)
