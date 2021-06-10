from typing import Dict
import jsonpickle
import pymongo
import config


class User:

    def __init__(self, subList: Dict[str, int] = None):
        self.subs = subList


class DBConnection:

    def __init__(self, databaseName: str, password: str):
        client = pymongo.MongoClient(
            "mongodb+srv://AllAccessUser:" + password +
            "@cluster0.4wktl.mongodb.net/" + databaseName + "?retryWrites=true&w=majority")

        with client:
            if config.DEBUG:
                self._db = client.test
            else:
                self._db = client.leaderboard_bot

            self._users = self._db['redditors']

    # Returns None if no user is found
    def getUser(self, username: str) -> None or User:
        user = self._users.find_one({config.data['MongoAtlas']['idName']: username})

        if user is None:
            return None

        return jsonpickle.decode(user[config.data['MongoAtlas']['item']])

    # Returns the user that it added the post count to
    def addPostToUser(self, username, subreddit) -> User:
        user = self.getUser(username)

        # Create the user if it doesn't exist
        if user is None:
            user = self._addUser(username)

        if user.subs is not None and subreddit in user.subs:
            user.subs[subreddit] += 1
        else:
            user.subs = dict()
            user.subs[subreddit] = 1

        self._users.update_one({config.data['MongoAtlas']['idName']: username},
                               {"$set": {config.data['MongoAtlas']['item']: jsonpickle.encode(user)}})

        return user

    # Returns the user that it added
    def _addUser(self, username: str) -> User:

        newUser = User()

        self._users.insert_one({config.data['MongoAtlas']['idName']: username,
                                config.data['MongoAtlas']['item']: jsonpickle.encode(newUser)})

        return newUser
