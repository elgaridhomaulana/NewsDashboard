import pandas as pd
import numpy as np
import json
import re
from datetime import timedelta, date

with open('tempo.json', encoding='utf-8') as tempo:
    data = json.load(tempo)

df = pd.DataFrame(data)
df['tags_string'] = df['tags'].apply(lambda ser: ' '.join(ser).lower())

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


def series_top_topic(df_splice_date, n_topic):
    all_tags = []
    for tag in df_splice_date['tags']:
        all_tags += [item.lower() for item in tag]
    series_top = pd.Series(all_tags).value_counts().head(n_topic)
    return series_top


def daterange(date1, date2):
    for n in range(int((date2 - date1).days)+1):
        yield date1 + timedelta(n)


def create_data(start_date, end_date, series_top):
    year_start, month_start, date_start = int(start_date.split(
        '-')[0]), int(start_date.split('-')[1]), int(start_date.split('-')[2])
    year_end, month_end, date_end = int(end_date.split(
        '-')[0]), int(end_date.split('-')[1]), int(end_date.split('-')[2])
    start_dt = date(year_start, month_start, date_start)
    end_dt = date(year_end, month_end, date_end)
    dict_semua = {}
    for dt in daterange(start_dt, end_dt):
        #     print(dt.strftime("%Y-%m-%d"))
        ls_jumlah = []
        for topic in series_top.index:
            ls_jumlah.append(
                sum(df[dt.strftime('%Y-%m-%d')]['tags_string'].str.contains(topic)))
        dict_semua[dt.strftime('%Y-%m-%d')] = ls_jumlah

    df_time_series = pd.DataFrame(dict_semua).transpose()
    df_time_series.columns = series_top.index
    df_time_series.index = pd.to_datetime(df_time_series.index)
    return df_time_series


def Hot_News(start_date, end_date, n_topic):
    df_splice_date = splice_df(start_date, end_date)
    series_top = series_top_topic(df_splice_date, n_topic)
    df_time_series = create_data(start_date, end_date, series_top)
    return df_time_series
