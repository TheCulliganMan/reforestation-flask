# -*- coding: utf-8 -*-

from flask.views import View

from flask import flash, redirect, url_for, render_template

from google.appengine.api import users
from google.appengine.api import images
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError


from decorators import login_required

from models import DocModel

from google.appengine.ext import blobstore

class PublicListDocs(View):

	@login_required
	def dispatch_request(self):

		docs = DocModel.query()
		
		uploadUri = blobstore.create_upload_url(url_for("submit_doc"))
		return render_template('list_docs.html', docs=docs, upload_uri=uploadUri)