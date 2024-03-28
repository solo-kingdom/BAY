#!/bin/python3
import abc
import os


class FileSystem(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def list(self, path: str):
        raise NotImplementedError()


class File:
    def __init__(self, file_system: FileSystem, path: str):
        self.path = path
        self.name = self.path.split('/')[-1]
        self.name_without_extension = self.name.split('.')[0]
        self.extension = self.path.split('.')[-1]
        self.file_system = file_system
        self.priority = -1

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return '{} {}'.format(self.priority, self.name)


class LocalFileSystem(FileSystem):
    def list(self, path: str):
        return os.listdir(path)


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
    @abc.abstractmethod
    def is_fit(self, name: str):
        raise NotImplementedError()


class MusicFileManager(FileManager):
    music_file_extensions = ["dts", "flac", "ape", "wma", "mp3"]

    def __init__(self):
        self.files = []
        self.file_names = {}

    def add(self, file: File):
        file.priority = len(self.music_file_extensions) - self.music_file_extensions.index(file.extension)
        self.files.append(File)
        if file.name_without_extension in self.file_names:
            self.file_names[file.name_without_extension].append(file)
        else:
            self.file_names[file.name_without_extension] = [file]

    def get_deduplicate(self):
        rst = []
        for k, v in self.file_names.items():
            print(k, v)

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
