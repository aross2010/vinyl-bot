from reddit_albums import get_album_posts
from email_sender import send_email

def main():
    email_data = get_album_posts()
    if not email_data: 
        print('No email to send')
        return

    send_email(email_data)
    
    

main()
# Use cron jobs to schedule scripts on Pi

# Call discogs.py every hour and write data to discogs.json (call every hour 1st minute)

# Call main.py every two minutes (even minutes)
# Fetche new posts with album names from discogs.json
# if the post id isnt in posts.json, send email and add post id, title, and time posted to posts.json

# Call clean.py every week, remove any posts that arent less than five minutes old

# If there are any errors, send an email error


# Handle case where there is no data from discogs