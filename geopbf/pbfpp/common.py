# -*- coding: utf-8 -*-
import logging
from .. import settings
import sys

logger = logging.getLogger("geopbf")
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
)
for item in settings.LOGGERS:
    level, filename = item.split(":", 1)
    if filename in ("stdout", "stderr"):
        handler = logging.StreamHandler(getattr(sys, filename))
    else:
        handler = logging.FileHandler(filename)
    handler.setFormatter(formatter)
    logger.setLevel(getattr(logging, level.upper(), "DEBUG"))
    logger.addHandler(handler)

if hasattr(settings, 'DB_URI') and not settings.DB_URI is None:

    from py4web import DAL

    db = DAL(settings.DB_URI,
        folder = settings.DB_FOLDER,
        pool_size = 1 if not hasattr(settings, 'DB_POOL_SIZE') else settings.DB_POOL_SIZE,
        migrate = hasattr(settings, 'DB_MIGRATE') and settings.DB_MIGRATE,
        fake_migrate = hasattr(settings, 'DB_FAKE_MIGRATE') and settings.DB_FAKE_MIGRATE,
        lazy_tables=False, check_reserved=False
    )

else:

    db = None
