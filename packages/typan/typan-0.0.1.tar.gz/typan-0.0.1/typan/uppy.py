import urllib.request

class Uppy:
    def __init__(self,url,current):
        self.url = url
        self.current = current
        
        file = urllib.request.urlopen(self.url)

        lines = ""
        for line in file:
            lines += line.decode("utf-8")

        self.latest = lines.rstrip()

    def download_link(self,link):
        self.download_url = link

    def check(self):
        return self.current == self.latest

    def download(self,path):
        urllib.request.urlretrieve(self.download_url,path)