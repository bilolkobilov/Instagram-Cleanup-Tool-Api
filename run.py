import os
from app import create_app
from config import config

env = os.environ.get('FLASK_ENV', 'development')
app = create_app(config[env])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    
    print(f'Starting server at port {port}')  
    app.run(debug=debug, host='0.0.0.0', port=port)