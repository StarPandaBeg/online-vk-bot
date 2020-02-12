"""
"""

import vk_api

import time
import os
import random

VK_USER_TOKEN = str(os.environ.get("TOKEN"))
VK_CONTROL_TOKEN = str(os.environ.get("ACCESS_TOKEN"))

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
        text = format_time(random_s)
        send_message(ac_api, text)
        wait_for_seconds(random_s)
        send_message(ac_api, "Захожу в онлайн на " + str(random_online) + " секунд.")
        set_online(api, random_online)
        send_message(ac_api, "Оффлайн")

# ------------
def format_time(s):
    now_time = int(time.time())
    next_time = now_time + s
    resp = "Следущий онлайн будет в " + time.strftime("%H:%M %d.%m.%Y", time.localtime(next_time))
    return resp

def get_random():
    random_s = 5400 + random.randrange(0, 1800, 60)
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