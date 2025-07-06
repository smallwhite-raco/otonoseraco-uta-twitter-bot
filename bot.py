import json
import os
import tweepy
import re
import random
import requests
from datetime import datetime

# 📩 Telegram 通知
def notify_telegram(message):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    requests.post(url, data=payload)

notify_telegram("🚀 Workflow 開始執行：Twitter bot 正在啟動")

# ⚙️ 載入設定
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

opening = random.choice(config["opening_options"])

# 🎬 載入 tweet queue
with open("tweet_queue.json", "r", encoding="utf-8") as f:
    queue = json.load(f)

if not queue:
    print("🚫 沒有影片待發")
    exit()

video = queue[0]  # 唔即刻 pop，等成功先寫入
title_raw = video["title"]
link = video["link"]

# 🔍 分拆格式：「歌曲名 / VTuber名【註解】」
parts = [p.strip() for p in title_raw.split("/")]
if len(parts) >= 2:
    song_title = parts[0]
    vtuber_full = parts[1]
else:
    song_title = title_raw
    vtuber_full = "VTuber"

vtuber_name = re.sub(r"[\[【（(].*?[\]】）)]", "", vtuber_full).strip()

# ✍️ 組合 Tweet
tweet = config["template"].format(
    opening=opening,
    vtuber=vtuber_name,
    title=song_title,
    link=link,
    hashtags=config["hashtags"]
)

# 🐦 發 Tweet（Twitter v2 API）
try:
    client = tweepy.Client(
        consumer_key=os.getenv("CONSUMER_KEY"),
        consumer_secret=os.getenv("CONSUMER_SECRET"),
        access_token=os.getenv("ACCESS_TOKEN"),
        access_token_secret=os.getenv("ACCESS_TOKEN_SECRET")
    )
    client.create_tweet(text=tweet)

    # ✅ 通知 Telegram
    notify_telegram(f"✅ 已發文：{vtuber_name}《{song_title}》\n{link}")

    # 📓 記錄 log.txt
    log_line = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ✅ {vtuber_name}《{song_title}》 {link}\n"
    with open("tweet_log.txt", "a", encoding="utf-8") as log:
        log.write(log_line)

    # 📦 更新 queue.json
    queue.pop(0)
    with open("tweet_queue.json", "w", encoding="utf-8") as f:
        json.dump(queue, f, ensure_ascii=False)

    print("✅ 發文成功，已更新 queue 和記錄 log。")

except Exception as e:
    notify_telegram(f"❗ 發文失敗：{vtuber_name}《{song_title}》\n原因：{str(e)}")
    print("❗ 發文失敗：", e)
    raise