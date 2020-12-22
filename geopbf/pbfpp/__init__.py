# -*- coding: utf-8 -*-

import io
from py4web.core import redirect
from py4web import request, response
from mapbox_vector_tile import encode as mvt_encode
from kilimanjaro.frameworks.py4web.controller import WebWrapper

from .. import Prototizer, f2f
from .. import settings

from .common import logger
from .models import db, now
import datetime

CLIENT_EXPIRE_THRESHOLD = 3650000 # Just a big number, i.e. more than one year.

# import time, random

class Prototizerpp(Prototizer):
    """ """

    ver = '__version'

    def on_request_(self, version=None):

        if version is None:
            self.params = {}
        else:
            self.params = {self.ver: version}

        # url_path = request.path[1:].split('/')
        # self.kw = {k: v for k,v in request.query.items() if k.startswith('__')}

        self.now = now()
        self.public = (db.fcache.file.uploadfolder == settings.STATIC_UPLOAD_FOLDER)

    def on_request(self):
        """ called when a request arrives """

        if self.ver in request.query:
            self.on_request_(version=request.query.pop(self.ver))
        else:
            self.on_request_()

    def on_error(self):
        """ called when a request errors """

    def on_success(self, status):
        """ """
        response.headers["Content-Type"]="application/x-protobuf"

        if settings.CACHE_ON_CLIENT:
            time_expire = min([self.time_expire, CLIENT_EXPIRE_THRESHOLD])
            ctrl = 'public' if self.public else 'private'
            cache_control = f'max-age={time_expire}, s-maxage={time_expire}, {ctrl}'
            expires = (self.now + datetime.timedelta(seconds=time_expire)).strftime('%a, %d %b %Y %H:%M:%S GMT')
            headers = {
                'Pragma': None,
                'Expires': expires,
                'Cache-Control': cache_control,
                'Content-Disposition': f'inline; filename="{self.filename}"'
            }

            response.headers.update(headers)

    def __call__(self, func, stream_public=False, **defaults):
        get_stream = lambda : io.BytesIO(mvt_encode(WebWrapper.__call__(self, f2f(func), **defaults)()))
        def wrapper():
            kwargs = self.parse_request(func, **defaults)
            name = self._hash(func, **dict(kwargs, **self.params))
            self.filename = f"{name}{self.EXT}"
            rec = db.fcache(name=name)
            commit = False

            if rec is None:
                stream = get_stream()

                if settings.CACHE_NEW:
                    try:
                        newid = db.fcache.insert(
                            name = name,
                            file = db.fcache.file.store(stream, self.filename)
                        )
                    except AttributeError:
                        raise
                        self.time_expire = settings.CACHE_EXPIRE-(self.now - now()).seconds
                        return stream.read()
                    else:
                        rec = db.fcache[newid]
                        commit = True
                else:
                    self.time_expire = settings.CACHE_EXPIRE-(self.now - now()).seconds
                    return stream.read()

            elif (self.now - rec.modified_on).seconds > (rec.timeout or settings.CACHE_EXPIRE):
                stream = get_stream()
                rec.update(file=db.fcache.file.store(stream, self.filename))
                commit = True

            self.time_expire = (rec.timeout or settings.CACHE_EXPIRE)-(self.now - rec.modified_on).seconds

            if self.public and not stream_public:
                _, path_to_img = db.fcache.file.retrieve(rec.file, nameonly=True)
                if commit: db.commit()
                redirect(path_to_img[path_to_img.index('/'):])
            else:
                _, stream = db.fcache.file.retrieve(rec.file, nameonly=False)
                return stream.read()

        return wrapper
