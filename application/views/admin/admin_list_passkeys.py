# -*- coding: utf-8 -*-

from flask.views import View

from flask import flash, redirect, url_for, render_template

from google.appengine.api import users
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from forms import PasskeyForm
from models import PasskeyModel

from decorators import admin_required


class AdminListPasskeys(View):
    
    @admin_required
    def dispatch_request(self):
        passkeys = PasskeyModel.query()
        form = PasskeyForm()
        if form.validate_on_submit():
            passkey = PasskeyModel(
                passkey=form.passkey.data
            )
            try:
                passkey.put()
                passkey_id = passkey.key.id()
                flash(u'Passkey %s successfully saved.' % passkey_id, 'success')
                return redirect(url_for('list_passkeys'))
            except CapabilityDisabledError:
                flash(u'App Engine Datastore is currently in read-only mode.', 'info')
                return redirect(url_for('list_passkeys'))
        return render_template('list_passkeys.html', passkeys=passkeys, form=form)
