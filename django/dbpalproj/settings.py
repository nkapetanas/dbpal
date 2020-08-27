import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, 'dbpal'))

if 'DJANGO_SETTINGS' in os.environ:
    if os.environ['DJANGO_SETTINGS'] == "dev":
        print ("DEV SERVER")
        from .settings_dev import *
else:
    # print ("PROD SERVER")
    # from .settings_prod import *
    print("DEV SERVER")
    from .settings_dev import *
