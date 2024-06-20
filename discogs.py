# This script fetches the user wantlist and parses the data to retrieve the albums or singles the user wants
from pathlib import Path
from dotenv import load_dotenv 
import os
import discogs_client
import json

MAX_PAGES = 10 # Limit wantlist to 1000 albums
DISCOGS_USER = 'aross2010'


# Fetches wantlist Data from Discogs. Returns a list of dictionaries containing album title, artists, and the album cover to discogs.json. -> to be fetched hourly
def get_wantlist_data():

    current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd() # Return current folder
    envars = current_dir / ".env"
    load_dotenv(envars)

    app_name = os.getenv("DISCOGS_APP")
    user_token = os.getenv("DISCOGS_TOKEN")

    discogs = discogs_client.Client(app_name, user_token=user_token)

    wantlist = discogs._get(f'https://api.discogs.com/users/{DISCOGS_USER}/wants?page=1&per_page=100')

    data = []

    while wantlist:
        albums = wantlist['wants']
        for album in albums:
            info = album['basic_information']
            title = info.get('title', None)
            artists = info.get('artists', None)
            artist_names = [artist.get('name', None) for artist in artists]
            cover = info.get('cover_image', None)
            data.append({
                "title": title,
                "artists": artist_names,
                "cover": cover
            })
        wantlist_url = wantlist['pagination']['urls'].get('next', None) # if no url, wantlist_url = None
        if not wantlist_url: break
        wantlist = discogs._get(wantlist_url)
    try:
        with open('discogs.json', 'w') as file:
            json.dump(data, file, indent=4)
        
    except FileNotFoundError:
        print('discogs.json not found')


# get wantlist every hour, check reddit every minute
# daily recap of artists that might have released, every minute check albums 

get_wantlist_data()