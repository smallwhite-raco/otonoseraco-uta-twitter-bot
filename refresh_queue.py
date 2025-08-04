import csv
import random
import json
import os
from datetime import datetime

# History limit
HISTORY_LIMIT = 200

# read history
if os.path.exists("history.json") and os.path.getsize("history.json") > 0:
    with open("history.json", "r", encoding="utf-8") as f:
        history = json.load(f)
else:
    history = []

# read CSV：A = title、B = link
with open("playlist.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # skip header
    videos = [(row[1], row[0]) for row in reader if row[1].startswith("http") and row[0].strip() != ""]

# filter history
unposted = [(link, title) for link, title in videos if link not in history]

# reset history
if len(unposted) < 1:
    unposted = videos
    history = []

# choose 1
chosen = random.sample(unposted, 1)

# save to queue.json
with open("tweet_queue.json", "w", encoding="utf-8") as f:
    json.dump([{"link": l, "title": t} for l, t in chosen], f, ensure_ascii=False)

# update history.json
history += [l for l, _ in chosen]
history = history[-HISTORY_LIMIT:]
with open("history.json", "w", encoding="utf-8") as f:
    json.dump(history, f, ensure_ascii=False)


log_lines = [
    f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} extract queue："
]
for link, title in chosen:
    log_lines.append(f"- {title} ({link})")

with open("queue_log.txt", "a", encoding="utf-8") as f:
    f.write("\n".join(log_lines) + "\n")
