# -*- coding: utf-8 -*-
"""
Created on Wed Apr 05 21:17:44 2017

@author: shouh
"""
import re
import requests
from bs4 import BeautifulSoup as bs

gre = re.compile('var redirect = "(.*)";')
urlOrigin = 'https://passport.csdn.net/?service=http://write.blog.csdn.net/postlist'
headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Host':'passport.csdn.net',
        'Referer':'https://passport.csdn.net/?service=http://write.blog.csdn.net/postlist',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
    
#1 - use requests.Session to keep the cookies
ses = requests.Session()
resposeOrigin = ses.get(urlOrigin)
resposeOrigin = bs(resposeOrigin.text)

#2 - get the random value from the response of first access urlOrigin
lt = resposeOrigin.find('input',{'name':'lt'})['value']
execution = resposeOrigin.find('input',{'name':'execution'})['value']
_eventId = resposeOrigin.find('input',{'name':'_eventId'})['value']
data = {
  'username':'username',
  'password':'password',
  'lt':lt,
  'execution':execution,
  '_eventId':_eventId
}

#3 - login csdn
responseLogin = ses.post(url = urlOrigin,headers = headers,data = data)

#4 - get the redirect link
urlRedirect = gre.findall(responseLogin.text)[0]

#5 - delete the useless element of headers 
del headers['Referer']
del headers['Host'] 

#6 - one useless but necessary access operation
_ = ses.get(url = urlRedirect,headers = headers)

#7 - get the docment category links
urlDocList = 'http://write.blog.csdn.net/category'
responseDocList = ses.get(url = urlDocList,headers = headers)
print responseDocList.text
