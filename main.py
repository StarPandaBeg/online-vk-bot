"""
"""

import vk_api

import time
import datetime
import os
import random

VK_USER_TOKEN = str(os.environ.get("TOKEN"))
VK_CONTROL_TOKEN = str(os.environ.get("ACCESS_TOKEN"))
UP = int(os.environ.get("UP"))
DOWN = int(os.environ.get("DOWN"))

def login(token):
    vk = vk_api.VkApi(token=token)
    api = vk.get_api()
    return api

def send_message(api, text):
    api.messages.send(message=text, peer_id=278308173, random_id=random.randint(0,60000))

def run(api):
    ac_api = login(VK_CONTROL_TOKEN)
    while (True):
        random_s, random_online = get_random()
        send_message(ac_api, "Жду " + random_s + " секунд до следующего онлайна.")
        wait_for_seconds(random_s)
        send_message(ac_api, "Захожу в онлайн на " + random_online + " секунд.")
        set_online(api, random_online)
        send_message(ac_api, "Оффлайн")

# ------------
def get_random():
    temp_date = datetime.datetime.now()
    if UP < temp_date.hour: 
        if temp_date.month in [1,3,5,7,8,10,12]:
            if temp_date.day == 31:
                if temp_date.month == 12:
                    temp_new_date = datetime.datetime(temp_date.year+1,1,1,UP,0,0)
                else:
                    temp_new_date = datetime.datetime(temp_date.year,temp_date.month+1,1,UP,0,0)
            else:
                temp_new_date = datetime.datetime(temp_date.year,temp_date.month,temp_date.day+1,UP,0,0)
        elif temp_date.month == 2:
            if (temp_date.year % 4) == 0:
                if temp_date.day == 29:
                    temp_new_date = datetime.datetime(temp_date.year,3,1,UP,0,0)
                else:
                    temp_new_date = datetime.datetime(temp_date.year,temp_date.month,temp_date.day+1,UP,0,0)
            else:
                if temp_date.day == 28:
                    temp_new_date = datetime.datetime(temp_date.year,3,1,UP,0,0)
                else:
                    temp_new_date = datetime.datetime(temp_date.year,temp_date.month,temp_date.day+1,UP,0,0)
        else:
            if temp_date.day == 30:
                temp_new_date = datetime.datetime(temp_date.year,temp_date.month+1,1,UP,0,0)
            else:
                temp_new_date = datetime.datetime(temp_date.year,temp_date.month,temp_date.day+1,UP,0,0)
    else:
        temp_new_date = datetime.datetime(temp_date.year,temp_date.month,temp_date.day,UP,0,0)

    if temp_new_date.day - temp_date.day == 0:
        start = 120
    else:
        start = (datetime.datetime(temp_date.year,temp_date.month,temp_date.day,DOWN,0,0) - temp_date).total_seconds()
        if start < 0:
            start = 120

    delta = temp_new_date - temp_date
    total = delta.total_seconds()
    random_s = random.randrange(int(start), int(total), 30)
    random_online = random.randrange(300, 3600, 300)
    return random_s, random_online

def wait_for_seconds(s):
    time.sleep(s)

def set_online(api, sec):
    while sec > 0:
        api.account.setOnline()
        if sec > 300:
            time.sleep(300)
            sec -= 300
        else:
            time.sleep(sec)
            sec=0 
    api.account.setOffline()           


if __name__ == "__main__":
    api = login(VK_USER_TOKEN)
    run(api)