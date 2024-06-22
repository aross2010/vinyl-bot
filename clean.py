from helpers import read_posts_json, write_posts_json
import time, datetime

# Clear out posts from posts.json that are NOT younger than 5 minutes
def clean_posts():
    posts = read_posts_json()
    if not posts: return

    current_time = time.time()

    # Filter out posts older than 5 minutes
    posts = [post for post in posts if (current_time - post['time_posted']) < 300]

    write_posts_json(posts)
            
def main():
    clean_posts()
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'{time} -> Cleaned out old posts!')

main()