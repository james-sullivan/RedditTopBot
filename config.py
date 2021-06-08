import configparser
from os import environ

data = configparser.ConfigParser()
data.read('config.cfg')
DEBUG = bool(data['App']['debug'])

# If we're in debug mode, then we can access the environ varibles
if DEBUG:
    sensitiveData = configparser.ConfigParser()
    sensitiveData.read('local_sensitive_config.cfg')
    REDDIT_CLIENT_SECRET = sensitiveData['Reddit']['client_secret']
    REDDIT_PASSWORD = sensitiveData['Reddit']['password']
    DB_PASSWORD = sensitiveData['MongoAtlas']['password']
else:
    REDDIT_CLIENT_SECRET = environ['REDDIT_CLIENT_SECRET']
    REDDIT_PASSWORD = environ['REDDIT_PASSWORD']
    DB_PASSWORD = environ['DB_PASSWORD']
