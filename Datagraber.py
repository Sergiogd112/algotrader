#!/usr/bin/env python
# coding: utf-8

# In[13]:


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


class Symbol:
    def __init__(self,data,tick):
        self.tick=tick
        self.data=data
    def from_url(ohlcurl,macdurl, interval,tick):
        ohlctmp=json.loads(http.request('GET', ohlcurl).data)
        print(ohlctmp.keys())
        try:
            ohlcdata=ohlctmp['Time Series ('+interval+')']
        except Exception as e:
            print(ohlctmp(list(ohlctmp.keys())[0]))
            print(e.traceback)
        time.sleep(12)
        try:
            macddata=json.loads(http.request('GET',macdurl).data)['Technical Analysis: MACDEXT']
        except:
            print(json.loads(http.request('GET',macdurl).data))
        data={}
        print(len(ohlcdata))
        for keyo,keym in zip(list(ohlcdata.keys()),list(macddata.keys())):
            if(keyo[:-3] in list(macddata.keys())):
                data[keyo[:-3]]={**ohlcdata[keyo],**macddata[keyo[:-3]]}
        time.sleep(12)
        return Symbol(data,tick)
    def update(self,ohlcurl,macdurl,interval):
        ohlctmp=json.loads(http.request('GET', ohlcurl).data)
        print(ohlctmp.keys())
        ohlcdata=ohlctmp['Time Series ('+interval+')']
        time.sleep(12)
        try:
            macddata=json.loads(http.request('GET',macdurl).data)['Technical Analysis: MACDEXT']
        except:
            print(json.loads(http.request('GET',macdurl).data))
        data={}

        print(len(ohlcdata))
        for keyo,keym in zip(list(ohlcdata.keys()),list(macddata.keys())):
            if(keyo[:-3] in list(macddata.keys())):
                data[keyo[:-3]]={**ohlcdata[keyo],**macddata[keyo[:-3]]}
        time.sleep(12)
        for key in list(data.keys()):
            if(not(key in list(self.data.keys()))):
                self.data[key]=data[key]


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

    time.sleep(sl)

# In[39]:


#'_'.join(time.ctime().split())


# In[ ]:




