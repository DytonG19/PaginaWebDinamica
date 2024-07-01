class configuracion:
    SECRET_KEY = 'B!1w8NAt1T^%kvhUI*S^'

class DevelopmentConfig(configuracion):
    DEBUG = True

configuracion = {
    'development': DevelopmentConfig
}
