In Data Collection system, we have collected data from Twitter Streaming API and Billboard HOT 100 chart every Tuesday.

1.  Data Cleaning: 

    • To filter the this data using hashtags and mentions collected.
    
    • The attributes in Twitter data that we plan to extract are created_at,_id,tweet,lang,annotations,entities,public_metrics.
    
    • The extracted features are stored separately from the raw data in PostgreSQL.
    
    
2.  Data Analysis

    • Performed sentiment analysis on tweets collected using hashtags and mentions from Billboard HOT 100 using NLTKs Vader.

3.  Plots

    • Concluded this project with some plots (timeseries plot, number of posotive, negative, neitral tweets by hashtags, mentions, song title and so on) using matplotlib. 

  
