import requests
import json
import shutil
from time import sleep
import mlcode

# secret token code stored in a text file named secret.txt
with open("secret.txt", "r") as fh:
    token = fh.read().strip()
    
baseurl = "https://api.telegram.org/bot{}/".format(token)

def get_updates(offset = None):
    while True:
        url = baseurl + 'getUpdates'
        if offset:
            url += '?offset={}'.format(offset)
        res = requests.get(url)
        while (res.status_code !=200 or len(res.json()['result'])== 0):
            sleep(1)
            res = requests.get(url)
        print(res.url)
        return res.json()

def last_update_id(res):
    return res['result'][-1]['update_id']

def is_starter(msg):
    starter = ["hey", "hello", "start", "strt", "begin", "init"]
    for s in starter:
        if s in msg: return True
    else: return False
    
def get_photo_chats(updates): # get image 
    photo_chats = []
    for i in updates['result']:
        if 'photo' in i['message']:
            photo_chats.append((i['message']['chat']['id'],
                               i['message']['photo'][-1]['file_id'], i['message']['message_id']))
            if i['message']['chat']['type']=='private':
                print(i['message']['chat']['first_name'], "sent an image")
            else:
                print(i['message']['chat']['title'], "sent an image")
    return photo_chats
   
   
   
def run():
    print("\nStarting the Bot...")
    offset = None
    while True:
        try:
            updates = get_updates(offset)
            offset = last_update_id(updates)+1
            start_chats = get_start_chats(updates)
            
            #photo_chats = get_photo_chats(updates)
            
        except KeyboardInterrupt:
            print("\nStopping the Bot...")
            break
        except:
            continue

run()
