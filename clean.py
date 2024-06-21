from helpers import read_posts_json
import time, json

# Clear out posts from posts.json that are NOT younger than 5 minutes
def clean_posts():
    posts = read_posts_json()
    if not posts: return

    current_time = time.time()

    # Filter out posts older than 5 minutes
    posts = [post for post in posts if (current_time - post['time_posted']) < 300]

    try:
        with open('posts.json', 'w') as file:
                json.dump(posts, file, indent=4)
    except Exception:
        print('posts.json not found, not able to write new posts')   
            

clean_posts()