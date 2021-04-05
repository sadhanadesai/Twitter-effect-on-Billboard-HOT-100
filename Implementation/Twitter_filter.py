import os
import requests
import simplejson as json
import config
import psycopg2
from csv import writer
import re
from collections import OrderedDict


def Twitter_filter():
    title_list = []
    artist_list = []
    try:
        conn = psycopg2.connect('dbname=kasturivartak user=kasturivartak host=localhost')
        cur = conn.cursor()
        sql = "SELECT title,artist FROM DS_project.Billboard"
        cur.execute(sql)
        rec = cur.fetchall()
        
        for row in rec:
            title = re.sub(r"\s+", "", str(row[0],), flags=re.UNICODE)
            title_list.append(title)
            artists = row[1].split(",")
            if(len(artists) > 0):
                for artist in artists:
                    # artist=artist.replace(" ","")
                    artist = re.sub(r"\s+", "", str(artist), flags=re.UNICODE)
                    artist_list.append(artist)
            

    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL", error)
   
    cur.close()
    conn.close()
    title_list = list(OrderedDict.fromkeys(title_list))
    artist_list = list(OrderedDict.fromkeys(artist_list))
    # print(len(title_list))
    # print(len(artist_list))
    # print("\n\n\n\n")
    # print(title_list)
    # print("\n\n\n\n")
    # print(artist_list)
    print("PostgreSQL connection is closed for Billboard")

    try:
        conn = psycopg2.connect('dbname=kasturivartak user=kasturivartak host=localhost')
        cur = conn.cursor()

        postgreSQL_select_Query = "select * from DS_project.Twitter"
        
        cur.execute(postgreSQL_select_Query)
        
        rec = cur.fetchall()
        for row in rec:
            hash_flag = 0 # Inititlly False
            mention_flag = 0 # Inititlly False
            arr=[]
            
            created_at = row[0]
            tweet_id = row[1]
            tweet = row[2]
            annotations = row[6]
            hashtags = row[7]
            mention = row[8]

            today_date = created_at.split('T')[0]

            hashtags = re.sub(r'[{}]', '', hashtags)
            hashtags_list = []
            if(hashtags != ""):
                hashtags_list = hashtags.split(",")

            mention = re.sub(r'[{}]', '', mention)
            mention_list = []
            if(mention != ""):
                mention_list = mention.split(",")

            present_hashtags = []
            if(len(hashtags_list)>0):
                for hash in hashtags_list:
                    if(hash in title_list or hash in artist_list):
                        present_hashtags.append(hash)
                        hash_flag = 1 # True
            present_mentions = []
            if(len(mention_list)>0):
                for m in mention_list:
                    if(m in artist_list):
                        present_mentions.append(m)
                        mention_flag = 1 # True
                              
            arr=[created_at,tweet_id,tweet,today_date,present_hashtags,present_mentions]

            if(hash_flag == 1 or mention_flag==1):
                cur.execute("INSERT INTO DS_project.Twitter_filtered (created_at,tweet_id,tweet,today_date,present_hashtags,present_mentions) VALUES (%s,%s,%s,%s,%s,%s)", (created_at,tweet_id,tweet,today_date,present_hashtags,present_mentions))
        conn.commit()
        print("inserted records")
            # print("\n\n\n")


    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL", error)
    cur.close()
    conn.close()
    print("PostgreSQL connection is closed")


Twitter_filter()
