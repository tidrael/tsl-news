from datetime import datetime as dt
import requests
import pandas as pd
import numpy as np


def convert_date(date):
    return dt.fromtimestamp(date).strftime("%Y-%m-%d")


class Stock:
    """
    """

    def __init__(self, ticker="^DJI"):
        self.ticker = ticker
        self.url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v3/get-historical-data"
        self.querstring = {"symbol": self.ticker, "region": "US"}
        self.headers = {
            "X-RapidAPI-Key": "95848cb9e5mshe6ee8a9438ed637p165d5fjsn4a84d0d55dca",
            "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com",
        }
        self.response = requests.get(
            self.url, headers=self.headers, params=self.querstring
        ).json()
        self.prices = self.response["prices"]
        self.bins = [-np.inf, 0, np.inf]
        self.labels = ["negative", "positive"]
        self.get_close()
        self.get_dates()
        self.make_sentiment()
        
    def get_dates(self):
        self.dates = [convert_date(i["date"]) for i in self.prices]
    
    def make_sentiment(self):
        self.close_df = pd.DataFrame({"date": self.dates, "close": self.close})
        self.close_df["pct_change"] = round(
            self.close_df["close"].pct_change(periods=-1) * 100, 2
        )
        self.close_df["label"] = pd.cut(self.close_df["pct_change"], bins=self.bins, labels=self.labels)
        
    def get_close(self):
        self.close = []
        for i in self.prices:
            try:
                close = round(i["close"], 2)
            except KeyError:
                close = None
            self.close.append(close)

    def __repr__(self):
        return self.ticker


class News:
    def __init__(self, url, api_key, params):
        self.url = url
        self.api_key = api_key
        self.params = params
        self.response = requests.get(self.url, params=self.params)
        self.response.raise_for_status()
        self.articles = self.response.json()["articles"]
        self.articles_list = [
            {"title": article["title"], "date": article["publishedAt"][:10]}
            for article in self.articles
        ]
        self.articale_df = pd.DataFrame(self.articles_list)

    def save_to_csv(self, append=False):
        self.articale_df.to_csv(
            "articles.csv", index=False, mode="a" if append else "w"
        )
