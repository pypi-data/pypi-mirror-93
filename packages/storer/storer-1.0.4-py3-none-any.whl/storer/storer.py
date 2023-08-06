from dataclasses import dataclass, field
from pathlib import Path
import os
import shutil
from typing import Any
from storer.compressor import compressor

@dataclass
class Storer:
    __version__ = "1.0.4 [48]"
    internal_name:  str  = "[Storer]"
    dump_name:      str  = "noname"
    path_dumps:     str  = Path(os.path.expanduser(os.path.dirname(__file__)))
    verbose:        bool = False
    data:           dict = field(default_factory=dict)
    default_dir:    str  = "data"
    compressed:     bool = True
    separations:    int  = int(1e6)
    _backup_dir:    str  = "backup"
    _backup_list:   list = field(default_factory=list)
    _put_counter:   int  = 0
    _dump_counter:  int  = 0
    _dump_name:     str  = None
    _extension:     str  = None

    def __post_init__(self):
        if self.verbose: print(f"[Storer v.{Storer.__version__ }] is initialized!")
        self._dump_name = self.dump_name
        if self.path_dumps == Path(os.path.expanduser(os.path.dirname(__file__))) or self.path_dumps == "." :
            self.path_dumps = Path(os.path.expanduser(os.path.dirname(__file__))) / "data"
        else: 
            self.path_dumps = Path(os.path.expanduser(self.path_dumps))

        if self.verbose: print(f"Dump folder: [{self.path_dumps}]")
        os.makedirs(self.path_dumps, exist_ok=True)
        self._extension = ".pbz2" if self.compressed else ".pkl"
        self.initialization()  # creating _backup_list
        self.compressor = compressor.Compressor(compressed=self.compressed)
    
    def _get_priv_dump_name(self) -> None:
        self.dump_name      = self._dump_name + "_" + str(self._dump_counter)
        self._dump_counter -= 1
        if self._dump_counter < 0: self._dump_counter = 0
    
    def _get_next_dump_name(self) -> None:
        self.dump_name      = self._dump_name + "_" + str(self._dump_counter)
        self._dump_counter += 1
    
    def initialization(self:object) -> None:
        """ Splitting project """
        self._backup_list = [p for p in self.path_dumps.iterdir() if p.is_file()]
        self.backup_list = []
        if self.verbose: print("[backups] Found: ")
        for path_fname in self._backup_list:
            fname = str(path_fname.name).split(self._extension)[0]
            if self.verbose: print("--> ", path_fname)
            self.backup_list.append(fname)
        if len(self.backup_list) == 0: self.backup_list.append(self.dump_name)

    def put(self, what=None, name: str = None) -> None:
        self.data[name]   = what
        self._put_counter+=1
        if self._put_counter >= self.separations: 
            self.dump()
            self._get_next_dump_name()
            self._put_counter   = 0

    def get(self, name: str = None) -> Any :
        """
        Get an item from dump[s]
        """
        if name in self.data: return self.data[name]
        for dump_name in self.backup_list:
            data = self._load(dump_name=str(dump_name))
            if name in data: return data[name]
        return False

    def dump(self:object, backup:bool = False) -> None:
        if backup: path_dumps = self.path_dumps / self._backup_dir
        else:      path_dumps = self.path_dumps
                    
        if self.verbose: print(self.internal_name, self.path_dumps, self.dump_name, "dumping...")
        self.compressor.dump(path_dumps=path_dumps, dump_name=self.dump_name, data=self.data)
        if backup: self.data = dict()

    def _load(self:object, dump_name:str = None) -> dict:
        if not dump_name: dump_name = self.dump_name
        data = self.compressor.load(path_dumps=self.path_dumps, dump_name=dump_name)
        return data
    
    def load(self:object, dump_name:str = None) -> None:
        
        if not dump_name: 
            dump_name = self.dump_name
            if self.verbose: print(self.internal_name, self.path_dumps,  "loading...")
        
        self.data = self.compressor.load(path_dumps=self.path_dumps, dump_name=dump_name)

    def show(self, get_string = False) -> Any:
        string = ""
        for name in self.data:
            string += "key: {0:10} | value:  {1:4}; ".format(name, str(self.data[name]))
        if get_string: return string
        else: print(string)
    
    def backup(self:object) -> None:
        """
        Backuping the current dump_name in separate folder [<path_dumps> / backup ]
        """
        if self.verbose: print(f"Backup...")
        os.makedirs(self.path_dumps / self._backup_dir, exist_ok=True)
        self.dump(backup=True)

    def _cleanup(self:object) -> None:
        """
        Cleanup the path_dumps directory fully: including all folders and files. 
        Assuming the folder is used only for Storer purposes.
        """
        if self.verbose: print(f"Cleaning...[{self.path_dumps}]")
        shutil.rmtree(self.path_dumps)
        

if __name__ == "__main__":
    s = Storer(path_dumps=".")
    s.put(what="string", name="my_string")
    s.put(what=1, name="my_int")
    s.put(what=[i for i in range(10)],     name="my_range")
    s.put(what={v:v*2 for v in range(10)}, name="my_dict")
    s.show()
    s.dump()

    print("\n Now we creating new storer instance...\n")
    s1 = Storer(path_dumps=".", verbose=False)
    s1.load()
    s1.show()

