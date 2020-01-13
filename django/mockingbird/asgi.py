import os
import django
from channels.routing import get_default_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mockingbird.settings")
channel_layer = channels.asgi.get_channel_layer()
# django.setup()
# application = get_default_application()
