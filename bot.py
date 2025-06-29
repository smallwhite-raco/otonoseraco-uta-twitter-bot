import json
import os
import tweepy
import re
import random
import requests

# 載入設定
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

# 隨機抽開場白
opening = random.choice(config["opening_options"])

# 載入佇列
with open("tweet_queue.json", "r", encoding="utf-8") as f:
    queue = json.load(f)

if not queue:
    print("🚫 沒有影片待發")
    exit()

video = queue.pop(0)
title_raw = video["title"]
link = video["link"]

# 分拆格式：「影片名稱 / VTuber名【註解】」
parts = [p.strip() for p in title_raw.split("/")]

if len(parts) >= 2:
    song_title = parts[0]
    vtuber_full = parts[1]
else:
    song_title = title_raw
    vtuber_full = "VTuber"

vtuber_name = re.sub(r"[\[【（(].*?[\]】）)]", "", vtuber_full).strip()

# 組合 Tweet
tweet = config["template"].format(
    opening=opening,
    vtuber=vtuber_name,
    title=song_title,
    link=link,
    hashtags=config["hashtags"]
)

# Twitter 發文
auth = tweepy.OAuth1UserHandler(
    os.getenv("CONSUMER_KEY"),
    os.getenv("CONSUMER_SECRET"),
    os.getenv("ACCESS_TOKEN"),
    os.getenv("ACCESS_TOKEN_SECRET")
)
api = tweepy.API(auth)


# 更新佇列
with open("tweet_queue.json", "w", encoding="utf-8") as f:
    json.dump(queue, f, ensure_ascii=False)

# 發完 Tweet 後，通知 Telegram
def notify_telegram(message):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    requests.post(url, data=payload)

try:
    api.update_status(tweet)
    # 成功發文後通知
    notify_telegram(f"✅ 已發文：{vtuber_name}《{song_title}》\n{link}")
except Exception as e:
    error_msg = f"❗發文失敗：{vtuber_name}《{song_title}》\n原因：{str(e)}"
    notify_telegram(error_msg)
    raise