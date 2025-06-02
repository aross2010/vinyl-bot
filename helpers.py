import json, os, praw
from dotenv import load_dotenv
import traceback
import re

# Returns the json object containing the post ids that have already been emailed out
def read_posts_json():

    # Get full path
    dir_path = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(dir_path, 'posts.json')

    try:
        with open(filename, 'r') as file:
            try:
                return json.load(file)
            except Exception:
                return []
    except Exception:
        print('posts.json not found')

# Keeps track of which posts have been emailed out
def write_posts_json(recent_valid_posts):

    # Get full path
    dir_path = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(dir_path, 'posts.json')

    try:
        with open(filename, 'w') as file:
                json.dump(recent_valid_posts, file, indent=4)
    except Exception:
        print('posts.json not found')   

# Returns the json object containg the relevant wantlist data from discogs
def read_discogs_json():

    # Get full path
    dir_path = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(dir_path, 'discogs.json')

    try:
        with open(filename, 'r') as file:
            try:
                return json.load(file)
            except Exception:
                print('discogs.json is empty')
                return None
    except FileExistsError:
        print('discogs.json not found')

# Returns the last seen json object containing the last post seen for both types of fetches
def read_last_seen_json():

    # Get full path
    dir_path = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(dir_path, 'last_seen.json')
    # If file does not exist, create it with default value

    try:
        with open(filename, 'r') as file:
                return json.load(file)
    except Exception:
        # Create the file with default values
        last_seen = {
            'main': 0,
            'alt': 0
        }
        with open(filename, 'w') as file:
            json.dump(last_seen, file, indent=4)
        return last_seen

# Keeps track of the last post visited, so no post is checked twice
def write_last_seen_json(is_main: bool, id: int):

    last_seen = read_last_seen_json()
    if is_main: last_seen['main'] = id
    else: last_seen['alt'] = id

    # Get full path
    dir_path = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(dir_path, 'last_seen.json')

    try:
        with open(filename, 'w') as file:
                json.dump(last_seen, file, indent=4)
    except Exception:
        print('last_seen.json not found')

def is_valid_match_artist(artist: str, post: str):
        artist_in_post = post.split('-')[0].strip().lower() if '-' in post else post.split('(')[0].strip().lower()
        match = rf'\b{re.escape(artist)}\b'
        return re.search(match, artist_in_post) is not None

# Validates whether a key is in a string. The key must be its own word or be a word with a non-letter trailing and leading it
def is_valid_match(album_title: str, album_artists: list, post: str):
    artist_in_post = post.split('-')[0].strip().lower() if '-' in post else post.split('(')[0].strip().lower()
    album_in_post = post.split('-')[1].strip().lower() if '-' in post else post.strip().lower()
    match = rf'\b{re.escape(album_title)}\b'
    valid_album = re.search(match, album_in_post) is not None
    if valid_album: 
        # confirm with presence of artists
        for artist in album_artists:
            if artist in artist_in_post: return True # presence of artist in post AND album title
    return False # no match

# Returns a subreddit Instance to query the subreddit
def get_reddit_instance():
    
    # Get full path
    dir_path = os.path.dirname(os.path.realpath(__file__))
    envars = os.path.join(dir_path, '.env')
    load_dotenv(envars)

    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = os.getenv("REDDIT_USER_AGENT")

    reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent )
    return reddit.subreddit('VinylReleases')