"""
WSGI config for bureaucrat_app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import nltk  # Import nltk

# Download punkt tokenizer
nltk.download('punkt')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bureaucrat_app.settings')

application = get_wsgi_application()
