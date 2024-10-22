import os
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
            fs.copy(i, i.path + '.back')

    def test_filter_musics(self):
        fs = LocalFileSystem()
        fm = FileManager(fs)
        fm.add_path("/Volumes/ssd/音乐/国语")
        rm = fm.music_file_manager.get_deletable()
        fs.move_with_confirm(rm, '/Volumes/ssd/音乐/备份/')

    def test_filter_and_delete(self):
        fs = LocalFileSystem()
        fm = FileManager(fs)
        fm.add_path("/Volumes/ssd/音乐")
        rm = fm.music_file_manager.get_deletable()
        fs.delete_with_confirm(rm)

    def test_delete(self):
        # r = os.listdir("/Volumes/ssd/音乐/欧美/Hélène Rollès - Je m'appelle Hélène.mp3")
        # print(r)
        pt = "/Volumes/ssd/音乐/欧美/Hélène Rollès - Je m'appelle Hélène.mp3"
        npt = os.path.normpath(pt)
        print(os.path.normpath(pt))
        print(os.path.exists(pt))
        print(os.path.exists(npt))
        os.remove(os.path.normpath(pt))


