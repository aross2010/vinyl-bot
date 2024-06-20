from reddit_instance import get_reddit_instance


# Fetch reddit posts that contain the any artist in the watchlist -> to be ran every night at 10pm. Find way to run AFTER get_album_posts
def get_artists_posts(recent_albums_sent, wantlist_data):

    vinyl_releases = get_reddit_instance()

    None