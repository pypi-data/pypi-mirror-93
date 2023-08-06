import unittest
import os
import shutil

from storer import Storer

PATH_DUMPS        = "./data/"
PATH_DUMPS_BACKUP = PATH_DUMPS + "backup/"
DUMP_NAME         = "test_case"
PKL               = ".pkl"
PBZ2              = ".pbz2"

class TestsStorer(unittest.TestCase):
    def test_creating_pkl(self):
        """
        Test paths of the created instance (PKL)
        """
        s = Storer(path_dumps=PATH_DUMPS, dump_name=DUMP_NAME, verbose=False, compressed=False)
        s.put(1, name="one")
        s.dump()
        assert os.path.exists(os.path.expanduser(PATH_DUMPS) + DUMP_NAME + PKL)
        s._cleanup()

    def test_creating_pbz2(self):
        """
        Test paths of the created instance (PBZ2)
        """
        s = Storer(path_dumps=PATH_DUMPS, dump_name=DUMP_NAME, verbose=False)
        s.put(1, name="one")
        s.dump()
        assert os.path.exists(os.path.expanduser(PATH_DUMPS) + DUMP_NAME + PBZ2)
        s._cleanup()
    
    def test_backup_dumb_pkl(self):
        """
        Test backup creating
        """
        s = Storer(path_dumps=PATH_DUMPS, dump_name=DUMP_NAME, verbose=False, compressed=False)
        s.put(1, name="one")
        s.backup()
        assert os.path.exists(os.path.expanduser(PATH_DUMPS_BACKUP) + DUMP_NAME + PKL)
        s._cleanup()
    
    def test_backup_dumb_pbz2(self):
        """
        Test backup creating
        """
        s = Storer(path_dumps=PATH_DUMPS, dump_name=DUMP_NAME, verbose=False,)
        s.put(1, name="one")
        s.backup()
        assert os.path.exists(os.path.expanduser(PATH_DUMPS_BACKUP) + DUMP_NAME + PBZ2)
        s._cleanup()
    
    def test_get_item_pkl(self):
        """
        Test get item procedure
        """
        s = Storer(path_dumps=PATH_DUMPS, dump_name=DUMP_NAME, verbose=False, compressed=False)
        s.put(1, name="one")
        s.put(2, name="two")
        three = s.get("three")
        assert three == False #  "Should be False!"
        s.put(3, name="three")
        s.dump()
        # here is new data in storer
        three = s.get("three")
        assert three == 3, f"got something different: [{three}]"  # "Should be 3!"
        s._cleanup()
    
    def test_get_item_bpz2(self):
        """
        Test get item procedure
        """
        s = Storer(path_dumps=PATH_DUMPS, dump_name=DUMP_NAME, verbose=False)
        s.put(1, name="one")
        s.put(2, name="two")
        three = s.get("three")
        assert three == False #  "Should be False!"
        s.put(3, name="three")
        s.dump()
        # here is new data in storer
        three = s.get("three")
        assert three == 3, f"got something different: [{three}]"  # "Should be 3!"
        s._cleanup()
    
    def test_initialization_pkl(self):
        """
        Test initialization procedure
        Expected one backup file after dump procedure
        """
        s = Storer(path_dumps=PATH_DUMPS, dump_name=DUMP_NAME, verbose=False, compressed=False)
        s.put(1, name="one")
        s.dump()
        s2 = Storer(path_dumps=PATH_DUMPS, dump_name=DUMP_NAME, verbose=False, compressed=False)
        one = len(s2.backup_list)
        assert one == 1
        s._cleanup()
    
    def test_initialization_pbz2(self):
        """
        Test initialization procedure
        Expected one backup file after dump procedure
        """
        s = Storer(path_dumps=PATH_DUMPS, dump_name=DUMP_NAME, verbose=False)
        s.put(1, name="one")
        s.dump()
        s2 = Storer(path_dumps=PATH_DUMPS, dump_name=DUMP_NAME, verbose=False)
        one = len(s2.backup_list)
        assert one == 1
        s._cleanup()

    def test_separation(self):
        """
        Test separation procedure
        """
        s = Storer(path_dumps=PATH_DUMPS, dump_name=DUMP_NAME, verbose=False, compressed=False, separations=1)
        s.put(1, name="one")    # _
        s.put(2, name="two")    # 0
        s.put(3, name="three")  # 1
        s.put(4, name="four")   # 2
        s.dump()                # 3
        s2 = Storer(path_dumps=PATH_DUMPS, dump_name=DUMP_NAME, verbose=False, compressed=False)
        assert len(s2.backup_list) == 5
        s._cleanup()
    
    def test_loading_separation(self):
        """
        Test separation procedure
        """
        s = Storer(path_dumps=PATH_DUMPS, dump_name=DUMP_NAME, verbose=False, compressed=False, separations=1)
        s.put(1, name="one")    # _
        s.put(2, name="two")    # 0
        s.put(3, name="three")  # 1
        s.put(4, name="four")   # 2
        s.dump()                # 3
        s2 = Storer(path_dumps=PATH_DUMPS, dump_name=DUMP_NAME, verbose=False, compressed=False)
        s2.load()
        one = s2.get(name="one")
        assert 1 == one, f"Got something different: {one}"
        two = s2.get(name="two")
        assert 2 == two, f"Got something different: {two}"
        three = s2.get(name="three")
        assert 3 == three, f"Got something different: {three}"
        four = s2.get(name="four")
        assert 4 == four, f"Got something different: {four}"
        s._cleanup()
    
    def test_loading_separation_pbz2(self):
        """
        Test separation procedure
        """
        s = Storer(path_dumps=PATH_DUMPS, dump_name=DUMP_NAME, verbose=False, compressed=True, separations=1)
        s.put(1, name="one")    # _
        s.put(2, name="two")    # 0
        s.put(3, name="three")  # 1
        s.put(4, name="four")   # 2
        s.dump()                # 3
        s2 = Storer(path_dumps=PATH_DUMPS, dump_name=DUMP_NAME, verbose=False, compressed=True)
        s2.load()
        one = s2.get(name="one")
        assert 1 == one, f"Got something different: {one}"
        two = s2.get(name="two")
        assert 2 == two, f"Got something different: {two}"
        three = s2.get(name="three")
        assert 3 == three, f"Got something different: {three}"
        four = s2.get(name="four")
        assert 4 == four, f"Got something different: {four}"
        s._cleanup()

if __name__ == "__main__":
    unittest.main()
