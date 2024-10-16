#!/bin/python3
import abc
import os
from typing import List
import logging

# logging.basicConfig()
formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
LOG = logging.getLogger('BAY')
LOG.addHandler(ch)


class FileSystem(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def list(self, path: str):
        raise NotImplementedError()

    @abc.abstractmethod
    def delete_file(self, path: str):
        raise NotImplementedError()

    def delete_files(self, pts: List[str]):
        for pt in pts:
            self.delete_file(pt)

    @abc.abstractmethod
    def copy(self, source: str, destination: str):
        raise NotImplementedError()


class File:
    def __init__(self, file_system: FileSystem, path: str):
        self.path = path
        self.name = self.path.split('/')[-1]
        self.name_without_extension = self.name.split('.')[0]
        self.extension = self.path.split('.')[-1]
        self.file_system = file_system
        self.priority = -1
        self.deleted = False

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return '{} {}'.format(self.priority, self.name)

    def __lt__(self, other):
        return self.priority > other.priority

    def delete(self):
        self.file_system.delete_file(self.path)
        self.deleted = True
        LOG.warning("delete file. [file={}]".format(self))


class LocalFileSystem(FileSystem):
    def copy(self, source: str, destination: str):
        with open(source, 'rb') as src, open(destination, 'wb') as dst:
            dst.write(src.read())

    def list(self, path: str):
        return [os.path.join(path, i) for i in os.listdir(path)]

    def delete_file(self, path: str):
        return os.remove(path)


class FileSystemManager:
    def __init__(self):
        self.file_system_list = {}

    def add(self, name: str, fs: FileSystem):
        self.file_system_list[name] = fs

    def get(self, name: str):
        return self.file_system_list.get(name, None)

    def list(self):
        return self.file_system_list.keys()


class FileManager(metaclass=abc.ABCMeta):
    def __init__(self):
        self.files = []
        self.file_names = {}

    @abc.abstractmethod
    def is_fit(self, name: str):
        raise NotImplementedError()

    def add(self, file: File):
        self.files.append(file)
        if file.name_without_extension in self.file_names:
            self.file_names[file.name_without_extension].append(file)
        else:
            self.file_names[file.name_without_extension] = [file]

    @abc.abstractmethod
    def get_deduplicate(self):
        return []

    @abc.abstractmethod
    def get_deletable(self):
        return []


class NormalFileManager(FileManager):
    def __init__(self):
        super().__init__()

    def get_deduplicate(self):
        return super().get_deduplicate()

    def get_deletable(self):
        return super().get_deletable()

    def is_fit(self, name: str):
        return True


class MusicFileManager(FileManager):
    music_file_extensions = ["dts", "flac", "ape", "wma", "mp3"]

    def __init__(self):
        super().__init__()

    def add(self, file: File):
        super().add(file)
        file.priority = len(self.music_file_extensions) - self.music_file_extensions.index(file.extension)
        self.file_names[file.name_without_extension] = sorted(self.file_names[file.name_without_extension])

    def get_deduplicate(self):
        rst = []
        for k, v in self.file_names.items():
            rst.append(v[0])
        return rst

    def get_deletable(self):
        rst = []
        for k, v in self.file_names.items():
            rst += v[1:]
        return rst

    def is_fit(self, name: str):
        ext = name.split('.')[-1].lower()
        return ext in self.music_file_extensions


class FileManager:
    def __init__(self, file_system: FileSystem):
        self.file_system = file_system
        self.music_file_manager = MusicFileManager()
        self.file_manager_list = [self.music_file_manager]

    def add_path(self, path: str):
        file_list = self.file_system.list(path)
        for file in file_list:
            for m in self.file_manager_list:
                if m.is_fit(file):
                    m.add(File(self.file_system, file))

    def get_music_list(self):
        return self.music_file_manager.files
