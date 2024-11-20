# Mood Melody Nepal

An music player that suggests YouTube playlists based on your detected emotional state.

## Features

- Real-time emotion detection using webcam
- Mood-based playlist recommendations
- YouTube playlist integration
- Responsive web interface
- Support for multiple emotional states (Happy, Sad, Angry, Neutral, Surprise, Calm)

## Tech Stack

- Python/Django
- TensorFlow for emotion detection
- YouTube Data API
- Bootstrap 5
- JavaScript/AJAX

## Setup

1. Clone the repository:
```bash
git clone https://github.com/publishername/MoodMelodyNepal.git
```

2. Change the directory:
```bash
cd MoodMelodyNepal
```

3. Set up a virtual environment:
```bash
python -m venv .venv
source venv/bin/activate
```

4. Install the dependencies:
```bash
pip install -r requirements.txt
```

5. Copy the `.env.example` file to `.env` and set the environment variables:
```bash
cp .env.example .env
```

6. Load Dummy Playlist:
```bash
python manage.py loaddata seeds/music.json
```

7. Run the server:
```bash
python manage.py runserver
```

8. Open the web interface in your browser:
```bash
http://127.0.0.1:8000/
```
