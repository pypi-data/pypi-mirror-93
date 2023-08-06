from pathlib import Path

from .ZJPG import ZJPG

class ZIMG():

    @staticmethod
    def load(filepath, loader_func=None):
        if filepath.suffix == '.jpg':
            return ZJPG.load ( str(filepath), loader_func=loader_func )
        else:
            return None
