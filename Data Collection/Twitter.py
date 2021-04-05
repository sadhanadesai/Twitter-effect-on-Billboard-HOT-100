#from csv import writer
import os
import requests
import simplejson as json
import config
import psycopg2


def fun(url,headers):
    conn = psycopg2.connect('dbname=ds_project user=kasturivartak password=password host=localhost')
    cur = conn.cursor()

    # today_date = datetime.datetime.now()  
    # print(today_date) 
    response = requests.request("GET", url, headers=headers, stream=True)
    if(response.status_code != 200):
        raise Exception("Req errror".format(
            response.status_code,response.text
    ))

    else:
        i=0
        for line in response.iter_lines():
            if line:
                json_response = json.loads(line)
                annotations = []
                entities = []
                public_metrics = []
                created_at = json_response['data']['created_at']
                tweet_id = json_response['data']['id']
                tweet = json_response['data']['text']
                lang = json_response['data']['lang']
                if('context_annotations' in json_response['data']):
                    annotations = json_response['data']['context_annotations']
                if('entities' in json_response['data']):
                    entities = json_response['data']['entities']
                if('public_metrics' in json_response['data']):
                    public_metrics = json_response['data']['public_metrics']
                
                if(lang=="en"):
                    array = []
                    
                    retweet_count = public_metrics['retweet_count']
                    like_count = public_metrics['like_count']
                    
                    domain_name = []
                    entity_name = []
                    

                    if(len(annotations) > 0):
                        for annote in annotations:
                            annote_json = json.dumps(annote, sort_keys=True, indent=2)
                            annotations_r = json.loads(annote_json)
                            if('domain' in annotations_r):
                                domain_name.append(annotations_r['domain']['name'])
                            if('entity' in annotations_r):
                                # print(annotations_r['entity']['name'])
                                entity_name.append(annotations_r['entity']['name'])
                    # # Entities
                    entity = json.dumps(entities, sort_keys=True, indent=2)
                    entity_r = json.loads(entity)
                    # Hashtag
                    hashtags = []
                    if 'hashtags' in entity_r:
                        for hash in entity_r['hashtags']:
                            hashtag = json.dumps(hash, sort_keys=True, indent=2)
                            hashtag_r = json.loads(hashtag)
                            hashtags.append(hashtag_r['tag'])
                    
                    # Mentions
                    mention = []
                    if 'mentions' in entity_r:
                        for ment in entity_r['mentions']:
                            mentions = json.dumps(ment, sort_keys=True, indent=2)
                            mentions_r = json.loads(mentions)
                            mention.append(mentions_r['username'])

                    array.extend((created_at,tweet_id,tweet,lang,retweet_count,like_count,domain_name,entity_name,hashtags,mention))
                    
                        
                        # print("\n-------\n")

                    cur.execute("INSERT INTO project.Twitter (created_at,tweet_id,tweet, lang,retweet_count,like_count,domain_name,entity_name,hashtags,mention) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (created_at,tweet_id,tweet, lang,retweet_count,like_count,domain_name,entity_name,hashtags,mention))

                    # with open('data/twitter222.csv', 'a+', newline='') as write_obj:
                    #     csv_writer = writer(write_obj)
                    #     csv_writer.writerow(arr)
                    #print(i)
                #i+=1
                conn.commit()
                # print("Records created successfully")
        conn.close()
        print("Connection closed")    

def main():
    # bearer_token = 'AAAAAAAAAAAAAAAAAAAAAOPjIwEAAAAA6IpFQXkJKeZB%2BzOtsf%2FN6P02jU8%3Dyzy47q1KkjE9vXsHQuZOsbuPLEjujmbqJC0PffUwclQZ60gxDX'
    headers = {"Authorization":"Bearer {}".format(config.bearer_token)}
    url = "https://api.twitter.com/2/tweets/sample/stream?tweet.fields=public_metrics,context_annotations,created_at,entities,lang&expansions=entities.mentions.username"
    timeout=0
    while True:
        fun(url,headers)
        timeout+=1

if __name__ == "__main__":
    main()
