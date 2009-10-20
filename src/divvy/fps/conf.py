
try:
    from django.conf import settings
except ImportError, e:
    # django not installed
    settings = object()

RUN_IN_SANDBOX = getattr(settings, "FPS_RUN_IN_SANDBOX", False)

DEFAULT_ACCESS_KEY_ID = getattr(settings, "FPS_DEFAULT_ACCESS_KEY_ID", None)
DEFAULT_SECRET_KEY = getattr(settings, "FPS_DEFAULT_SECRET_KEY", None)
DEFAULT_COBRANDING_URL = getattr(settings, "FPS_DEFAULT_COBRANDING_URL", None)
