from flask import make_response, render_template

from .app import app


@app.errorhandler(401)
def internal_error(e):
    resp = make_response(render_template('401.html'))
    resp.headers['WWW-Authenticate'] = 'Basic realm=""'
    resp.status_code = 401
    return resp


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.errorhandler(403)
def permission_denied(e):
    return render_template('403.html')
