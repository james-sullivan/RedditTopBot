import time
import db_connection
import praw
import config
from datetime import date
from praw.exceptions import RedditAPIException
from pymongo.errors import ConnectionFailure


# https://praw.readthedocs.io/en/latest/getting_started/quick_start.html

# Hosting
# https://dashboard.heroku.com/apps/reddit-leaderboard-bot
# https://github.com/james-sullivan/RedditTopBot

def replyTo(content, message):
    if config.DEBUG:
        print(message)
    else:
        try:
            content.reply(message)
        except RedditAPIException as error:
            print(error)


def getTopDailyPostForSub(reddit, subreddit):
    topPost = None
    postsToScan = 10

    for submission in reddit.subreddit(subreddit).top(limit=postsToScan, time_filter='day'):
        if topPost is None or submission.score > topPost.score:
            topPost = submission

    return topPost


def endOfDayUpdate(reddit, subList, connection: db_connection.DBConnection):
    print("Running end of day update:")

    for subreddit in subList:
        try:
            topPost = getTopDailyPostForSub(reddit=reddit, subreddit=subreddit)

            print('Subreddit: ' + subreddit)

            user = connection.addPostToUser(username=topPost.author.name, subreddit=subreddit)

            message = ('Congratulations u/' + topPost.author.name + ' ! Your post was the top post on r/' + subreddit +
                       ' today! (' + date.today().strftime("%m/%d/%y") + ')' +
                       '\n\nTop Post Counts: ')

            subTextList = []

            for sub in user.subs:
                subTextList.append('r/' + sub + ' (' + str(user.subs[sub]) + ') ')

            message += ', '.join(subTextList)

            message += (
                "\n\n*This comment was made by a bot*"
            )

            replyTo(content=topPost, message=message)

            if not config.DEBUG:
                # Reddit's API only allows comments to be written once every 2 seconds
                time.sleep(3)

        except RedditAPIException as error:
            print(error)


# ------------------------------------------------------
# Main Code
# ------------------------------------------------------
def main():
    print("Start of Main")

    reddit = praw.Reddit(
        client_id=config.REDDIT_CLIENT_ID,
        client_secret=config.REDDIT_CLIENT_SECRET,
        user_agent=config.REDDIT_USER_AGENT,
        username=config.REDDIT_USERNAME,
        password=config.REDDIT_PASSWORD
    )

    try:
        connection = db_connection.DBConnection(databaseName=config.data['MongoAtlas']['databaseName'],
                                                password=config.DB_PASSWORD)

        subList = config.data['App']['subs'].split(',')

        endOfDayUpdate(reddit=reddit, subList=subList, connection=connection)
    except ConnectionFailure as error:
        print(error)


if __name__ == '__main__':
    main()
