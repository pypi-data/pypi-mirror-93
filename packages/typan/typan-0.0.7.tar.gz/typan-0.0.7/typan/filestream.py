import codecs

class Filestream:
    def __init__(self,path):
        self.path = path

    def read(self):
        return codecs.open(self.path,"r",encoding="utf-8")

    def read_binary(self):
        return codecs.open(self.path,"rb",encoding="utf-8")

    def read_and_write(self):
        return codecs.open(self.path,"r+",encoding="utf-8")

    def write(self):
        return codecs.open(self.path,"w",encoding="utf-8")

    def write_binary(self):
        return codecs.open(self.path,"wb",encoding="utf-8")

    def write_and_read_binary(self):
        return codecs.open(self.path,"wb+",encoding="utf-8")

    def append(self):
        return codecs.open(self.path,"a",encoding="utf-8")

    def append_binary(self):
        return codecs.open(self.path,"ab",encoding="utf-8")

    def append_and_read(self):
        return codecs.open(self.path,"a+",encoding="utf-8")

    def append_and_read_binary(self):
        return codecs.open(self.path,"ab+",encoding="utf-8")