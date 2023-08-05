from pathlib import Path
from os import environ
from more_itertools import unique_everseen
from itertools import chain
from dataclasses import dataclass
from collections.abc import Sequence, Mapping
from ruamel.yaml import YAML
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from asyncio import get_running_loop

executor = ThreadPoolExecutor(max_workers=5)


__all__ = (
    'ProgramFiles',
    'File',
)


@dataclass
class File:
    name: str
    write_dir: Path
    search_dirs: Sequence

    def __post_init__(self):
        self.yaml = YAML(pure=True)
        self.yaml.default_flow_style = False
        self.write_dir = self.write_dir / self.name
        self.search_dirs = tuple(
            path / self.name
            for path in self.search_dirs
        )
        self.__data_future = None
        self.__lock = Lock()
        self.__create_future()

    @property
    def data(self) -> Mapping:
        with self.__lock:
            return self.__data_future.result()

    def reload(self):
        self.__create_future()

    def __create_future(self):
        with self.__lock:
            if self.__data_future and self.__data_future.running():
                self.__data_future.cancel()
            self.__data_future = executor.submit(self.load_files)

    def merge(self, data_mappings):
        new = {}
        for mapping in data_mappings:
            new.update(mapping)

        return new

    def load_files(self):
        data_mappings = (
            self.read_file(file)
            for file in reversed(self.search_dirs)
        )

        return self.merge(
            filter(
                lambda mapping: mapping is not None,
                data_mappings,
            ),
        )

    def read_file(self, path):
        try:
            with open(path, 'r') as file_obj:
                return self.yaml.load(file_obj)
        except FileNotFoundError:
            return None

    async def get_data(self):
        return await self.__data_future

    def write_file_sync(self, new_data):
        self.write_dir.parent.mkdir(parents=True, exist_ok=True)
        with self.write_dir.open('w') as file_obj:
            self.yaml.dump(new_data, file_obj)

        # Reload the data
        self.__create_future()

    async def write_file(self, new_data):
        return await get_running_loop().run_in_executor(
            executor,
            self.write_file_sync,
            new_data,
        )


class DirList(tuple):
    def __new__(cls, user_path, path_iter, /):
        instance = super().__new__(cls, chain((user_path,), path_iter))
        instance.user_dir = user_path
        return instance


RUNTIME_VAR = 'XDG_RUNTIME_DIR'
CACHE_VAR = 'XDG_CACHE_HOME'
DATA_VAR = 'XDG_DATA_HOME'
DATA_SEARCH = 'XDG_DATA_DIRS'
CONFIG_VAR = 'XDG_CONFIG_HOME'
CONFIG_SEARCH = 'XDG_CONFIG_DIRS'


default_eager_files = object()


class ProgramFiles:
    def __init__(
            self,
            name,
            *,
            file_cls=File,
            eager_files=default_eager_files,
    ):
        self.name = name
        self.__file_cls = file_cls
        self.__data_cache = {}

        self.__data_dirs = self.__get_paths(
            DATA_VAR,
            fallback=Path.home() / '.local/share',
            search_paths_var=DATA_SEARCH,
            search_fallback=(Path(' /usr/local/share/'), Path('/usr/share'))
        )

        self.__config_dirs = self.__get_paths(
            CONFIG_VAR,
            fallback=Path.home() / '.config',
            search_paths_var=CONFIG_SEARCH,
            search_fallback=(Path('/etc/xdg'), ),
        )

        runtime_dir_set = RUNTIME_VAR in environ
        if runtime_dir_set and Path(environ[RUNTIME_VAR]).is_absolute():
            self.__runtime_dir = Path(environ[RUNTIME_VAR])
        else:
            self.__runtime_dir = None

        self.__runtime_cache = {}

        if CACHE_VAR in environ and Path(environ[CACHE_VAR]).is_absolute():
            self.__cache_dir = Path(environ[CACHE_VAR])
        else:
            self.__cache_dir = Path.home()/'.cache'/self.name

        self.__cache_cache = {}

        if eager_files:
            if eager_files is default_eager_files:
                eager_files = {
                    'config': (name, )
                }

            for type, files in eager_files.items():
                for file in files:
                    self.get(type, file)

    def __get_paths(
        self,
        env_var,
        *,
        fallback,
        search_paths_var,
        search_fallback,
    ):
        user_path = fallback
        if env_var in environ:
            path = Path(environ[env_var])
            if path.is_absolute():
                user_path = path

        paths = search_fallback
        if search_paths_var in environ and environ[search_paths_var]:
            env_str = environ[search_paths_var]
            str_paths = env_str.split(':')
            search_paths = tuple(
                Path(path)
                for path in str_paths
                if Path(path).is_absolute()
            )

            if search_paths:
                paths = search_paths

        if user_path in paths:
            index = paths.index(user_path)
            start = paths[:index]
            end = paths[index + 1:]
            paths = start + end

        return DirList(
            user_path / self.name,
            unique_everseen(
                path / self.name
                for path in paths
            )
        )

    def get_config_file(self, name):
        file = File(
            f'{name}.yaml',
            self.__config_dirs.user_dir,
            self.__config_dirs,
        )

        self.__data_cache[name] = file
        return file

    def get_data_file(self, name):
        file = File(
            f'{name}.yaml',
            self.__data_dirs.user_dir,
            self.__data_dirs,
        )

        self.__data_cache[name] = file
        return file

    def get_runtime_file(self, name):
        file = File(
            f'{name}.yaml',
            self.__runtime_dir,
            (self.__runtime_dir, ),
        )

        self.__runtime_cache[name] = file
        return file

    def get_cache_file(self, name):
        file = File(
            f'{name}.yaml',
            self.__cache_dir,
            (self.__cache_dir, ),
        )

        self.__cache_cache[name] = file
        return file

    def get(self, type, name):
        if type == 'cache':
            return self.get_cache_file(name)
        elif type == 'config':
            return self.get_config_file(name)
        elif type == 'runtime':
            return self.get_runtime_file(name)
        elif type == 'data':
            return self.get_data_file(name)
