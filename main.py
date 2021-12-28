STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

stock_api_key = 'FJTIZV81C783NPZD'
news_api_key = "32902feee24b41fbbc9d5fe47a159605"

Twilio_SID = "ACdd079257318b0fbe0277341b15f95c26"
Twilio_Auth = "6f937382f856b91c25a767d88a29a02a"

import requests
from twilio.rest import Client
 

stock_params = {
    "function" : "TIME_SERIES_DAILY",
    "symbol" : STOCK_NAME,
    "apikey" : stock_api_key
    }

response = requests.get(STOCK_ENDPOINT, stock_params)

data = response.json()["Time Series (Daily)"]
data_list = [value for (key,value) in data.items()]

yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]

day_before_yesterday = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday["4. close"]

difference = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
diff_percent = (difference/ float(yesterday_closing_price))*100


if diff_percent > 1:
    new_params = {
        "apiKey": news_api_key,
        "qInTitle": COMPANY_NAME,
        
        }
    news_response = requests.get(NEWS_ENDPOINT, new_params)
    articales = news_response.json()['articles']
    three_articales = articales[:3]
    
    
    articales_formatted = [f"Headline :{article ['title']}. \nBrief : {article ['description']}" for article in three_articales]
    print(articales_formatted)
    client = Client(Twilio_SID, Twilio_Auth)

    for article in articales_formatted:
        message = client.messages.create(
        to="+97433476222", 
        from_="+12542523157",
        body=article)




#TODO 9. - Send each article as a separate message via Twilio. 




#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

