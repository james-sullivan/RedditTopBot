import configparser
from os import environ
from dotenv import load_dotenv

load_dotenv()

data = configparser.ConfigParser()
data.read('config.cfg')
DEBUG = data['App']['debug'].lower() == 'true'

REDDIT_USER_AGENT = environ['REDDIT_USER_AGENT']
REDDIT_USERNAME = environ['REDDIT_USERNAME']
REDDIT_CLIENT_ID = environ['REDDIT_CLIENT_ID']
REDDIT_CLIENT_SECRET = environ['REDDIT_CLIENT_SECRET']
REDDIT_PASSWORD = environ['REDDIT_PASSWORD']
DB_PASSWORD = environ['DB_PASSWORD']
