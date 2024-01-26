"""
asgi.py and wsgi.py: These files are used to serve your application. 
asgi.py is used for asynchronous applications, while wsgi.py is used for synchronous applications. 
They both contain the logic needed to start the server and handle requests.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'outfitted.settings')

application = get_asgi_application()
