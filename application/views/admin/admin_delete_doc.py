# -*- coding: utf-8 -*-

from flask.views import View

from flask import flash, redirect, url_for, request

from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from models import DocModel

from decorators import login_required


class AdminDeleteDoc(View):

    @login_required
    def dispatch_request(self, document_id):
        document = DocModel.get_by_id(document_id)
        try:
            try:
                document.key.delete()
            except AttributeError:
                return redirect(url_for('list_docs'))
            flash(u'document %s successfully deleted.' % document_id, 'success')
            return redirect(url_for('list_docs'))
        except CapabilityDisabledError:
            flash(u'App Engine Datastore is currently in read-only mode.', 'info')
            return redirect(url_for('list_docs'))
