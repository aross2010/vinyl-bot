from pathlib import Path
from dotenv import load_dotenv 
import os
import praw

# Returns a subreddit Instance to query the subreddit
def get_reddit_instance():
    current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd() # Return current folder
    envars = current_dir / ".env"
    load_dotenv(envars)

    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = os.getenv("REDDIT_USER_AGENT")

    reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent )
    return reddit.subreddit('VinylReleases')