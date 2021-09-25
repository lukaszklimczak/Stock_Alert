import requests
from twilio.rest import Client
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

STOCK_API_key = os.environ.get("STOCK_API_key")
NEWS_API_key = os.environ.get("NEWS_API_key")
account_sid = os.environ.get("account_sid") #regards to twilio account
auth_token = os.environ.get("auth_token") #regards to twilio account

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"


stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "outputsize": "compact",
    "apikey": STOCK_API_key
}

news_parameters = {
    "q": COMPANY_NAME,
    "apiKey": NEWS_API_key
}

response = requests.get(url="https://www.alphavantage.co/query?", params=stock_parameters)
response.raise_for_status()
data = response.json()
data = data["Time Series (Daily)"]
days = list(data)[:2]
last_data = float(data[days[0]]["4. close"])
prelast_data = float(data[days[1]]["4. close"])
value = round((last_data - prelast_data)/prelast_data * 100, 2)

run_alert = False
selected_articles = []

if value >= 2 or value <= -2:
    run_alert = True
    news = requests.get(url="https://newsapi.org/v2/everything?", params=news_parameters)
    news.raise_for_status()
    all_articles = news.json()
    for i in range(3):
        selected_article = {}
        selected_article["Headline"] = all_articles["articles"][i]["title"]
        selected_article["Content"] = all_articles["articles"][i]["description"]
        selected_articles.append(selected_article)

if run_alert:
    for i in range(len(selected_articles)):
        client = Client(account_sid, auth_token)
        if value >= 2:
            message = client.messages \
                .create(
                body=f"{STOCK} 🔺{value}%\n"
                     f'HEADLINE: {selected_articles[i]["Headline"]}\n'
                     f'Brief: {selected_articles[i]["Content"]}',
                from_='+19285998325',
                to='+48512921263'
            )

        elif value <= -2:
            message = client.messages \
                .create(
                body=f"{STOCK} 🔻{value}%\n"
                     f'HEADLINE: {selected_articles[i]["Headline"]}\n'
                     f'Brief: {selected_articles[i]["Content"]}',
                from_='+19285998325',
                to='+48512921263'
            )
