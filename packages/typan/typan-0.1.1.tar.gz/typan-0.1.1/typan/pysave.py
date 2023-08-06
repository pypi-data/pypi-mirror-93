from . import filestream

import json
import codecs

class PysaveSyntaxError(Exception):
    pass

class JSON:
    def __init__(self,path:str,*args,**kwargs):
        self.path = path
        self.file = filestream.Filestream(path)
        self.loaded = json.load(self.file.read())
        self.save_args = args
        self.save_kwargs = kwargs

    def save(self):
        self.file.write().write(json.dumps(self.loaded,*self.save_args,**self.save_kwargs))

class Save:
    def __init__(self,path:str):
        self.path = path
        self.file = filestream.Filestream(path)
        self.readed = self.file.read().read()
        self.loaded = self.pysave_to_dict()

    def pysave_to_dict(self):
        DIGITS = [
            "a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",
            "A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z",
            "1","2","3","4","5","6","7","8","9","0",
            "!","@","#","$","%","^","&","*","(",")",
            "`","~","-","_","+",
            "[","{","]","}","\\","|",
            ";",":","'","\"",
            "<",">",".","?","/", " "
        ]
        value = False
        word = ""

        setting_names = []
        setting_values = []

        for c in self.readed:
            if c in DIGITS:
                if c != " ":
                    word += c
                elif value and word != "":
                    word += c
            elif c in "\n\t":
                pass
            elif c == "=":
                if not value:
                    value = True
                    setting_names.append(word)
                    word = ""
                else:
                    raise PysaveSyntaxError("Invalid syntax '='")
            elif c == ",":
                if value:
                    value = False
                    setting_values.append(word)
                    word = ""
                else:
                    raise PysaveSyntaxError("Invalid syntax ';'")
            else:
                raise PysaveSyntaxError("Invalid syntax '" + c + "'")

        return dict(zip(setting_names,setting_values))

    def dict_to_pysave(self):
        dicto = self.loaded
        content = ""

        for key in dicto:
            content += key + "=" + dicto[key] + ","
        
        return content

    def save(self):
        self.file.write().write(self.dict_to_pysave())