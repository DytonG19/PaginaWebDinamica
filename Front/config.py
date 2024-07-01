class config:
    SECRET_KEY = 'B!1w8NAt1T^%kvhUI*S^'

class DevelopmentConfig(config):
    DEBUG = True

config = {
    'development': DevelopmentConfig
}
