from utilities import News, Stock
import pandas as pd
import csv


URL = "https://newsapi.org/v2/everything"
NEWS_API = "fa05e0f7c5004f6eae0cce6cd6c18b3c"
QUERRY = "Tesla"

def get_news():
    for i in range(50):
        page = i + 1
        params = {
            "q": QUERRY,
            "apiKey": NEWS_API,
            "from": "2022-09-06",
            "to": "2022-10-05",
            "language": "en",
            "sortBy": "popularity",
            "page": page,
        }
        news = News(URL, NEWS_API, params)
        if page == 1:
            news.save_to_csv()
        else:
            news.save_to_csv(append=True)
    return "News updated!"

news_df = pd.read_csv("articles.csv")

tsl = Stock("TSLA")
tsl_close = tsl.close_df
tsl_close.to_csv("tsl_close.csv", index=False)

train_df = news_df.merge(tsl_close, on="date", how="inner")
print(train_df.describe(include=["category"]))
train_df.to_csv("train.csv", index=False)

test_df = train_df.sample(frac=0.1, random_state=42)
test_df.to_csv("test.csv", index=False)


