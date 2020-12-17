# -*- coding: utf-8 -*-

import datetime
from py4web import Field

from . import settings
from .common import db

now = lambda : datetime.datetime.utcnow()

db.define_table("fcache",
    Field("name", required=True, notnull=True, unique=True),
    Field("file", uploadseparate=True, uploadfolder=settings.STATIC_UPLOAD_FOLDER),
    Field('created_on', 'datetime',
        default = now,
        writable=False, readable=False,
        label = 'Created On'
    ),
    Field('modified_on', 'datetime',
        update=now, default=now,
        writable=False, readable=False,
        label = 'Modified On'
    ),
    Field('timeout', 'integer', label="Timeout seconds")
)
