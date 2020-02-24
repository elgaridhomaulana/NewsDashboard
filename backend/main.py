from fastapi import FastAPI, Body
from starlette.middleware.cors import CORSMiddleware
from create_plot2 import Hot_News
from create_plot import create_data_plot
from last_new import newest_news
from datetime import datetime
import pandas as pd

app = FastAPI()

origins = [
    "http://localhost:3001"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/hot_topic/{num_topics}/{start_date}/{end_date}')
async def hot_topic(num_topics: int, start_date: str, end_date: str):
    df_hot_news = Hot_News(start_date, end_date, num_topics)
    df_hot_news.reset_index(inplace=True)
    df_hot_news['index'] = df_hot_news['index'].apply(
        lambda ser: ser.strftime('%Y-%m-%d'))
    return df_hot_news.to_dict('records')


@app.get('/hot_topic2/{num_topics}/{start_date}/{end_date}')
async def hot_topic2(num_topics: int, start_date: str, end_date: str):
    df = create_data_plot(start_date, end_date, num_topics)
    return df.to_dict('records')


@app.get('/newest/{start_date}/{end_date}/{word}')
async def newest(start_date: str, end_date: str, word: str):
    newest = newest_news(start_date, end_date, word)
    return newest
