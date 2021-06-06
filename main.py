import praw
import configparser
from datetime import date
import pymongo

# https://praw.readthedocs.io/en/latest/getting_started/quick_start.html


def replyTo(content, message):
    if DEBUG:
        print(message)
    else:
        content.reply(message)


def getTopDailyPostForSub(reddit, subreddit):
    topPost = None
    postsToScan = 10

    for submission in reddit.subreddit(subreddit).top(limit=postsToScan, time_filter='day'):
        if topPost is None or submission.score > topPost.score:
            topPost = submission

    return topPost


def updateLeaderboard(post):
    if not DEBUG:
        pass


def getUserData(user):
    return None


def endOfDayUpdate(reddit, subList):
    for subreddit in subList:
        topPost = getTopDailyPostForSub(reddit=reddit, subreddit=subreddit)
        updateLeaderboard(topPost)
        user = getUserData(topPost)

        # print(datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S'))

        message = ('Congratulations! Your post was the top post on r/' + subreddit +
                   ' today! (' + date.today().strftime("%m/%d/%y") + ')' +
                   '\n\nTop Post Counts: ' + subreddit)

        message += (
            "\n\n*This comment was made by a bot*"
        )

        replyTo(content=topPost, message=message)


def connectToDatabase():
    client = pymongo.MongoClient(
        "mongodb+srv://AllAccessUser:" + config['MongoAtlas']['password'] +
        "@cluster0.4wktl.mongodb.net/" + config['MongoAtlas']['databaseName'] + "?retryWrites=true&w=majority")
    with client:
        db = client.leaderboard_bot
        #db.leaderboard_bot.insert({'name': 'James'})


# ------------------------------------------------------
# Main Code
# ------------------------------------------------------
def main():
    subreddits = ['Grimdank']

    redditConfig = config['Reddit']

    reddit = praw.Reddit(
        client_id=redditConfig['client_id'],
        client_secret=redditConfig['client_secret'],
        user_agent=redditConfig['user_agent'],
        username=redditConfig['username'],
        password=redditConfig['password']
    )

    # endOfDayUpdate(reddit=reddit, subList=subreddits)
    connectToDatabase()


config = configparser.ConfigParser()
config.read('config.cfg')
DEBUG = bool(config['App']['debug'])

if __name__ == '__main__':
    main()
