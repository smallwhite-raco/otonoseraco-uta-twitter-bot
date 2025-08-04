import subprocess

url = "https://www.youtube.com/playlist?list=PL1kHTE5nMBODjTLPSDlWJPnTlFuIFrhqy"
cmd = ["yt-dlp", "--flat-playlist", "-J", url]

with open("playlist.json", "w", encoding="utf-8") as f:
    subprocess.run(cmd, stdout=f, check=True)