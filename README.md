# Automatic Windows Lockscreen Wallpaper
lets you script what types of photos are posted on your lockscreen

# How to use

1. Must create config.ini for Reddit API key credentials, as well as location of where wallpapers are stored
https://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html
2. Add path where you want wallpapers stored in config.ini under

3. Uses [Dynamic Theme](https://www.microsoft.com/en-us/p/dynamic-theme/9nblggh1zbkw?activetab=pivot:overviewtab) from Windows Store to actually update the lockscreen, as updating the lockscreen is shockingly difficult for whatever reason. With Dynamic Theme, you could also sync your lockscreen and desktop wallpaper.
4. Use Windows Task Scheduler to run the script automatically over intervals of time
## Example config.ini
```
[Reddit]
client_id = myID
client_secret = mySecret
user_agent = image downloader for hot posts on r/wallpaper
[LocalPath]
saved_images_path = myPath
```
