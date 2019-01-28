import os
import re
import csv
import sys
import time
import urllib
import asyncio
import secrets
import multiprocessing as mp

import requests
import numpy as np
from bs4 import BeautifulSoup as bs


topics = [212,236,241,240,239,238,252,253,256,259,258,263,262,229,243,242,232,231,230,218,219,220,221,222,215,214,233,224,226,225,228,216,249,227,223,217,244,245,246,247,248,213,57,60,58,59,61,62,63,12,14,15,16,17,18,19,20,31,13,22,26,27,28,30,21,23,24,25,1,2,11,3,6,4,5,7,8,9,10,296,297,304,299,298,300,301,302,303,79,84,94,95,96,97,32,33,34,35,36,37,38,39,40,305,310,306,309,308,183,187,324,311,312,313,41,42,43,48,52,47,49,50,45,46,56,54,55,51,44,53,64,65,66,67,314,318,322,315,316,317,319,320,321,323,102,106,107,105,112,103,111,104,108,109,110,147,148,149,159,160,161,170,155,151,150,176,167,177,174,152,153,156,157,162,163,165,166,168,169,173,164,175,172,171,158,189,191,197,190,192,193,195,196,194,264,266,265,270,287,288,278,267,271,274,273,275,272,276,277,279,284,283,285,268,269,286,280,281,282,289,290,292,295,291,294,293,198,200,204,199,201,202,203,205,206,209,207,208,182]
'''
import csv
with open('libgen_content1.csv') as fr, open('libgen_content2_nobanLangExtTop.csv','w') as fw:
    reader = csv.reader(fr)
    writer = csv.writer(fw)
    for row in reader:
        ban = row[39]
        language = row[12]
        topic = row[13]
        extension = row[36]
        if  ban == 'ban' or ban == 'del': continue
        if language and ('English'.lower() not in language.lower().strip() and
            'Chinese'.lower() not in language.lower().strip() and
                                    'englsih'.lower() not in language.lower().strip() and
                                    '中文' not in language.strip() and
                                    'China'.lower() not in language.lower().strip() and
                                    'en' != language.lower().strip() and
                                    'eng' != language.lower().strip()):
                                        continue
        if 'russian' in language.lower(): continue
        if extension.lower() not in ('pdf','djvu'): continue
        if topic.isdigit() and int(topic) in topics: continue
        writer.writerow(row)

'''

async def get(url,headers = {},allow_redirects=True):
    await asyncio.sleep(secrets.choice(np.linspace(1,10,100)))
    
    ans = requests.get(url=url,headers=headers,timeout=300,allow_redirects=allow_redirects)
    return ans


async def mirror_Genlibrusec(ind,id1,url,keyword,row):

   for indtry in range(5):
       name = author = ''
       try:
           res = await get(url)
           content = bs(res.text,'lxml')
           bookLink = content.find('a',{'href':re.compile('http://download.library.*')})
           download = bookLink['href']
           downloadfilename = urllib.parse.unquote(download.split('/')[-1])
           title = row[1]
           authors = row[5]
           extra = [downloadfilename,download]
           print(f'[ok] [{ind}] keyword:[{keyword}] title:[{title}]')
           return extra
       except Exception as e:
            print(f'\033[31m [error] [{ind}] try...{indtry}... name:author=[{name}:{author}] {str(e)}, {url} \033[0m')
            await asyncio.sleep(2*indtry)
  
   return ['','']


async def mirror_LibgenIO(ind,id1,url,keyword,row):

   for indtry in range(5):
       name = author = ''
       try:
           md5 = row[37]
           url = f'http://booksdescr.org/ads.php?md5={md5}'
           res = await get(url)
           content = bs(res.text,'lxml')

           torrent = f'http://booksdescr.org/book/index.php?md5={md5}&oftorrent='

           download = content.find('a',{'href':re.compile(f'http://booksdl.org/get.php\?md5={md5}&key=.*')})
           download = download['href']
           title = row[1]
           authors = row[5]

           extra = [torrent,download]
           print(f'[ok] [{ind}] [mirror_LibgenIO] keyword:[{keyword}] title:[{title}] [{download}]')
           return extra
       except Exception as e:
            print(f'\033[31m [error] [{ind}] try...{indtry}... name:author=[{name}:{author}] {str(e)}, {url} \033[0m')
            await asyncio.sleep(2*indtry)
  
   return [torrent,'']



