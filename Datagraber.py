#!/usr/bin/env python
# coding: utf-8

# In[1]:


import urllib3
import json
import pickle as pk
import time
from bs4 import BeautifulSoup
import datetime
import dateutil.relativedelta as dr
import pandas as pd
from urllib import request


# In[2]:


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


# In[3]:


http = urllib3.PoolManager()
ohlcurl='https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&interval=5min&apikey=46O5MSJ0J745T9J8&outputsize=full&symbol='
macdurl='https://www.alphavantage.co/query?function=MACDEXT&interval=5min&series_type=open&apikey=46O5MSJ0J745T9J8&symbol='
symbols=['TSLA','AAPL','GOOG','AMZN','AMD','HPQ','INTC','ARM']


# In[4]:


class Symbol:
    def __init__(self,data,tick):
        self.tick=tick
        self.data=data
    def from_url(ohlcurl,macdurl, interval,tick):
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


# In[5]:


#class Manager:
#    def __init__():


# In[6]:


#symbolsdata=[Symbol.from_url(ohlcurl+x,macdurl+x,'5min',x)for x in symbols]


# In[7]:


with open('/home/sergio/github/algotrader/sdata.pkl','rb') as f:
    symbolsdata=pk.load(f)


# In[8]:


[x.update(ohlcurl+x.tick,macdurl+x.tick,'5min') for x in symbolsdata]


# In[9]:


len(symbolsdata[0].data)


# In[10]:


with open('/home/sergio/github/algotrader/sdata.pkl','wb') as f:
    pk.dump(symbolsdata,f)


# In[ ]:
