import os
import numpy as np
import pandas as pd
import pickle as pk
from Symbol import Symbol
from multiprocessing import Pool
import time

class Merger:
    def string_to_epoch(timestamp,arr, n):
        [date,t]=timestamp.split()
        date=[int(x) for x in date.split('-')]
        t=[int(x) for x in t.split(':')]

        if((date[1]<=3 and date[2]<=29 and t[0]<=2 and t[1]<=0)):
            tmz='CET'
        elif(date[1]>=10 and date[2]>=29 and t[0]>=3 and t[1]>=0):
            tmz='CET'
        elif(date[1]>=10 and date[2]>=29):
            try:
                prev=arr[n-12]
                [pdate,ptime]=prev.split()
                pdate=[int(x) for x in pdate.split('-')]
                ptime=[int(x) for x in ptime.split(':')]
                if(t[0]==ptime[0]):
                    tmz='CET'
                else:
                    tmz='CEST'
            except:
                futr=arr[n+12]
                [fdate,ftime]=prev.split()
                fdate=[int(x) for x in fdate.split('-')]
                ftime=[int(x) for x in ftime.split(':')]
                if(t[0]==ftime[0]):
                    tmz='CEST'
                else:
                    tmz='CET'
        else:
            tmz='CEST'


        return int(time.mktime(time.strptime(timestamp+' '+tmz,'%Y-%m-%d %H:%M %Z')))
    def load(path):
        files=[y for y in os.listdir(path)  if '.pkl' in y]
        print(path, files)
        objects=[pk.load(open(path+y,'rb'))[0] for y in files]
        data=[[[pd.DataFrame(x.data).transpose(),x.tick,pd.DataFrame(x.data).transpose().index]for x in y] for y in objects]
        datadic={}
        for file in data:
            for symbol in file:
                index=[Merger.string_to_epoch(x,symbol[0].index.tolist(),n) 
                       for x,n in zip(symbol[0].index.tolist(), 
                                      [n for n in range(len(symbol[0].index.tolist()))])]
                symbol[0].index=index
                if(symbol[1] not in datadic.keys()):
                    datadic[symbol[1]]=[symbol[0]]
                else:
                    datadic[symbol[1]]+=[symbol[0]]
        return datadic
    def merge_ticker(arg):
        [arr,ticker]=arg
        columns=[ticker+' '+x.replace('1.','').replace('2.','').replace('3.','').replace('4.','').replace('5.','').replace(' M','M')
                 for x in arr[0].columns]
        df=pd.DataFrame(columns=columns)
        for file in arr:
                for index in file.index:
                    if(index not in df.index):
                        df=df.append(pd.DataFrame(data=[file.loc[index].tolist()],index=[index],columns=columns))
        print(True in df.duplicated())
        return df.sort_index()
    def gen_df(path,fillna=None):
        startt=time.time()
        print('loading')
        data = Merger.load(path)
        tickers=list(data.keys())
        ltime=time.time()
        print(ltime-startt)
        print('merging tickers')
        with Pool(4) as p:
            dfs=p.map(Merger.merge_ticker,zip([data[ticker] for ticker in tickers],tickers))
        print(time.time()-ltime)
        if(fillna==None):
            fillna=-10000
        maindf=dfs[0]
        for df in dfs[1:]:
            for column in df.columns:
                maindf[column]=df[column]
        return maindf.fillna(fillna).astype(float)