from unittest import TestCase

from src.py.file_manager import FileManager, LocalFileSystem, File


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

    def test_file(self):
        fs = LocalFileSystem()
        f = [File(fs, 'a.mp3'), File(fs, 'a.flac')]
        f[0].priority = 1
        f[1].priority = 2
        f = sorted(f)
        print(f)

    def test_file_manager(self):
        fs = LocalFileSystem()
        fm = FileManager(fs)
        fm.add_path("/home/wii/Downloads/")
        # print(fm.get_music_list())
        r = fm.music_file_manager.get_deduplicate()
        print(r)
        r = fm.music_file_manager.get_deletable()
        print(r)
        for i in r:
            print(r)
            i.delete()

    def test_copy(self):
        fs = LocalFileSystem()
        fm = FileManager(fs)
        fm.add_path("/home/wii/Downloads/")
        r = fm.music_file_manager.get_deduplicate()
        for i in r:
            print(i)
            fs.copy(i.path, i.path + '.back')
