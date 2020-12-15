# -*- coding: utf-8 -*-

import io
from py4web.core import redirect

from .. import prototize
from .. import settings

from .hashit import hashit

from .models import db, now

ext = '.pbf'

get_name = lambda *args, **kwargs: "{}.{}".format(*map(hashit, (args, kwargs)))

class Prototizer(object):
    """docstring for Prototizer."""
    def __init__(self, arg):
        super(Prototizer, self).__init__()
        self.arg = arg

def prototizepp(func):
    """
    Warning: func must return a dictionary with at least a 'features' key.
    """
    get_stream = lambda *args, **kwargs: io.BytesIO(prototize(func)(*args, **kwargs))
    def wrapper(x, y, z, **kwargs):
        """ """
        name = get_name(x, y, z, **kwargs)
        filename = f"{name}{ext}"
        rec = db.fcache(name=name)
        if rec is None:
            stream = get_stream(x, y, z, **kwargs)
            newid = db.fcache.insert(
                name = name,
                file = db.fcache.file.store(stream, filename)
            )
            rec = db.fcache[newid]
        elif (now() - rec.modified_on).seconds > (rec.timeout or settings.CACHE):
            stream = get_stream(x, y, z, **kwargs)
            rec.update(file=db.fcache.file.store(stream, filename))

        db.commit()
        if db.fcache.file.uploadfolder == settings.STATIC_UPLOAD_FOLDER:
            _, path_to_img = db.fcache.file.retrieve(rec.file, nameonly=True)
            redirect(path_to_img[path_to_img.index('/'):])
        else:
            _, stream = db.fcache.file.retrieve(rec.file, nameonly=False)
            return stream.read()

    return wrapper
