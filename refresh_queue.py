import csv
import random
import json
import os

HISTORY_LIMIT = 100

# 讀舊 history
if os.path.exists("history.json"):
    with open("history.json", "r", encoding="utf-8") as f:
        history = json.load(f)
else:
    history = []

# 讀 CSV：A = title、B = link
with open("videos.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # skip header
    videos = [(row[1], row[0]) for row in reader if row[1].startswith("http") and row[0].strip() != ""]

# 過濾已發過
unposted = [(link, title) for link, title in videos if link not in history]

# 如果唔夠新片，就重設 history
if len(unposted) < 3:
    print("⚠️ 未發過嘅片唔夠 3 條 → 清空紀錄重新洗牌")
    unposted = videos
    history = []

# 抽出 3 條
chosen = random.sample(unposted, 3)

# 儲存至 queue.json
with open("tweet_queue.json", "w", encoding="utf-8") as f:
    json.dump([{"link": l, "title": t} for l, t in chosen], f, ensure_ascii=False)

# 更新 history，保留最近 100 條
history += [l for l, _ in chosen]
history = history[-HISTORY_LIMIT:]  # 保留最後 100 條
with open("history.json", "w", encoding="utf-8") as f:
    json.dump(history, f, ensure_ascii=False)