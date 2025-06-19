# VinylBot 🤖

<img src="https://github.com/aross2010/vinyl-bot/assets/121838301/ed9e7014-6605-4d74-9f90-49b72137d73b" height="450"/>

VinylBot gives you real-time notifications on the vinyl drops you need! It regularly checks your Discogs watchlist to automatically know what you're looking for and utilizes r/VinylReleases to send you an email the minute something you want is posted. Here's how to download your own VinylBot for the music you need:

### Pre-requisites

1. Must have [Python](https://www.python.org/downloads/) installed
2. Have a Reddit and Discogs account

### Installation Instructions

#### 1. Clone Repository

```
git clone https://github.com/aross2010/vinyl-bot.git
```

#### 2. Gather API keys

[Reddit](https://www.reddit.com/wiki/api/)
[Discogs](https://www.discogs.com/settings/developers)
[Email](https://mailmeteor.com/blog/gmail-smtp-settings)

Fill out the .env file with the keys –

EMAIL_SENDER=
EMAIL_SENDER_PASSWORD=
EMAIL_APP_PASSWORD=
EMAIL_RECEPIENT=
DISCOGS_APP=
DISCOGS_TOKEN=
REDDIT_CLIENT_ID=
REDDIT_CLIENT_SECRET=
REDDIT_USER_AGENT=

#### 3. Install Dependencies

```
pip install -r requirements.txt
```

#### 4. Run Cron Commands to Schedule Scripts

```
crontab -e
```

Select Vim as the editor and press 'i' to insert the following text:

```
# Main script ran every even minute
*/2 * * * * [python3 path] [insert path]/reddit_main.py >> [project folder path]/cron.log 2>&1

# # Alt script ran every day at 12:59pm (typically when releases are finished for the day)
59 12 * * * [python3 path] [insert path]/reddit_alt.py >> [project folder path]/cron.log 2>&1

# # Discogs script every four hours at the first minute
1 */4 * * * [python3 path] [insert path]/discogs.py >> [project folder path]/cron.log 2>&1

# # Cleaning script every Sunday at 11:59pm
59 11 * * 6 [python3 path] [insert path]/clean.py >> [project folder path]/cron.log 2>&1
```

Press 'esc' and ':wq' enter to quit and write out of the editor.

#### 5. VinylBot Does the Rest!
