# -*- coding: utf-8 -*-
import requests
import telebot
import config
import json
import sqlite3
import time



bot = telebot.TeleBot(config.token)
key = True

url = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN"

CHANNEL = '@asdfadsaasdfadfad'

#get the json
def get_json(request):
    response = requests.get(request)

    return response.json()

#parce json to list
def dump_json():
    result = json.dumps(get_json(url))
    f_doc = json.loads(result)
    f_doc = f_doc['Data']
    return f_doc


#cheking for new post, if from json returned id that didn't exist in data base
#adding new post information
def check_new_post():
    conn = sqlite3.connect('post.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM post_data')
    r = cursor.fetchall()
    g = dump_json()
    new_id = int(g[0]['id'])
    trigger = True
    if(int(r[len(r)-1][0])==int(new_id)):
          time.sleep(60)
    else:
            json = g[0]
            cursor.execute('INSERT INTO post_data(id,title,category,body,source,site_url) VALUES (?,?,?,?,?,?)'\
                           , (json['id'],json['title'],json['categories'],json['body'],json['source'],json['url']))
            conn.commit()
            trigger = False

    return trigger


#parsing database for last post and send it
def send_news_message():
    conn = sqlite3.connect('post.db')
    cursor = conn.cursor()
    cursor.execute('SELECT title,category,body,source,site_url FROM post_data')
    r = cursor.fetchall()

    title = r[len(r)-1][0]
    category = r[len(r)-1][1]
    body =r[len(r)-1][2]
    source = r[len(r)-1][3]
    site_url = r[len(r)-1][4]


    return bot.send_message(CHANNEL, text = '*'+title+'*'+'\n'+'\n'+body+'\n'+'\n'+'#'+category+'\n'+'\n'\
                 +source+'\n'+site_url, parse_mode='MARKDOWN')



#for the first star to put some post
def first_start():
        global key
        if key:
            send_news_message()
            key = False


#call first_start to send first post
#cheking for new post if it exist add
#wait to avoid flood
#send new post

if __name__== '__main__':
  first_start()
while True:
    time.sleep(60)
    if(not(check_new_post())):
        send_news_message()





