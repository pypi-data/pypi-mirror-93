from flask import abort, request, send_file

from . import auth, storage, utils
from .app import app


# wiki
@app.route('/<string:wiki_name>')
@auth.view_premission_required
def get_wiki(wiki_name):
    wiki = storage.GitStorage(wiki_name)
    if not wiki.exists():
        abort(404)
    return send_file(wiki.filepath)


@app.route('/<string:wiki_name>/store', methods=['POST'])
@auth.view_premission_required
def update_wiki(wiki_name):
    params = utils.split_params(request.form.get('UploadPlugin', ''))
    password = params.get('password')
    if not auth.can_write(wiki_name, password):
        abort(401)
    file_obj = request.files.get('userfile')
    if not file_obj or file_obj.mimetype != 'text/html':
        abort(400)
    wiki = storage.GitStorage(wiki_name)
    if not wiki.exists():
        abort(404)
    wiki.update(file_obj.stream)
    return '0 - '
