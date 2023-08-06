from dataclasses import dataclass
import os
from pathlib import Path
from enum import Enum
import typing

import pickle
import bz2
import lzma
import gzip
import io


class Algorithm(Enum):
    gzip = "gzip"
    bz2  = "bz2"
    lzma = "lzma"
    lz4   = ""

_file_algorithm_mapper = {
    Algorithm.gzip: [gzip.GzipFile, ".pgz"],
    Algorithm.bz2:  [bz2.BZ2File,   ".pbz2"],
    Algorithm.lzma: [lzma.LZMAFile, ".xz"],
}

@dataclass
class Compressor:
    __version__ = "0.0.1 [1]"
    compressed: bool = True
    algorithm: Algorithm = Algorithm.bz2

    def _use(self:object, algorithm: Algorithm) -> None:
        self.algorithm = algorithm 

    def dump(self:object, path_dumps:Path, dump_name:str, data:dict) -> None:
        if not self.compressed: 
            with open(path_dumps / (dump_name + ".pkl"), 'wb') as f: pickle.dump(data, f)
        else:
            with _file_algorithm_mapper[self.algorithm][0](
                filename = path_dumps / (dump_name + _file_algorithm_mapper[self.algorithm][1]), 
                mode     = "wb") as f: 
                pickle.dump(data, f)


    def load(self:object, path_dumps:Path, dump_name:str) -> dict:
        if not self.compressed:
            if os.path.exists(path_dumps / (dump_name + ".pkl") ):
                with open(path_dumps / (dump_name + ".pkl"), 'rb') as f: data = pickle.load(f)
            else:
                data=dict()
        else:
            if os.path.exists(path_dumps / (dump_name + _file_algorithm_mapper[self.algorithm][1]) ):
                with open(path_dumps / (dump_name + _file_algorithm_mapper[self.algorithm][1]), 'rb') as f:
                    data = _file_algorithm_mapper[self.algorithm][0](filename=f, mode='rb')
                    data = pickle.load(data)
            else:
                data=dict()
        return data