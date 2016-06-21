# -*- coding: utf-8 -*-

from flask.views import View

from flask import redirect, url_for

from google.appengine.ext import blobstore

from flask import make_response

class PublicViewDoc(View):

    def dispatch_request(self, bkey, filename):    
		blob_info = blobstore.get(bkey)
		response = make_response(blob_info.open().read())
		response.headers['Content-Type'] = blob_info.content_type
		return response
