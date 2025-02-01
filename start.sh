#!/bin/bash

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Download nltk punkt data
python -c "import nltk; nltk.download('punkt')"

# Start your Django application
gunicorn bureaucrat_app.wsgi:application --bind 0.0.0.0:8000