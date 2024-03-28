from unittest import TestCase

from src.py.file_manager import FileManager, LocalFileSystem


class TestFileManager(TestCase):
    def test_basic(self):
        d = {'b': []}
        lst = d.get('a', [])
        lst.append('a')
        print(lst)
        print(d.get('b', []))
        r = d.get('b', [])
        r.append('3')
        r.append('2')
        print(d)
        r = d.get('c', [])
        r.append('3')
        r.append('2')

    def test_file_manager(self):
        fs = LocalFileSystem()
        fm = FileManager(fs)
        fm.add_path("/Users/wii/Downloads/")
        print(fm.get_music_list())
        fm.music_file_manager.get_deduplicate()
