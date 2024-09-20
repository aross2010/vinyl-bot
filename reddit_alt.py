from helpers import get_reddit_instance, read_discogs_json, read_last_seen_json, write_last_seen_json, is_valid_match, read_posts_json, write_posts_json
import time, datetime
from send_email import send_email


# Fetch reddit posts that contain the any artist in the wantlist -> to be ran every four hours
def get_artists_posts(ids):

    vinyl_releases = get_reddit_instance()
    discogs_data = read_discogs_json()
    last_seen = read_last_seen_json()['alt'] 

    if not discogs_data: return

    data = []
    last_id_seen = None

    # Posts in order from newest to oldest
    for submission in vinyl_releases.new(): # last 100 posts
        post = vars(submission)
        post_id = post['id']

        if post_id == last_seen: break # The rest of list has already been checked
        if not last_id_seen: last_id_seen = post_id # Set to the first new post seen
        if post_id in ids: continue # Email already sent, skip

        post_title = post['title']
        post_title_lower = post_title.lower()
        discogs_album_match = None

        # Search discog albums for a valid match
        for album in discogs_data:
            match = True
            for artist in album['artists']:
                if artist.lower().includes('various'): continue # Skip various artists
                if not is_valid_match(artist.lower(), post_title_lower): 
                    match = False
                    break
            if match:
                discogs_album_match = album
                break
        
        if not discogs_album_match: continue

        cover = post.get('tumbnail')
        if not cover: cover = discogs_album_match['cover']

        data.append({
            "title": discogs_album_match['title'],
            "artists": discogs_album_match['artists'],
            "cover": cover, # If no reddit thumbail image, use discogs cover
            "link": post.get('url', f'https://www.reddit.com/r/VinylReleases/comments/{post_id}'), # Either link to shop to buy or to post
            "id": post_id,
            "time_posted": post.get('created_utc', time.time()) # If somehow no time posted, use current time (close enough)
        })

    if last_id_seen: write_last_seen_json(False, last_id_seen) # if a new post was seen, update last id seen

    return data

# run every four hours, the alt script
def main():

    # Get recent posts to send with func
    recent_valid_posts = read_posts_json()

    try:
        ids = set([post['id'] for post in recent_valid_posts])
        email_data = get_artists_posts(ids)

        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if not email_data: 
            print(f'No email to send from alt - {time}')
            return
        
        send_email(email_data, False)
        print(f'{time} -> Email sent!', email_data)

        for album in email_data:
            recent_valid_posts.append({
                "id": album["id"],
                "time_posted": album['time_posted']
            })
        
        write_posts_json(recent_valid_posts)

    except Exception:
        print('Something went wrong fetching new posts.')


main()