# -*- coding: utf-8 -*-

import os

from pathlib import Path
HOME = str(Path.home())

# db settings
APP_FOLDER = HOME

# DB_FOLDER:    Sets the place where migration files will be created
#               and is the store location for SQLite databases
DB_FOLDER = os.path.join(APP_FOLDER, "databases")
DB_URI = "sqlite://vtile_cache.db"
# DB_POOL_SIZE = 1
DB_MIGRATE = True
# DB_FAKE_MIGRATE = False  # maybe?

# location where to store uploaded files:
UPLOAD_FOLDER = os.path.join(APP_FOLDER, "uploads")
STATIC_UPLOAD_FOLDER = os.path.join(APP_FOLDER, "static", "uploads")

CACHE = float('Inf')

# try import private settings
try:
    from .settings_private import *
except (ImportError, ModuleNotFoundError):
    pass