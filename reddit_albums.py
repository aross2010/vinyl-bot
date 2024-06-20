import time
from reddit_instance import get_reddit_instance
import json

# Fetch reddit posts that contain the album name -> to be ran every couple of minutes
def get_album_posts():

    vinyl_releases = get_reddit_instance()

    try:
        with open('discogs.json', 'r') as file:
            try:
                discogs_data = json.load(file)
            except Exception:
                print('discogs.json is empty')
                discogs_data = None
    except FileExistsError:
        print('discogs.json not found')

    if not discogs_data: return

    try:
        with open('posts.json', 'r') as file:
            try:
                recent_valid_posts = json.load(file)
            except Exception:
                recent_valid_posts = None
    except Exception:
        print('posts.json not found')
    
    if not recent_valid_posts:
        recent_valid_posts = []
        ids = set()
    else:
        ids = set([post['id'] for post in recent_valid_posts])

    
    data = []
    post_ids_to_add = []
    current_time = time.time()


    # Posts in order from newest to oldest
    for submission in vinyl_releases.new(limit=10):
        post = vars(submission)
        time_posted = post['created_utc']
        time_since_post = current_time - time_posted
       # if time_since_post >= 300: break # If post is greater than 5 minutes old, break out of loop. The rest of the posts are older.

        post_id = post['id']

        if post_id in ids: continue # If sent already, skip

        post_title = post['title']
        post_title_lower = post_title.lower()
        discogs_album_match = None

        for album in discogs_data:
            if album['title'].lower() in post_title_lower:
                discogs_album_match = album
                break
        if not discogs_album_match: continue # No title match, skip

        post_ids_to_add.append({
            "id": post_id,
            "time_posted": time_posted,
        })

        data.append({
            "title": album['title'],
            "artists": album['artists'],
            "cover": post.get('thumbnail', album['cover']), # If no reddit thumbail image, use discogs cover
            "link": post.get('url', f'https://www.reddit.com/r/VinylReleases/comments/{post_id}') # Either link to shop to buy or to post
        })

        if post_ids_to_add: recent_valid_posts.extend(post_ids_to_add)

        try:
            with open('posts.json', 'w') as file:
                try:
                    json.dump(recent_valid_posts, file, indent=4)
                except Exception:
                    recent_valid_posts = None
        except Exception:
            print('posts.json not found')   

        return data
        
    