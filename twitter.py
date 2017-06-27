#!/usr/bin/python
# -*- coding: utf-8 -*-

# imports
from __future__ import absolute_import, print_function
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import psycopg2
import json
import csv


def saveToCsv(txt):
    # persist to csv
    print(txt)
    fobj = open('twitter-data.csv', 'a')      # open file
    csvw = csv.writer(fobj, delimiter = ';') # create csv writer, set delimiter to 
    csvw.writerow(txt)
    
def saveToDb(tid,user,text):
    conn=connect()
    cur=conn.cursor()
    cur.execute("""INSERT INTO public.tweets (tweetid, "user", text) VALUES (%s, %s, %s);""", [tid,user,text])
    conn.commit()
    conn.close()
    
def connect():

    conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(host="178.254.35.26", database="dbs", user="testuser", password="testpass")
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return conn

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    
    def on_data(self, data):
        
        
        decoded = json.loads(data)
        print(decoded)
        text=[]
        text.append(str(decoded['id_str']))
        text.append(str(decoded['user']['screen_name']))
        text.append(str(decoded['text'].encode('ascii', 'ignore')))
        text.append(str(decoded['created_at']))
        saveToCsv(text)
        saveToDb(decoded['id_str'],str(decoded['user']['screen_name']),str(decoded['text'].encode('ascii', 'ignore')))
       

    def on_error(self, status):
        print(status)
        
def main():
    try:
        
        
        consumer_key        = "JpSR7TjCfhU7VjaWt1lYoyVdm"
        consumer_secret     = "1qA11pY3EQlWT93JXqtV60ZZ1VoYRirAWcWsJIwTBcM1RqNvJp"
        access_token        = "2902275983-CqLsO6UT0LEbJlvjL7Cg78s1Vq7G0TKPCrOddIS"
        access_token_secret = "HuqO2gJjcD9FeJHgPPvFwlWgkylto9EkQD0bddo75khk9"
    
        # write csv Header
        with open('twitter-data.csv', 'w') as f:
            writer = csv.writer(f ,delimiter = ';')
            writer.writerow(['TweetId', 'User', 'Text','Date'])
            
        listener = StdOutListener()
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        stream = Stream(auth, listener)
        stream.filter(track=['@realDonaldTrump'], async=True)
        
    except (Exception) as error:
        print("Fehler:",error)
       

if __name__ == '__main__':

    main()
    
