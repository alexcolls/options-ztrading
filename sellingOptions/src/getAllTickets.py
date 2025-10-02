from src.apis.polygonApi import api_key
import requests
import csv
# get tickers
endpoint = 'https://api.polygon.io/v3/reference/tickers?type=CS&market=stocks&active=true&limit=1000&apiKey=' + api_key 
tickers = []
run = True
while run:
  res = requests.get(endpoint)
  if res.status_code == 200:
    data = res.json()
    for x in data['results']:
      tickers.append(x['ticker'])
    if data['next_url'].startswith('https://api.polygon.io/v3/'):
      endpoint = data['next_url'] +'&apiKey='+ api_key 
    else:
      run = False
      break
  else: 
    print('Response 404')
    break
# save tickers.csv
with open('./src/apis/db/tickers.csv', 'a') as csvfile:
  write = csv.writer(csvfile)
  write.writerow(tickers)
