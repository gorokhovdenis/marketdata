import requests
import json
import datetime
import psycopg2
import time
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import pytz
import re

def coincap():
    # This example uses Python 2.7+ and the python-request library
    from requests import Request, Session
    from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
    import json
    import os

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '3',
        'limit': '1',
        'convert': 'USD',
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': os.environ.get("coinmarketcap_token", None),
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        return data['data'][0]['quote']['USD']['price']
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return e

def coincap_btc_percent():
    try:
        req = Request('https://coinmarketcap.com/', headers={'User-Agent': 'Mozilla/55.0'})
        page=urlopen(req).read()
        soup = BeautifulSoup(page,"html.parser")
        text = soup.find("tr", {"id":"id-bitcoin"})
        reg1=(re.search(r'data-percentusd=\".+?(?=\")', str(text)))
        reg=(re.search(r'(?<=\")\S*',reg1[0]))
        link = reg[0]
        return link
    except Exception:
        pass


while True:
    msk = pytz.timezone('Europe/Moscow')
    time_def = datetime.datetime.now()
    now_t=str(msk.localize(time_def))[:-13]
    #BITTREX-XRP
    url1='https://api.bittrex.com/api/v1.1/public/getticker?market=USD-XRP'
    r1 = requests.get(url1)
    json_data=json.loads(r1.text)
    btrx_xrp=json_data['result']['Last']
    #BITTREX-BTC
    url2='https://api.bittrex.com/api/v1.1/public/getticker?market=USD-BTC'
    r2 = requests.get(url2)
    json_data2=json.loads(r2.text)
    btrx_btc=json_data2['result']['Last']
    #CEXIO
    url3='https://cex.io/api/ticker/XRP/USD'
    r3 = requests.get(url3)
    json_data3=json.loads(r3.text)
    cex_xrp=json_data3['last']
    #COINDESKAPI
    url4='https://api.coindesk.com/v1/bpi/currentprice.json'
    r4 = requests.get(url4)
    json_data4=json.loads(r4.text)
    coindesk_btc=json_data4['bpi']['USD']['rate_float']

    #INSERT INTO DB
    try:
        connection = psycopg2.connect(user="postgres",
                                        #password="pynative@#29",
                                        host="postgres-server",
                                        port="5432",
                                        database="postgres")
        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO transactions (cexio_xrp, bittrex_xrp, bittrex_btc, coindesk_btc, coinmarketcap_btc, time)
        VALUES (%s,%s,%s,%s,%s,%s)"""
        record_to_insert = (cex_xrp, btrx_xrp, btrx_btc, coindesk_btc, coincap_btc_percent(), now_t)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        count = cursor.rowcount
        print (count, "Record inserted successfully into transactions table")
    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to insert record into transactions table", error)
    try:
        postgreSQL_select_Query = "select * from transactions"
        cursor.execute(postgreSQL_select_Query)
        print("Selecting rows from transactions table using cursor.fetchall")
        mobile_records = cursor.fetchall() 

        print("Print each row and it's columns values")
        for row in mobile_records:
            print("Id",row[0]," |  cex_XRP = ", row[1],"  |  btrx_XRP  = ", row[2], "  |  btrx_BTC", row[3]," | cndsk_BTC ", row[4],"  |  % ", row[5],"  |  ", row[6],"\n")
    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL", error)
    time.sleep(10)

# finally:
#     #closing database connection.
#     if(connection):
#         cursor.close()
#         connection.close()
#         print("PostgreSQL connection is closed")
    