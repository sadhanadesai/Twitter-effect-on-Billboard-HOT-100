import requests 
import datetime
import json
import re
import sys
from bs4 import BeautifulSoup
import requests
import datetime
#import schedule
import time
import uuid
import psycopg2

def billboardAPI():
    today_date = datetime.datetime.now()  

    conn = psycopg2.connect('dbname=ds_project user=kasturivartak password=password host=localhost')
    #conn = psycopg2.connect('dbname=kasturivartak user=kasturivartak host=localhost')
    cur = conn.cursor()

    _CHART_NAME_SELECTOR = 'meta[name="title"]'
    _ENTRY_ARTIST_ATTR = "data-artist"
    _PREVIOUS_DATE_SELECTOR = "span.fa-chevron-left"


    url = "https://www.billboard.com/charts/hot-100"
    
    def _get_session_with_retries(max_retries):
        session = requests.Session()
        session.mount(
            "https://www.billboard.com",
            requests.adapters.HTTPAdapter(max_retries=max_retries),
        )
        return session
    
    def _parseNewStylePage(soup):
        dateElement = soup.select_one("button.date-selector__button.button--link")
        datenow = datetime.datetime.now()

        if dateElement:
            dt = dateElement.text.strip()
            date = datetime.datetime.strptime(re.sub(r"(st|th|rd)", "", dt), "%B %d, %Y").strftime("%Y-%m-%d")
                        
            for i in soup.select("li.chart-list__element"):
                def getEntryAttr(selector):
                    element = i.select_one(selector)
                    if element:
                        return element.text.strip()
                    return None
                
                try:
                    title = getEntryAttr("span.chart-element__information__song")
                except:
                    raise Exception("Failed to parse title")
                
                try:
                    artist = getEntryAttr("span.chart-element__information__artist") or ""
                    artist = artist.replace('Featuring', ',').replace('&', ',').replace(' x ',',').replace(' X ',',')
                    artist = re.sub(r'\s*,\s*', ',', artist)
                except:
                    raise Exception("Failed to parse artist")
                
                try:
                    rank = int(getEntryAttr("span.chart-element__rank__number"))
                except:
                    raise Exception("Failed to parse rank")

                def getMeta(attribute, ifNoValue=None):
                    try:
                        selected = i.select_one(
                            "span.chart-element__meta.text--%s" % attribute
                        )
                        if (
                            not selected
                            or selected.string is None
                            or selected.string == "-"
                        ):
                            return ifNoValue
                        else:
                            return int(selected.string.strip())
                    except:
                        raise Exception("Failed to parse metadata")
                        
                if date:
                    peakPos = getMeta("peak")
                    lastPos = getMeta("last", ifNoValue=0)
                    weeks = getMeta("week", ifNoValue=1)
                    isNew = True if weeks == 1 else False
                
                id = uuid.uuid4()
                
                array = [title, artist, peakPos, lastPos, weeks, rank, isNew]
                cur.execute("INSERT INTO project.billboard VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (title, artist, peakPos, lastPos, weeks, rank, isNew, str(today_date)))
                #cur.execute("INSERT INTO project.billboard("title","artist","peakPos","lastPos","weeks","rank","isNew","timestamp") VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (title,artist,peakPos,lastPos,weeks,rank,isNew,str(today_date)))
            conn.commit()
            print("Records created successfully")

    def _parsePage(soup):
        chartTitleElement = soup.select_one(_CHART_NAME_SELECTOR)
        if chartTitleElement:
            title = re.sub(
                " Chart$",
                "",
                chartTitleElement.get("content", "").split("|")[0].strip(),
            )
        if soup.select("table"):
            print("table")
        else:
            _parseNewStylePage(soup)


    session = _get_session_with_retries(5)
    req = session.get(url, timeout=25)
    if req.status_code == 404:
        print("404")
    else:
        req.raise_for_status()
        soup = BeautifulSoup(req.text, "html.parser")
        _parsePage(soup)

    conn.close()
    print("Connection closed")

billboardAPI()

