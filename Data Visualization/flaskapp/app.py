from flask import Flask
from flask import render_template
import matplotlib.pyplot as plt
import pandas as pd
import io
from datetime import datetime
import sys
import base64
from flask import request
from flask import Markup
from flask import Flask, Markup, render_template
import pandas as pd

app = Flask(__name__)


colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]

@app.route('/',methods=['POST','GET'])
def default():
    return render_template('error.html')

@app.route('/sentiment',methods=['POST','GET'])
def sentiment():
    if 'sentiment_type' in request.args:
        sentiment_type = request.args.get('sentiment_type')
        if sentiment_type == 'positive':
            df = pd.read_csv('combined.csv')
            df = df.sort_values(by=['combine_pos_cnt'], ascending=False)
            title = df['Title'].values.tolist()
            positive = df['combine_pos_cnt'].values.tolist()
            negative = []
            neutral = []
            if 'start_percent' in request.args and 'end_percent' not in request.args:
                start_percent = request.args.get('start_percent')
                start = abs((int(start_percent) / 100) * len(title))
                title = title[int(start):]
                positive = positive[int(start):]
            if 'start_percent' not in request.args and 'end_percent' in request.args:
                end_percent = request.args.get('end_percent')
                end = abs((int(end_percent) / 100) * len(title))
                title = title[:int(end)]
                positive = positive[:int(end)]
            if 'start_percent' in request.args and 'end_percent' in request.args:
                start_percent = request.args.get('start_percent')
                end_percent = request.args.get('end_percent')
                start = abs((int(start_percent) / 100) * len(title))
                end = abs((int(end_percent) / 100) * len(title))
                title = title[int(start):int(end)]
                positive = positive[int(start):int(end)]
                return render_template('stacked_bar.html', title='Positive Sentiment Chart', names=title,positive=positive, negative=negative,neutral=neutral)
            else:
                return render_template('stacked_bar.html', title='Positive Sentiment Chart', names=title,positive=positive, negative=negative,neutral=neutral)
            
        elif sentiment_type == 'neutral':
            df = pd.read_csv('combined.csv')
            df = df.sort_values(by=['combine_neu_cnt'], ascending=False)
            title = df['Title'].values.tolist()
            positive = []
            negative = []
            neutral = df['combine_neu_cnt'].values.tolist()
            if 'start_percent' in request.args and 'end_percent' not in request.args:
                start_percent = request.args.get('start_percent')
                start = abs((int(start_percent) / 100) * len(title))
                title = title[int(start):]
                positive = positive[int(start):]
            if 'start_percent' not in request.args and 'end_percent' in request.args:
                end_percent = request.args.get('end_percent')
                end = abs((int(end_percent) / 100) * len(title))
                title = title[:int(end)]
                positive = positive[:int(end)]
            if 'start_percent' in request.args and 'end_percent' in request.args:
                start_percent = request.args.get('start_percent')
                end_percent = request.args.get('end_percent')
                start = abs((int(start_percent) / 100) * len(title))
                end = abs((int(end_percent) / 100) * len(title))
                title = title[int(start):int(end)]
                neutral = positive[int(start):int(end)]
                return render_template('stacked_bar.html', title='Neutral Sentiment Chart', names=title,positive=positive, negative=negative,neutral=neutral)
            else:
                return render_template('stacked_bar.html', title='Neutral Sentiment Chart', names=title,positive=positive, negative=negative,neutral=neutral)

            
        elif sentiment_type == 'negative':
            df = pd.read_csv('combined.csv')
            df = df.sort_values(by=['combine_neg_cnt'], ascending=False)
            title = df['Title'].values.tolist()
            positive = []
            negative = df['combine_neg_cnt'].values.tolist()
            neutral = []
            if 'start_percent' in request.args and 'end_percent' not in request.args:
                start_percent = request.args.get('start_percent')
                start = abs((int(start_percent) / 100) * len(title))
                title = title[int(start):]
                positive = positive[int(start):]
            if 'start_percent' not in request.args and 'end_percent' in request.args:
                end_percent = request.args.get('end_percent')
                end = abs((int(end_percent) / 100) * len(title))
                title = title[:int(end)]
                positive = positive[:int(end)]
            if 'start_percent' in request.args and 'end_percent' in request.args:
                start_percent = request.args.get('start_percent')
                end_percent = request.args.get('end_percent')
                start = abs((int(start_percent) / 100) * len(title))
                end = abs((int(end_percent) / 100) * len(title))
                title = title[int(start):int(end)]
                neutral = positive[int(start):int(end)]
                return render_template('stacked_bar.html', title='Negative Sentiment Chart', names=title,positive=positive, negative=negative,neutral=neutral)
            else:
                return render_template('stacked_bar.html', title='Negative Sentiment Chart', names=title,positive=positive, negative=negative,neutral=neutral)                
    elif 'sentiment_type' not in request.args:
        df = pd.read_csv('combined.csv')
        df['total_cnt'] = df.apply(lambda row: row.combine_pos_cnt + row.combine_neu_cnt + row.combine_neg_cnt, axis=1)
        df = df.sort_values(by=['total_cnt'], ascending=False)
        print(df.head())
        title = df['Title'].values.tolist()
        positive = df['combine_pos_cnt'].values.tolist()
        negative = df['combine_neu_cnt'].values.tolist()
        neutral = df['combine_neg_cnt'].values.tolist()
        
        if 'start_percent' in request.args and 'end_percent' not in request.args:
            start_percent = request.args.get('start_percent')
            start = abs((int(start_percent) / 100) * len(title))
            title = title[int(start):]
            neutral = positive[int(start):]
            return render_template('stacked_bar.html', title='Sentiment Chart Analysis', names=title,positive=positive, negative=negative,neutral=neutral)
        if 'start_percent' not in request.args and 'end_percent' in request.args:
            end_percent = request.args.get('end_percent')
            end = abs((int(end_percent) / 100) * len(title))
            title = title[:int(end)]
            neutral = positive[:int(end)]
            return render_template('stacked_bar.html', title='Sentiment Chart Analysis', names=title,positive=positive, negative=negative,neutral=neutral)
        if 'start_percent' in request.args and 'end_percent' in request.args:
            start_percent = request.args.get('start_percent')
            end_percent = request.args.get('end_percent')
            start = abs((int(start_percent) / 100) * len(title))
            end = abs((int(end_percent) / 100) * len(title))
            title = title[int(start):int(end)]
            neutral = positive[int(start):int(end)]
            return render_template('stacked_bar.html', title='Sentiment Chart', names=title,positive=positive, negative=negative,neutral=neutral)
        else:
            return render_template('stacked_bar.html', title='Sentiment Chart', names=title,positive=positive, negative=negative,neutral=neutral)


