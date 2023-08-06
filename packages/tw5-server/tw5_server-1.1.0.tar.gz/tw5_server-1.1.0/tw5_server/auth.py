from collections import namedtuple
import configparser
from functools import wraps

from flask import abort, request

from .config import CONFIG

Credential = namedtuple('Credential', ['write_key', 'view_key'])


def get_credential(wiki_name):
    config = configparser.ConfigParser()
    config.read(CONFIG.AUTH_BASIC_USER_FILE)
    if wiki_name in config:
        view_key = config[wiki_name].get('view_key', CONFIG.DEFAULT_VIEW_KEY)
        write_key = config[wiki_name].get('write_key', CONFIG.DEFAULT_WRITE_KEY)
    else:
        view_key = CONFIG.DEFAULT_VIEW_KEY
        write_key = CONFIG.DEFAULT_WRITE_KEY
    return Credential(write_key, view_key)


def can_write(wiki_name, key):
    credential = get_credential(wiki_name)
    return key == credential.write_key


def can_view(wiki_name, key):
    credential = get_credential(wiki_name)
    return key == credential.view_key


def view_premission_required(f):
    @wraps(f)
    def decorated_function(wiki_name, *args, **kwargs):
        authorization = request.authorization or {}
        password = authorization.get('password')
        if not can_view(wiki_name, password):
            abort(401)
        return f(wiki_name, *args, **kwargs)

    return decorated_function


def write_permission_required(f):
    @wraps(f)
    def decorated_function(wiki_name, *args, **kwargs):
        authorization = request.authorization or {}
        password = authorization.get('password')
        if not can_write(wiki_name, password):
            abort(401)
        return f(wiki_name, *args, **kwargs)

    return decorated_function
