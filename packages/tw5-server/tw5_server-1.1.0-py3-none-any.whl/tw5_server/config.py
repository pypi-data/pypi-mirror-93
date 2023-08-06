import os
from pathlib import Path
from p_config import Config

BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR.joinpath('static')


class MyConfig(Config):
    wiki_root = Path


CONFIG = MyConfig(
    base_dir=BASE_DIR,
    auth_basic_user_file=BASE_DIR.joinpath('basic_auth_file.ini'),
    default_view_key='to-be-changed',
    default_write_key='to-be-changed',
    wiki_root=Path.home().joinpath('.local/share', 'tw5_server'),
    blank_wiki_file=STATIC_DIR.joinpath('empty_tw5.html'),
)

CONFIG.load_env()
if os.environ.get('TW5_SERVER_CONFIG'):
    CONFIG.load_file(os.environ['TW5_SERVER_CONFIG'])
