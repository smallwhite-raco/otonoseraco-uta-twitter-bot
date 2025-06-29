import gspread
import random
import tweepy
from oauth2client.service_account import ServiceAccountCredentials
import os

# 🔐 Google Sheets 認證
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# 📊 讀取 Sheet（換成你自己的 Sheet ID）
sheet = client.open_by_key("YOUR_SHEET_ID").sheet1
links = sheet.col_values(1)
titles = sheet.col_values(2)

# 🚫 防呆：避免兩欄長度唔對
videos = list(zip(links, titles))
videos = [v for v in videos if v[0].startswith("http") and v[1].strip() != ""]

# 🎲 隨機抽一條
link, title = random.choice(videos)

# 🐦 Twitter 認證
auth = tweepy.OAuth1UserHandler(
    os.getenv("CONSUMER_KEY"),
    os.getenv("CONSUMER_SECRET"),
    os.getenv("ACCESS_TOKEN"),
    os.getenv("ACCESS_TOKEN_SECRET")
)
api = tweepy.API(auth)

# ✍️ 發 Tweet
tweet = f"🎶 今日推介：{title}\n🔗 {link}\n#VTuber #歌回 #每日推薦"
api.update_status(tweet)