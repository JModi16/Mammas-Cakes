# Temporary file to force settings reload

import sys
import importlib

# Clear Django settings from cache
if 'django.conf' in sys.modules:
    del sys.modules['django.conf']

# Clear our settings module
if 'mammas_cakes.settings' in sys.modules:
    del sys.modules['mammas_cakes.settings']

print("🔄 Settings cache cleared")