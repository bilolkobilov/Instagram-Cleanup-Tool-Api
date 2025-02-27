# Instagram Cleanup API

A RESTful API service for managing and cleaning up Instagram content, including posts, reels, and messages.

## Features

- Delete Instagram posts, reels, and direct messages
- Control deletion with rate limiting to avoid API blocks
- Specify maximum number of items to delete
- Monitor deletion progress and statistics
- User authentication with Instagram credentials

## Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file with your settings:
   ```
   FLASK_ENV=development
   FLASK_DEBUG=true
   SECRET_KEY=your-secret-key
   CORS_ORIGIN=*
   ```

## Running the Application

### Development

```bash
python run.py
```

### Production

```bash
gunicorn wsgi:application
```

## API Endpoints

### Authentication

- `POST /api/login` - Log in with Instagram credentials
- `POST /api/logout` - Log out from Instagram
- `GET /api/status` - Check login status

### Content Management

- `POST /api/delete` - Start deletion process (posts, reels, or messages)
- `GET /api/stats` - Get deletion statistics
- `POST /api/cancel` - Cancel deletion process

## License

[MIT](LICENSE)
