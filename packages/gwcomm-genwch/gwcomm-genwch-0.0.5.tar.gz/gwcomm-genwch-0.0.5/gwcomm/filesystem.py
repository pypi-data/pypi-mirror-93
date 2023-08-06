class filesystem():
    def to_dict(self, fullpath):
        p, f = self.__file_split(fullpath=fullpath)
        n = self.fname(f)
        e = self.fext(f)
        return {"full": fullpath, "path": p, "file": f, "name": n, "ext": e}

    def fname(self, fullpath):
        _, rtn = self.__file_split(fullpath=fullpath)
        return rtn.split(".")[0]

    def fext(self, fullpath):
        _, rtn = self.__file_split(fullpath=fullpath)
        rtn = rtn.split(".")
        return "" if len(rtn) == 1 else rtn[-1]

    def file(self, fullpath):
        _, rtn = self.__file_split(fullpath=fullpath)
        return rtn

    def fpath(self, fullpath):
        rtn, _ = self.__file_split(fullpath=fullpath)
        return rtn

    def __file_split(self, fullpath):
        import os
        return os.path.split(fullpath)

    def ls(self, folder):
        import glob
        return glob.glob(folder)

    def ls_dict(self, folder):
        return [self.to_dict(r) for r in self.ls(folder=folder)]
