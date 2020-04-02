# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 10:46:31 2020

@author: lenovo
"""

import requests,re
from bs4 import BeautifulSoup

def word_sim_baidu(word1,word2):
    word=word1+'+'+word2
    url='https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&word=%s'%word
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
    req=requests.get(url,headers=headers)
    soup=BeautifulSoup(req.content,'html.parser')
    # #header_top_bar > span
    # div[id="header_top_bar"] span
    text=soup.select('div[id="header_top_bar"] span')
    print(text[0].text)
    news_num=re.findall('\d.*\d',text[0].text)
    news_num=int(re.sub(',','',news_num[0]))
    print(news_num)
    
    #被限制了，与网页显示数字并不相同，加了cookie解决    
    url='https://www.baidu.com/s?&wd=%s&ie=utf-8'%word
    headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, compress',
        'Accept-Language': 'en-us;q=0.5,en;q=0.3',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0',
        'Cookie': 'BAIDUID=40998A376CEFA673F348CE5E9A97718A:FG=1; PSTM=1585656433; BD_UPN=12314753; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BIDUPSID=C9B7B2E958525890F64CA2C9579FDE16; BDUSS=JrNWZGOE1CM09XZjREZU4wZlNubm1wZkxoblVmMzZOelB6Yk9sdWlMVEg5NnhlRVFBQUFBJCQAAAAAAAAAAAEAAACc~LK0tLDN4rXE0NywoQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMdqhV7HaoVeeT; delPer=0; BD_CK_SAM=1; PSINO=5; BDRCVFR[C0p6oIjvx-c]=rJZwba6_rOCfAF9pywd; sug=3; sugstore=0; ORIGIN=0; bdime=0; H_PS_645EC=3c91hJ%2BYT2NBY%2BblBEN7PQZemw%2FiKgYyZ2z7qqxPSPsEjiHwfBrcsH%2FkkCk; H_PS_PSSID=; BDSVRTM=173'
    }
    req=requests.get(url,headers=headers)
    soup=BeautifulSoup(req.content,'html.parser')
    text=soup.select('#container > div.head_nums_cont_outer.OP_LOG > div > div.nums > span')
    print(text[0].text)
    results_num=re.findall('\d.*\d',text[0].text)
    results_num=int(re.sub(',','',results_num[0]))
    print(results_num)
    
word_sim_baidu('开心','烦恼')    