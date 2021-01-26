#Downloads top x posts from reddit. Used with Dynamic Wallpaper from Windows and Windows Task Scheduler, 
# you can automatically update your lockscreen or background wallpaper to reddit wallpapers!

import re
import requests
import praw
import os
import time
from datetime import datetime
from pytz import timezone
import glob

#choose sub to draw from
subreddit = "wallpapers"
tz = timezone('US/Eastern')
reddit = praw.Reddit(
    client_id="Bd83cwSUnsCMtQ",
    client_secret="q9DWmxnWMzudQYDOB-USk9IMGtK8Pw",
    user_agent="Image downloader for hot posts on r/Wallpapers"
)

#Downloads the hottest post (top = hot for this app)
def get_top_post():
    get_top_x_posts(1)

#Downloads x hottest posts
def get_top_x_posts(x):
    # get reddit post
    submission_list = []
    for submission in reddit.subreddit(subreddit).hot(limit=x):
        submission_list.append(submission.url)

    #delete
    #path will be where you store and update your wallpapers
    path = "your/path/here"
    files = glob.glob(path + '*')
    print("Deleting old wallpapers...")
    for f in files:
        os.remove(f)
    
    # download
    print("Downloading new wallpapers...")
    for submission in submission_list:
        url = (submission)
        file_name = url.split("/")
        if len(file_name) == 0:
            file_name = re.findall("/(.*?)", url)
        file_name = file_name[-1]

        if "." not in file_name:
            file_name += ".jpg"
        t = time.localtime()

        date_created = datetime.utcnow().strftime('%m-%d-%Y %H-%M-%S.%f')[:-5]

        file_name_dated = date_created + file_name[-4:]
        r = requests.get(url)

        with open(path + file_name_dated, "wb") as f:
            f.write(r.content)
    print("Done.")
get_top_x_posts(4)