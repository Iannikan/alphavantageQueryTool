import requests
import json
import sys
import time
import os
from decouple import config 



startIndex = len(next(os.walk('./prices'))[2]) #number of existing files
key = config('KEY')
sessionCeiling = 500

def writeToFile(data, fileName):
  with open(fileName, 'w+') as f:
    json.dump(data,f)

with open('symbols.json') as symbolsFile:
  symbols = json.load(symbolsFile)
  for i in range(startIndex, min(startIndex + sessionCeiling, len(symbols))):
    resp = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbols[i]}&outputsize=full&apikey={key}')
    respData = resp.json()
    code = resp.status_code
    print(json.dumps(respData))
    if 'Note' in respData: 
      print(json.dumps(respData))
      raise ValueError (f'Rate limited, aborting')
    symbol = respData['Meta Data']['2. Symbol']
    timeSeries = respData['Time Series (Daily)']
    compObj = {'ticker_symbol': symbol, 'daily_time_series_data': timeSeries}
    writeToFile(compObj, f'./prices/{symbols[i]}.json')
    time.sleep(12) #stop because of rate limiting
