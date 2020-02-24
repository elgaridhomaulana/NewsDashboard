import pandas as pd
import numpy as np
import json
import re
from datetime import timedelta, date

with open('tempo.json', encoding='utf-8') as tempo:
    data = json.load(tempo)

df = pd.DataFrame(data)
df['tags_string'] = df['tags'].apply(
    lambda ser: ' '.join(ser).lower().replace("'", ' '))

df.loc[1766, 'date'] = 'Rabu, 12 February 2020 16:19 WIB'

monthChanger = {
    'Januari': 'January',
    'January': 'January',
    'Februari': 'February',
    'February': 'February',
    'Maret': 'March',
    'March': 'March',
    'April': 'April',
    'Mei': 'May',
    'May': 'May',
    'Juni': 'June',
    'June': 'June',
    'Juli': 'July',
    'July': 'July',
    'Agustus': 'August',
    'August': 'August',
    'September': 'September',
    'Oktober': 'October',
    'October': 'October',
    'November': 'November',
    'Desember': 'December',
    'December': 'December'
}

monthChanger2 = {
    'Jan': '01',
    'Feb': '02',
    'Mar': '03',
    'Apr': '04',
    'May': '05',
    'Jun': '06',
    'Jul': '07',
    'Aug': '08',
    'Sep': '09',
    'Oct': '10',
    'Nov': '11',
    'Dec': '12'
}

# Merubah kolom tanggal
df['hari'] = df['date'].apply(lambda ser: ser.split(',')[0])
df['tanggal'] = df['date'].apply(
    lambda ser: ser.split(',')[1].replace('WIB', ''))
df['tanggal'] = df['tanggal'].apply(lambda ser: ser.replace(re.search(
    '[A-Za-z]+', ser).group(0), monthChanger[re.search('[A-Za-z]+', ser).group(0)]))
df['tanggal'] = df['tanggal'].apply(lambda ser: ser.strip())
df['tanggal'] = pd.to_datetime(df['tanggal'], format='%d %B %Y %H:%M')
df.set_index(df['tanggal'], inplace=True)


def splice_df(start_date, end_date):
    df_splice_date = df[start_date:end_date]
    return df_splice_date


def contain_tag(df_splice_date, word):
    df_contain_word = df_splice_date[df_splice_date['tags_string'].str.contains(
        word)]
    df_contain_word = df_contain_word.sort_index(ascending=False)
    return df_contain_word


def take_first_news(df_contain_word):
    for i in range(len(df_contain_word)):
        if df_contain_word.iloc[i].contentRaw != [' ']:
            return df_contain_word.iloc[i]


def newest_news(start_date, end_date, word):
    df_splice_date = splice_df(start_date, end_date)
    df_contain_word = contain_tag(df_splice_date, word)
    newest = take_first_news(df_contain_word)
    return newest
