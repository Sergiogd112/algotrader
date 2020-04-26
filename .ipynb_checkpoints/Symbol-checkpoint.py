import json
import urllib3
import time

http = urllib3.PoolManager()
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