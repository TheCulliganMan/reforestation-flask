# -*- coding: utf-8 -*-

from flask.views import View

from flask import flash, redirect, url_for, request

from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from models import PasskeyModel

from decorators import admin_required


class AdminDeletePasskey(View):

    @admin_required
    def dispatch_request(self, passkey_id):
        passkey = PasskeyModel.get_by_id(passkey_id)
        try:
            try:
                passkey.key.delete()
                flash(u'Passkey %s successfully deleted.' % passkey_id, 'success')
            except AttributeError:
                pass
            return redirect(url_for('list_passkeys'))
        except CapabilityDisabledError:
            flash(u'App Engine Datastore is currently in read-only mode.', 'info')
            return redirect(url_for('list_passkeys'))
