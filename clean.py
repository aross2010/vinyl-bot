from helpers import read_posts_json, write_posts_json
import time,  os, json
from datetime import datetime

# Clear out posts from posts.json that are NOT younger than 5 minutes
def clean_posts():
    posts = read_posts_json()
    if not posts: return

    current_time = time.time()

    # Filter out posts older than a week (needs to be at least a weeek to avoid removing posts that can be viewed and sent again)
    posts = [post for post in posts if (current_time - post['time_posted']) < 604800]

    write_posts_json(posts)

def clean_log():
    # Get full path
    dir_path = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(dir_path, 'cron.log')

    try:
        with open(filename, 'w') as file:
                json.dump('', file, indent=4)
    except Exception:
        print('cron.log not found') 
            
def main():
    clean_posts()
    clean_log()
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'{time} -> Cleaned out old posts and logs!')

main()