import os
from app import create_app
from config import config

env = os.environ.get('FLASK_ENV', 'production')
application = create_app(config[env])

if __name__ == '__main__':
    application.run()