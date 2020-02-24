import pandas as pd
import json
import re
from datetime import date, timedelta

FILENAME ='tempo.json'
CACHE_DATE_START=''
CACHE_DATE_END=''

d = {
    "Januari":"1",
    "January":"1",
    "Februari":"2",
    "February":"2",
    "Maret":"3",
    "March":"3",
    "April":"4",
    "Mei":"5",
    "May":"5",
    "Juni":"6",
    "June":"6",
    "Juli":"7",
    "July":"7",
    "Agustus":"8",
    "August":"8",
    "September":"9",
    "Oktober":"10",
    "October":"10",
    "November":"11",
    "Desember":"12",
    "December":"12"
    }
#DATE_START = date(2020, 1, 1)
#DATE_END = date(2020, 1, 31)


#change string month to date
def ganti_bulan(string, dictionary):
    for item in dictionary.keys():
        # sub item for item's paired value in string
        string = re.sub(item, dictionary[item], string)
    return string

#import data
def import_data(filename,DATE_START,DATE_END):

    #import data
    with open(filename, encoding='utf-8') as tempo:
        data = json.load(tempo)
    df = pd.DataFrame(data)

    #change string to datetime format
    df["date_norm"] = df.date.map(lambda x:ganti_bulan(x.split(',')[-1],d).lstrip(" "))
    df["date_norm"]= pd.to_datetime(df["date_norm"], format="%d %m %Y %H:%M WIB") #y m d 
    df.set_index('date_norm', inplace=True)
    df["num_index"] = [x for x in range(len(df))]
    df = df[str(DATE_START):str(DATE_END)]
    return df

#preporcessing list tag
def join_list_tags(df):
    #join multiple word tag with '+'
    df['tags']=df.tags.apply(lambda ser: [re.sub(r"[^a-zA-Z0-9]+", ' ', item) for item in ser])
#     df['tags']=df.tags.apply(lambda ser: [item.replace(' ', '+') for item in ser])
#     re.sub(r"[^a-zA-Z0-9]+", ' ', k)

    #create string tag from list tag word
    df['tags_string'] = df['tags'].apply(lambda ser: ' '.join(ser).lower())
    return df

#mencari urutan tag yang sering muncul
def series_top_topic(df_splice_date):
    all_tags = []
    for tag in df_splice_date['tags']:
        all_tags += [item.lower() for item in tag]
    series_top = pd.Series(all_tags).value_counts()
    return series_top

dict_topic={}
#find topic group
def find_topic_group(df,NUM_TOPIC):
    global dict_topic
    print('series top topic')
    stt = series_top_topic(df)

#     NUM_TOPIC =10
    TOP_TOPIC_GROUP = []
    TOP_TOPIC = []
    checker=[]
    root_checker=[]

    
    for itr in range(len(stt)):
        if (stt.index[itr] in dict_topic) and (df.num_index.get(dict_topic[stt.index[itr]].num_index) is not None):
            root_topic = dict_topic[stt.index[itr]]
        
        else:
            #find root tag (jumlah tag terpanjang berdasarkan jumlah kata dlm tag terbanyak)
            df_contain = df[df["tags_string"].str.contains(stt.index[itr])][['tags','tags_string','num_index']]
            df_contain_tag_sum = df_contain.tags.apply(lambda x : len(x))
            df_contain["tag_sum"] = df_contain_tag_sum;
            topic = pd.DataFrame(df_contain.sort_values(by='tag_sum', ascending=False))
            root_topic = topic.iloc[0]
            dict_topic.update({stt.index[itr]:root_topic})

        #sort topic
        root_tag_num = root_topic.num_index

        #list tag terpanjang
        source = list(root_topic.tags)
        if (root_tag_num not in checker) and not any(elem in root_checker  for elem in source) :
            #menyimpan list tag agar tidak dicari lagi tag yg sama
            root_checker.extend(source)
            
            #mencari seluruh row yang mengandung tag dari root
            temp = df[df["tags_string"].str.contains('|'.join(source),case=False)]
            
            #menyimpan root topic
            TOP_TOPIC.append([len(temp),source,stt.index[itr]])
            checker.append(root_tag_num)

            #menyimpan seluruh row
            TOP_TOPIC_GROUP.append(temp)
            
            #berhenti jika jumlah topic telah terpenuhi
            if len(TOP_TOPIC_GROUP) == NUM_TOPIC:
                break
    #return dataframe [banyak berita, tag terbanyak, kata kunci]
    TOP_TOPIC = pd.DataFrame(TOP_TOPIC, columns=['sum_news','tag_group','stt']).sort_values(by='sum_news', ascending=False)
    return TOP_TOPIC, TOP_TOPIC_GROUP

CDS = ''
CDE = ''
CTT = []
CTTP =[]

import time


def Hot_Topics(DATE_START:str = '2020-1-1', DATE_END:str = '2020-1-10',NUM_TOPIC:int = 10):
    global CDS 
    global CDE
    global CTT
    global CTTG
    
    
    #setup dataframe
    if (DATE_START == CDS) and (DATE_END == CDE):
        return CTT[:NUM_TOPIC], CTTG[:NUM_TOPIC]
    
    df = import_data(FILENAME,DATE_START,DATE_END)
    df = join_list_tags(df)

    start_time = time.time()
    #find topic group
    TOP_TOPIC, TOP_TOPIC_GROUP = find_topic_group(df,10)
    print("--- %s seconds ---" % (time.time() - start_time))
    
    CDS = DATE_START
    CDE = DATE_END
    CTT = TOP_TOPIC
    CTTG = TOP_TOPIC_GROUP
    
    
    return TOP_TOPIC[:NUM_TOPIC], TOP_TOPIC_GROUP[:NUM_TOPIC]


def daterange(date1, date2):
    for n in range(int((date2 - date1).days)+1):
        yield date1 + timedelta(n)
        
def create_data_plot(start_date, end_date,NUM_TOPIC):
    TOP_TOPIC, TOP_TOPIC_GROUP = Hot_Topics(start_date,end_date,NUM_TOPIC)
    #split date start
    year_start, month_start, date_start = int(start_date.split(
        '-')[0]), int(start_date.split('-')[1]), int(start_date.split('-')[2])
    
    #split date end
    year_end, month_end, date_end = int(end_date.split(
        '-')[0]), int(end_date.split('-')[1]), int(end_date.split('-')[2])
    
    start_dt = date(year_start, month_start, date_start)
    end_dt = date(year_end, month_end, date_end)
#     print('as')
    dict_semua = {}
    for dt in daterange(start_dt, end_dt):
        ls_jumlah = []

        for topic in TOP_TOPIC_GROUP:
            ls_jumlah.append(
                len(topic[topic.index.date == dt]))
        dict_semua[dt.strftime('%Y-%m-%d')] = ls_jumlah

    df_time_series = pd.DataFrame(dict_semua).transpose()
    df_time_series.columns = TOP_TOPIC.stt
    df_time_series.index = pd.to_datetime(df_time_series.index)
    df_time_series['index']=pd.to_datetime(df_time_series.index.date)
#     print(df_time_series)
    return df_time_series
# create_data_plot('2020-1-1','2020-2-28',5)