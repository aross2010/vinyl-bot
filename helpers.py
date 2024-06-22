import json, os, praw
from dotenv import load_dotenv

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

    try:
        with open(filename, 'r') as file:
                return json.load(file)
    except Exception:
        print('last_seen.json not found')

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

# Validates whether a key is in a string. The key must be its own word or be a word with a non-letter trailing and leading it
def is_valid_match(key: str, post: str):
    while True:
        start_index = post.find(key)
        if start_index == -1: return False
        start_index_minus = max(0, start_index - 1)
        end_index_plus = min(len(post), start_index + len(key) + 1)
        post_substring = post[start_index_minus:end_index_plus]
        if post_substring[0].isalpha() or post_substring[-1].isalpha(): # No match, search rest of post after found substring
            post = post[start_index+len(key)+1:] 
        else: 
            return True

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