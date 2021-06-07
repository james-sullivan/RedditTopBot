import configparser

data = configparser.ConfigParser()
data.read('config.cfg')
DEBUG = bool(data['App']['debug'])
