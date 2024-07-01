class config:
    SECRET_KEY = ''

class DevelopmentConfig(config):
    DEBUG = True

config = {
    'development': DevelopmentConfig
}
