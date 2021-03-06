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

# In[17]:


#class Manager:
#    def __init__():


# In[18]:


#symbolsdata=[Symbol.from_url(ohlcurl+x,macdurl+x,'5min',x)for x in symbols]


# In[19]:


#with open('sdata.pkl','rb') as f:
#    symbolsdata=pk.load(f)


# In[20]:


#[x.update(ohlcurl+x.tick,macdurl+x.tick,'5min') for x in symbolsdata]


# In[21]:


#len(symbolsdata[0].data)


# In[10]:


#with open('sdata.pkl','wb') as f:
 #   pk.dump(symbolsdata,f)


# In[34]:


#len(list(symbolsdata[0].data.keys()))/(12*24)


# In[23]:


#symbolsdata[0].data[list(symbolsdata[0].data.keys())[-1]]


# In[30]:


#months=[[int(x.split('-')[1]), int(x.split('-')[2].split()[0])] for x in list(symbolsdata[0].data.keys())]


# In[31]:


#min(months)


# In[32]:


#12*24


# In[40]:

sl=3600*24
while True:
    today=[[Symbol.from_url(ohlcurl+x,macdurl+x,'5min',x)for x in symbols]]
    fname='/home/pi/github/algotrader/data/'+'_'.join(time.ctime().split())+'.pkl'
    os.system('echo "" >> '+fname)
    with open(fname,'wb') as f:
        pk.dump(today,f)
    git_push()

    time.sleep(sl)

# In[39]:


#'_'.join(time.ctime().split())


# In[ ]:




