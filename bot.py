import json
import os
import tweepy
import re
import random
import requests
from datetime import datetime

# Telegram noti
def notify_telegram(message):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    requests.post(url, data=payload)

# load post format setting
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

opening = random.choice(config["opening_options"])

# get YouTube link and title
with open("tweet_queue.json", "r", encoding="utf-8") as f:
    queue = json.load(f)

if not queue:
    print("tweet_queue.json list is empty")
    exit()

video = queue[0] 
title_raw = video["title"]
link = video["link"]

# YouTube title = 「Song Name / Raco」
parts = [p.strip() for p in title_raw.split("/")]
if len(parts) >= 2:
    song_title = parts[0]
    vtuber_full = parts[1]
else:
    song_title = title_raw
    vtuber_full = "VTuber"

vtuber_name = re.sub(r"[\[【（(].*?[\]】）)]", "", vtuber_full).strip()

# Combin Tweet post
tweet = config["template"].format(
    opening=opening,
    vtuber=vtuber_name,
    title=song_title,
    link=link,
    hashtags=config["hashtags"]
)

# Post Tweet（Twitter v2 API）
try:
    client = tweepy.Client(
        consumer_key=os.getenv("CONSUMER_KEY"),
        consumer_secret=os.getenv("CONSUMER_SECRET"),
        access_token=os.getenv("ACCESS_TOKEN"),
        access_token_secret=os.getenv("ACCESS_TOKEN_SECRET")
    )
    client.create_tweet(text=tweet)

    # Telegram Noti
    notify_telegram(f"✅ {vtuber_name}《{song_title}》\n{link}")

    # record in log.txt
    log_line = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ✅ {vtuber_name}《{song_title}》 {link}\n"
    with open("tweet_log.txt", "a", encoding="utf-8") as log:
        log.write(log_line)

    # update queue.json
    queue.pop(0)
    with open("tweet_queue.json", "w", encoding="utf-8") as f:
        json.dump(queue, f, ensure_ascii=False)

    print("✅ Done, updated queue and log")

except Exception as e:
    notify_telegram(f"❗ Post failed：{vtuber_name}《{song_title}》\nReason：{str(e)}")
    print("❗ Failed：", e)
    raise