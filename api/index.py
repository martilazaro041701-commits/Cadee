import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application

ROOT = Path(__file__).resolve().parent.parent
PROJECT_ROOT = ROOT / "Cadee"
sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cadee_core.settings")

application = get_wsgi_application()
app = application
