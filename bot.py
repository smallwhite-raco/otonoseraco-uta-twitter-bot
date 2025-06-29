import json
import os
import tweepy
import re
import random
import requests

# Telegram 通知函式
def notify_telegram(message):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    requests.post(url, data=payload)

# 載入設定檔
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

opening = random.choice(config["opening_options"])

# 讀取 tweet queue
with open("tweet_queue.json", "r", encoding="utf-8") as f:
    queue = json.load(f)

if not queue:
    print("🚫 沒有影片待發")
    exit()

video = queue.pop(0)
title_raw = video["title"]
link = video["link"]

# 分拆格式：「歌曲名 / VTuber名【註解】」
parts = [p.strip() for p in title_raw.split("/")]

if len(parts) >= 2:
    song_title = parts[0]
    vtuber_full = parts[1]
else:
    song_title = title_raw
    vtuber_full = "VTuber"

vtuber_name = re.sub(r"[\[【（(].*?[\]】）)]", "", vtuber_full).strip()

# 組合 Tweet 內容
tweet = config["template"].format(
    opening=opening,
    vtuber=vtuber_name,
    title=song_title,
    link=link,
    hashtags=config["hashtags"]
)

# 使用 Twitter API v2 Client 發 Tweet
try:
    client = tweepy.Client(
        consumer_key=os.getenv("CONSUMER_KEY"),
        consumer_secret=os.getenv("CONSUMER_SECRET"),
        access_token=os.getenv("ACCESS_TOKEN"),
        access_token_secret=os.getenv("ACCESS_TOKEN_SECRET")
    )
    client.create_tweet(text=tweet)
    notify_telegram(f"✅ 已發文：{vtuber_name}《{song_title}》\n{link}")
except Exception as e:
    notify_telegram(f"❗ 發文失敗：{vtuber_name}《{song_title}》\n原因：{str(e)}")
    raise

# 寫回 queue
with open("tweet_queue.json", "w", encoding="utf-8") as f:
    json.dump(queue, f, ensure_ascii=False)