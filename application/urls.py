"""
urls.py

URL dispatch route mappings and error handlers

"""
from flask import render_template

from application import app

from application.views.public.public_warmup import PublicWarmup
from application.views.public.public_index import PublicIndex
from application.views.public.public_say_hello import PublicSayHello

from application.views.admin.admin_list_examples import AdminListExamples
from application.views.admin.admin_list_examples_cached import AdminListExamplesCached
from application.views.admin.admin_secret import AdminSecret
from application.views.admin.admin_edit_example import AdminEditExample
from application.views.admin.admin_delete_example import AdminDeleteExample


from application.views.public.public_list_docs import PublicListDocs
from application.views.public.public_submit_doc import PublicSubmitDoc
from application.views.public.public_view_doc import PublicViewDoc
from application.views.admin.admin_delete_doc import AdminDeleteDoc

from application.views.admin.admin_list_passkeys import AdminListPasskeys
from application.views.admin.admin_delete_passkey import AdminDeletePasskey

# URL dispatch rules

# App Engine warm up handler
# See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests
app.add_url_rule('/_ah/warmup', 'public_warmup', view_func=PublicWarmup.as_view('public_warmup'))

app.add_url_rule('/', 'public_index', view_func=PublicIndex.as_view('public_index'))

app.add_url_rule('/hello/<username>', 'public_say_hello', view_func=PublicSayHello.as_view('public_say_hello'))

app.add_url_rule('/examples', 'list_examples', view_func=AdminListExamples.as_view('list_examples'), methods=['GET', 'POST'])

app.add_url_rule('/examples/cached', 'cached_examples', view_func=AdminListExamplesCached.as_view('cached_examples'))

app.add_url_rule('/admin_only', 'admin_only', view_func=AdminSecret.as_view('admin_only'))

app.add_url_rule('/examples/<int:example_id>/edit', 'edit_example', view_func=AdminEditExample.as_view('edit_example'), methods=['GET', 'POST'])

app.add_url_rule('/examples/<int:example_id>/delete', 'delete_example', view_func=AdminDeleteExample.as_view('delete_example'), methods=['POST'])


app.add_url_rule('/docs','list_docs', view_func=PublicListDocs.as_view('list_docs'), methods=["GET"])
app.add_url_rule('/docs/submit_doc', 'submit_doc', view_func=PublicSubmitDoc.as_view('submit_doc'), methods=["GET",'POST'])
app.add_url_rule('/doc/<bkey>/<filename>', 'view_doc', view_func=PublicViewDoc.as_view('view_doc'), methods=["GET"])
app.add_url_rule('/examples/<int:document_id>/delete', 'delete_doc', view_func=AdminDeleteDoc.as_view('delete_doc'), methods=['POST', 'GET'])

app.add_url_rule('/passkeys', 'list_passkeys', view_func=AdminListPasskeys.as_view('list_passkeys'), methods=["GET", "POST"])
app.add_url_rule('/passkeys/<int:passkey_id>/delete', 'delete_passkey', view_func=AdminDeletePasskey.as_view('delete_passkey'), methods=['POST', 'GET'])


# Error handlers

# Handle 404 errors


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Handle 500 errors


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