@app.route('/bar',methods=['POST','GET'])
def bar():
    if 'type' not in request.args:
        return render_template('error.html')
    if 'type' in request.args:
        type = request.args.get('type')
        if(type=='hashtag'):
            df1 = pd.read_csv('Sentiment.csv')
            pr = df1['present_hashtags'].value_counts(ascending=False,normalize=False).to_csv('hashtag_count.csv')
            hashtag_count = pd.read_csv('hashtag_count.csv')
            hashtag_count.rename(columns={ hashtag_count.columns[0]: "hashtags" }, inplace = True)
            hashtag_count.rename(columns={ hashtag_count.columns[1]: "hashtag_count" }, inplace = True)

            hashtag_labels = hashtag_count['hashtags'].values.tolist()
            count_labels = hashtag_count['hashtag_count'].values.tolist()
            max_size = max(count_labels) + 150
            if 'top_songs' in request.args:
                top_songs = request.args.get('top_songs')
                
                hashtag_labels = hashtag_labels[:int(top_songs)]
                count_labels = count_labels[:int(top_songs)]
                bar_labels=hashtag_labels
                bar_values=count_labels
                return render_template('bar.html', title='Hashtags(#)', max=max_size, labels=bar_labels, values=bar_values)
            else:
                bar_labels=hashtag_labels
                bar_values=count_labels
                return render_template('bar.html', title='Hashtags(#)', max=max_size, labels=bar_labels, values=bar_values)

        elif(type=='mention'):
            df1 = pd.read_csv('Sentiment.csv')
            pr = df1['present_mentions'].value_counts(ascending=False,normalize=False).to_csv('mention_count.csv')
            mention_count = pd.read_csv('mention_count.csv')
            mention_count.rename(columns={ mention_count.columns[0]: "mentions" }, inplace = True)
            mention_count.rename(columns={ mention_count.columns[1]: "mention_count" }, inplace = True)

            mention_labels = mention_count['mentions'].values.tolist()
            count_labels = mention_count['mention_count'].values.tolist()
            max_size = max(count_labels) + 150
            if 'top_songs' in request.args:
                top_songs = request.args.get('top_songs')
                
                mention_labels = mention_labels[:int(top_songs)]
                count_labels = count_labels[:int(top_songs)]
                
                bar_labels=mention_labels
                bar_values=count_labels
                return render_template('bar.html', title='Mentions(@)', max=max_size, labels=bar_labels, values=bar_values)
            else:
                bar_labels=mention_labels
                bar_values=count_labels
                return render_template('bar.html', title='Mentions(@)', max=max_size, labels=bar_labels, values=bar_values)

        

    
@app.route('/timeseries',methods=['POST','GET'])
def line():
    if 'start_date' in request.args and 'end_date' in request.args:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        df = pd.read_csv('timeseries.csv')
        df['newdate'] = None
        df['newdate']=df.date.str.split(' ').str[0].tolist()
        df['newdate'] = df['newdate'].astype('datetime64[ns]')
        df['date'] = df['date'].astype('datetime64[ns]')
        df['newdate'] = df['newdate'].astype(str)
        df["newdate"] = pd.to_datetime(df["newdate"])

        after_start_date = df["newdate"] >= start_date
        before_end_date = df["newdate"] <= end_date
        between_two_dates = after_start_date & before_end_date
        filtered_dates = df.loc[between_two_dates]

        filtered_dates['date'] = filtered_dates['date'].apply(str)
        date_list = filtered_dates['date'].values.tolist()

        count_labels = filtered_dates['cnt'].values.tolist()
        line_labels=date_list
        line_values=count_labels
        return render_template('timeseries.html', title='Timeseries', max=130000, labels=line_labels, values=line_values)
    else:
        return render_template('error.html')
    
    
        
    

        

if __name__ == '__main__':
    app.run()