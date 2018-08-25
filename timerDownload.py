import schedule
import time
from qbittorrent import Client
import os

class QBitTorrentWrapper(object):
    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password

        self.qb = Client(ip)
        self.qb.login(self.username, self.password)

    def addTorrentsFromFolder(self, dl_location_path):
        self.dl_location_path = dl_location_path

        for filename in filter(os.path.isfile, os.listdir(os.curdir)):
            if filename.endswith(".torrent"):
                torrent_file=open('%s' % filename, 'rb')
                self.qb.download_from_file(torrent_file, savepath=dl_location_path)
    
    def startDownloading(self):
        self.qb.resume_all()
    
    def stopDownloading(self):
        self.qb.pause_all()

    def timeInterval(self):
        schedule.every().day.at("00:00").do(self.startDownloading)
        schedule.every().day.at("06:00").do(self.stopDownloading)

        while True:
            schedule.run_pending()

def main():
    client = QBitTorrentWrapper('http://127.0.0.1:8080/', 'username', 'password')

if __name__ == "__main__":
    main()