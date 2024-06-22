# This script fetches the user wantlist and parses the data to retrieve the albums or singles the user wants
from datetime import datetime
from dotenv import load_dotenv 
import os, discogs_client, json

MAX_PAGES = 10 # Limit wantlist to 1000 albums
DISCOGS_USER = 'aross2010'


# Fetches wantlist Data from Discogs. Returns a list of dictionaries containing album title, artists, and the album cover to discogs.json. -> to be fetched every four hours
def get_wantlist_data():

    # Get full path
    dir_path = os.path.dirname(os.path.realpath(__file__))
    envars = os.path.join(dir_path, '.env')
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

    # Get full path
    dir_path = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(dir_path, 'discogs.json')

    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        
    except FileNotFoundError:
        print('discogs.json not found')

def main():
    get_wantlist_data()
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'{time} -> Updated Discogs data!')

main()