async def mirror_BOKcc(ind,id1,url,keyword,row):

   for indtry in range(5):
       name = author = ''
       try:
           md5 = row[37]
           url = f'http://b-ok.cc/md5/{md5}'
           res = await get(url)
           content = bs(res.text,'lxml')
           predownload = content.find('a',{'href':re.compile(f'/book/.*')})
           predownload = predownload["href"]
           url = f'https://b-ok.cc{predownload}'
           
           res = await get(url)
           content = bs(res.text,'lxml')
           booklink = content.find('a',{'href':re.compile(f'/dl/{predownload.split("/")[2]}')}) 
           path = booklink['href']
           download = f'https://b-ok.cc{path}'
           
           headers = {'path':path,'referer':f'{url}?_ir=1'}
           res = await get(url=download,headers=headers,allow_redirects=False) 
           download = res.headers['Location']

           title = row[1]
           authors = row[5]
           extra = download
           print(f'[ok] [{ind}] [mirror_BOKcc] keyword:[{keyword}] title:[{title}] [{download}]')
           return extra
       except Exception as e:
            print(f'\033[31m [error] [{ind}] try...{indtry}... name:author=[{name}:{author}] {str(e)}, {url} \033[0m')
            await asyncio.sleep(2*indtry)
  
   return ''


async def mirror_LibgenPW(ind,id1,url,keyword,row):

   for indtry in range(5):
       name = author = ''
       try:
           id1 = row[0]
           url = f'https://ambry.pw/item/detail/id/{id1}'
           res = await get(url)
           content = bs(res.text,'lxml')
           bookLink = content.find('a',{'href':re.compile('https://dnld.ambry.cx/download/book/.*')})
           download = bookLink['href']
           title = row[1]
           authors = row[5]
           extra = download
           print(f'[ok] [{ind}] [mirror_LibgenPW] keyword:[{keyword}] title:[{title}] [{download}]')
           return extra
       except Exception as e:
            print(f'\033[31m [error] [{ind}] try...{indtry}... name:author=[{name}:{author}] {str(e)}, {url} \033[0m')
            await asyncio.sleep(2*indtry)
  
   return ''


class Bot:

    def __init__(self):
        self.tasks = asyncio.Queue()

    async def download(self):
        while True:
            task = await self.tasks.get()
            if task == 'done':
                return
            else:
                ind,id1,url,keyword,row = task
                downloadfilename,downloadmirror1 = await mirror_Genlibrusec(ind,id1,url,keyword,row)
                row.extend([downloadfilename,downloadmirror1])

                torrent,downloadmirror2 = await mirror_LibgenIO(ind,id1,url,keyword,row)
                row.extend([torrent,downloadmirror2])

                downloadmirror3 = '' #await mirror_BOKcc(ind,id1,url,keyword,row)
                row.append(downloadmirror3)

                downloadmirror4 = await mirror_LibgenPW(ind,id1,url,keyword,row)
                row.append(downloadmirror4)

                with open(f'libgen.io-{keyword}.txt','a') as fa:
                    writer = csv.writer(fa)
                    writer.writerow(row)
            

def main(lines_keyword):
    keyword,lines = lines_keyword
    bots = [Bot() for i in range(9)]
    result = f'libgen.io-{keyword}.txt'


    doneDi = {}
    if os.path.exists(result):
        with open(result) as fr:
            reader = csv.reader(fr)
            for row in reader:
                doneDi[row[0]] =1

    for ind,row in enumerate(lines):
        id1 = row[0]
        if id1 in doneDi: continue
        title = row[1]
        series = row[3]
        authors = row[5]
        publisher = row[8]
        year = row[6]
        pages = row[10] # 10,11
        language = row[12]
        topic = row[13]
        size = row[35]
        extension = row[36] 
        hashcode = row[37]
        ban = row[39]
        filename = row[40]

        if ban == 'ban' or ban == 'del': continue
        if language and ('English'.lower() not in language.lower().strip() and
                        'Chinese'.lower() not in language.lower().strip() and
                        'englsih'.lower() not in language.lower().strip() and
                        '中文' not in language.strip() and
                        'China'.lower() not in language.lower().strip() and
                        'en' != language.lower().strip() and
                        'eng' != language.lower().strip()):
            continue
        if 'russian' in language.lower(): continue
        if extension.lower() not in ('pdf','djvu','bz2','gz','rar','zip','tar','7z','epub'): continue
        if topic.isdigit() and int(topic) in topics: continue
        mirror1 = f'http://lib1.org/_ads/{hashcode}'
        url = mirror1
        meg = [ind,id1,url, keyword,row]
        bots[ind%9].tasks.put_nowait(meg) 

    for i in bots:
        i.tasks.put_nowait('done')

    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(bot.download()) for bot in bots]
    task_group = asyncio.gather(*tasks)
    loop.run_until_complete(task_group)
    #loop.close()
#            downloadlink = mirror_Genlibrusec(url, keyword, title, authors, extension)
#            if downloadlink:
#                fw.write(downloadlink)  
#            else:
#                print(f'[error] id:[{id1}] title:[{title}] cannot create the download link!')

if __name__ == "__main__":
    #main(*sys.argv[1:])
    
    file = sys.argv[1]
    num = 20
    totalines = [[] for i in range(num)]
    with open(file) as fr:
        reader = csv.reader(fr)
        for ind,row in enumerate(reader):
            totalines[ind%num].append(row)

    print('ready!')
    with mp.Pool(num) as p:
        p.map(main,[[f'libgentotal{ind}',lines] for ind,lines in enumerate(totalines)])
