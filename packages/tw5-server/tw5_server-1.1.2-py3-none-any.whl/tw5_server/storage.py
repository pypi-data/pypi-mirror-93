import abc
from functools import cached_property
import os
import shutil

from git import Repo
from git.util import Actor

from .config import CONFIG


class Base(abc.ABC):
    WIKI_FILE = 'index.html'
    ROOT = CONFIG.WIKI_ROOT

    def __init__(self, name, root=None):
        root = root or self.ROOT
        self.dirpath = root.resolve().joinpath(name)
        self.filepath = self.dirpath.joinpath(self.WIKI_FILE)

    def exists(self):
        return self.filepath.exists()

    @classmethod
    def create(cls, name, root=None, **kwargs):
        root = root or cls.ROOT
        dirpath = root.resolve().joinpath(name)
        if not dirpath.exists():
            os.makedirs(dirpath)
        else:
            raise RuntimeError(f'{dirpath} already exists')
        cls._init_storage(dirpath)
        return cls(name, root=root, **kwargs)

    @abc.abstractclassmethod
    def _init_storage(cls, dirpath):
        pass

    @abc.abstractmethod
    def update(self):
        pass


class GitStorage(Base):
    author = Actor('tw5-server', '')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @cached_property
    def repo(self):
        return Repo(self.dirpath)

    @classmethod
    def _init_storage(cls, dirpath):
        try:
            repo = Repo.init(dirpath)
            filepath = dirpath.joinpath(cls.WIKI_FILE)
            shutil.copy(CONFIG.BLANK_WIKI_FILE, filepath)
            repo.index.add(cls.WIKI_FILE)
            repo.index.commit('automatic create', author=cls.author)
        except Exception as err:
            if dirpath.exists():
                shutil.rmtree(dirpath)
            raise err

    def update(self, file_obj):
        with open(self.filepath, 'wb') as f:
            shutil.copyfileobj(file_obj, f)
        self.repo.index.add(self.WIKI_FILE)
        self.repo.index.commit('automatic commit', author=self.author)
