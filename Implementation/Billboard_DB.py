
import psycopg2
from csv import writer
import pandas as pd

conn = psycopg2.connect('dbname=kasturivartak user=kasturivartak host=localhost')
cur = conn.cursor()

df = pd.read_csv ('Billboard.csv')
for row in df.itertuples():
    title=row[1]
    artist=row[2] 
    peakPos=row[3] 
    lastPos=row[4] 
    weeks=row[5] 
    rank=row[6] 
    isNew=row[7] 
    today_date=row[8] 
    array=[]
    # array.extend((title, artist, peakPos, lastPos, weeks, rank, isNew, today_date))
    array = [title, artist, peakPos, lastPos, weeks, rank, isNew, today_date]
    

    cur.execute("INSERT INTO DS_project.Billboard (title, artist, peakPos, lastPos, weeks, rank, isNew, timestamp) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (title, artist, peakPos, lastPos, weeks, rank, isNew, today_date))
conn.commit()
conn.close()