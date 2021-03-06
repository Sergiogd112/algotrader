#!/usr/bin/env python
# coding: utf-8
import urllib3
import json
import pickle as pk
import time
from bs4 import BeautifulSoup
import datetime
import dateutil.relativedelta as dr
import pandas as pd
from urllib import request
import os
from Symbol import Symbol
# In[14]:


def get_constituents():
    # URL request, URL opener, read content
    req = request.Request('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    opener = request.urlopen(req)
    content = opener.read().decode() # Convert bytes to UTF-8

    soup = BeautifulSoup(content)
    tables = soup.find_all('table') # HTML table we actually need is tables[0] 

    external_class = tables[0].findAll('a', {'class':'external text'})

    tickers = []

    for ext in external_class:
        if not 'reports' in ext:
            tickers.append(ext.string)

    return tickers


# In[15]:


http = urllib3.PoolManager()
ohlcurl='https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&interval=5min&apikey=46O5MSJ0J745T9J8&outputsize=full&symbol='
macdurl='https://www.alphavantage.co/query?function=MACDEXT&interval=5min&series_type=open&apikey=46O5MSJ0J745T9J8&symbol='
symbols=['TSLA','AAPL','GOOG','AMZN','AMD','INTC','F']


# In[16]:
from git import Repo

PATH_OF_GIT_REPO = r'.git'  # make sure .git folder is properly configured
COMMIT_MESSAGE = 'update'

def git_push():
    try:
        repo = Repo(PATH_OF_GIT_REPO)
        repo.git.add(update=True)
        repo.index.commit(COMMIT_MESSAGE)
        origin = repo.remote(name='origin')
        origin.push()
    except:
        print('Some error occured while pushing the code')    


sl=3600*24
while True:
    today=[[Symbol.from_url(ohlcurl+x,macdurl+x,'5min',x)for x in symbols]]
    fname='/home/sergio/github/algotrader/data/'+'_'.join(time.ctime().split())+'.pkl'
    with open(fname,'w+') as f:
        pk.dump(today,f)
    print('done')
    git_push()

    time.sleep(sl)


