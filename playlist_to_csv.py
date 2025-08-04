# yt-dlp --flat-playlist -J "https://www.youtube.com/playlist?list=PL1kHTE5nMBODjTLPSDlWJPnTlFuIFrhqy" > playlist.json

import json
import csv
try:
    # with open('playlist.json', 'r', encoding='utf-8') as f:
    with open('playlist.json', 'r', encoding='utf-16') as f:
        data = json.load(f)
except:
    with open('playlist.json', 'r', encoding='utf-8') as f:
    # with open('playlist.json', 'r', encoding='utf-16') as f:
        data = json.load(f)

with open('playlist.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['Title', 'URL'])
    for entry in data['entries']:
        title = entry.get('title', 'N/A')
        url = f"https://www.youtube.com/watch?v={entry['id']}"
        writer.writerow([title, url])

print("Done！")