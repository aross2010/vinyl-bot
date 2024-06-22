
# Use cron jobs to schedule scripts on Pi

# Call discogs.py every morning at 3:01 am and write data to discogs.json 

# Call reddit_main.py every two minutes (even minutes)
# Fetch new posts with album names from discogs.json
# if the post id isnt in posts.json, send email and add post id, title, and time posted to posts.json

# Call reddit_alt.py every 8:01am, 12:01pm, 8:01pm

# Call clean.py every week 3:03 am, Sundays, remove any posts that arent less than five minutes old

# If there are any errors, send an email error


# Packages to install -> praw, discogs_client, dotenv, jinja2

# Crontab -> Vim, Press i, enter command, esc, :wq

# /usr/bin/python3 /home/aross/vinyl-bot/vinyl-bot/reddit_main.py

# Main script ran every even minute
# */2 * * * * /usr/bin/python3 /home/aross/vinyl-bot/vinyl-bot/reddit_main.py >> /home/aross/vinyl-bot/vinyl-bot/cron.log 2>&1

# # Alt script ran every night at 8:59pm
# 59 8 * * * /usr/bin/python3 /home/aross/vinyl-bot/vinyl-bot/reddit_alt.py >> /home/aross/vinyl-bot/vinyl-bot/cron.log 2>&1

# # Discogs script every one minute past the fourth hour
# 1 */4 * * * /usr/bin/python3 /home/aross/vinyl-bot/vinyl-bot/discogs.py >> /home/aross/vinyl-bot/vinyl-bot/cron.log 2>&1    

# # Cleaning script every Monday at 1:01 am
# 1 1 * * 1 /usr/bin/python3 /home/aross/vinyl-bot/vinyl-bot/clean.py >> /home/aross/vinyl-bot/vinyl-bot/cron.log 2>&1
