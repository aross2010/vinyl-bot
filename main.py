
# Use cron jobs to schedule scripts on Pi

# Call discogs.py every morning at 3:01 am and write data to discogs.json 

# Call reddit_main.py every two minutes (even minutes)
# Fetch new posts with album names from discogs.json
# if the post id isnt in posts.json, send email and add post id, title, and time posted to posts.json

# Call reddit_alt.py every 8:01am, 12:01pm, 8:01pm

# Call clean.py every week 3:03 am, Sundays, remove any posts that arent less than five minutes old

# If there are any errors, send an email error


# Packages to install -> praw, discogs_client, dotenv, jinja2