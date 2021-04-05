from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os
import requests
import simplejson as json
# import config
import psycopg2
from csv import writer
import re
from collections import OrderedDict
from csv import writer
import pandas as pd

def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", str(tweet)).split())

def Twitter_filter():
    title_list = []
    artist_list = []
    try:
        conn = psycopg2.connect('dbname=kasturivartak user=kasturivartak host=localhost')
        cur = conn.cursor()
        postgreSQL_select_Query = "select * from DS_project.Twitter_filtered"
        cur.execute(postgreSQL_select_Query)
        
        rec = cur.fetchall()
        for row in rec:
            array = []
            created_at = row[0]
            tweet_id = row[1]
            tweet = row[2]
            today_date = row[3]            
            present_hashtags = row[4]
            present_mentions = row[5]
            array.extend((created_at,tweet_id,tweet,today_date,present_hashtags,present_mentions))
            with open('filtered_twitter.csv', 'a+', newline='') as write_obj:
                csv_writer = writer(write_obj)
                csv_writer.writerow(array)
    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL", error)
    cur.close()
    print("conn closed")

def fun():
    sia = SentimentIntensityAnalyzer()
    df = pd.read_csv('filtered_twitter.csv', names=['created_at','tweet_id','tweet','today_date','present_hashtags','present_mentions','positive','negative','neutral','compound'])
    # print(df.head())
    for index,row in df.iterrows():
        tweet_text = df.at[index,'tweet']
        tweet = clean_tweet(tweet_text)
        polarity = sia.polarity_scores(tweet)
        pos = polarity["pos"]
        neu = polarity["neu"]
        neg = polarity["neg"]
        comp = polarity["compound"]
        
        df.at[index,'positive'] = pos
        df.at[index,'negative'] = neg
        df.at[index,'neutral'] = neu
        df.at[index,'compound'] = comp
    print(df.head())
    df.to_csv('file_name.csv', index=False)


fun()