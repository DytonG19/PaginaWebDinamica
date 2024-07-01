class configuracion:
    SECRET_KEY = ''

class DevelopmentConfig(configuracion):
    DEBUG = True

configuracion = {
    'development': DevelopmentConfig
}
