# Downloads top x posts from reddit. 
# Used with Dynamic Wallpaper from Windows and Windows Task Scheduler, 
# you can automatically update your lockscreen or background wallpaper to reddit wallpapers!
import requests
import praw
import os
from datetime import datetime
import glob
from PIL import Image
from io import BytesIO
import configparser

def get_current_directory():
    # Get the directory of the current script
    return os.path.dirname(os.path.abspath(__file__))

def get_absolute_path_for_file(file_name):
    # Get the directory of the current script
    current_script_directory = get_current_directory()
    # Your local path relative to the script directory
    relative_path = file_name
    # Construct the absolute path
    absolute_path = os.path.join(current_script_directory, relative_path)
    
    print(absolute_path)
    return absolute_path

def delete_files_at_path(path):
    """deletes all files in folder where wallpapers will be stored"""
    files = glob.glob(path + '*')
    print("Deleting old wallpapers...")
    for f in files:
        os.remove(f)


def get_top_post():
    """Downloads the hottest post (top = hot for this app)"""
    get_top_x_posts(1)

def process_default(submission, saved_images_path):
    """Takes submission url, downloads, and saves to path. Most submission use this function."""
    image_url = submission.url
    file_name = image_url.split("/")[-1]
    file_name_dated = date_created + "_" + file_name
    response = requests.get(image_url)
    final_file_path = saved_images_path + file_name_dated
    with open(final_file_path, "wb") as f:
        f.write(response.content)
        print("Downloaded: " + final_file_path)


def process_gallery(submission, saved_images_path):
    """
    Same output as process_default, but approach is different for galleries.
    Will download all images from a gallery. 
    
    See also:
        :func:`process_default`
    """
     # Iterate through the media of the submission
    for media in submission.media_metadata.values():
        # Check if media type is image
        if media['e'] == 'Image':
            # Get the direct URL to the image
            image_url = media['s']['u']
            file_name = image_url.split("/")[-1]
            # Download the image
            response = requests.get(image_url)

            if response.status_code == 200:
                # Open the image using PIL
                content = BytesIO(response.content)
                img = Image.open(content).convert("RGB")
                gallery_file_name = file_name.split("?")[0]
                # Save the image
                final_file_path = saved_images_path + date_created + "_" + gallery_file_name
                img.save(final_file_path)
                print("Downloaded: " + final_file_path)
            else:
                print("Failed to fetch the image. Status code:", response.status_code)



def create_directory(directory_path):
    """
    Creates images directory if it doesn't exist
    """
    if not os.path.exists(directory_path):
        # Create the directory and its parents if they don't exist
        os.makedirs(directory_path)
        print(f"Directory '{directory_path}' created successfully.")
    else:
        print(f"Directory '{directory_path}' already exists.")


def get_top_x_posts(x, saved_images_path):
    """
    Downloads x number of hottest posts. 
    Creates images folder to store them in, deletes all old images in folder, 
    and downloads x number of hottest image posts from the subreddit selected.
    """
    saved_images_path = os.path.join(saved_images_path, "images/")
    create_directory(saved_images_path)
    delete_files_at_path(saved_images_path)    

    # get reddit post
    submission_list = []
    for submission in reddit.subreddit(subreddit).hot(limit=x):
        submission_list.append(submission)

    # Download
    print("Downloading new wallpapers...")
    for submission in submission_list:
        if "gallery/" in submission.url:
            process_gallery(submission, saved_images_path)
        else:
            process_default(submission, saved_images_path)
    print("Done.")


config = configparser.ConfigParser()

# read config file to locally store sensitive data
config.read(get_absolute_path_for_file("config.ini"))

# PATH WHERE IMAGES WILL BE SAVED
saved_images_path = config['LocalPath']['saved_images_path']
date_created = datetime.utcnow().strftime('%Y-%m-%d')

# Choose subreddit to get images from, also provide your Reddit API client information in a config.ini
subreddit = "wallpaper"
reddit = praw.Reddit(
    client_id=config['Reddit']['client_id'],
    client_secret=config['Reddit']['client_secret'],
    user_agent=config['Reddit']['user_agent']
)


get_top_x_posts(4, saved_images_path)