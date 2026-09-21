import os
import sys

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campusconnect.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
