from Services.UtilsService import Utils
from Data.SteamData import Steam
from Services.GameDownloaderService import GameDownloader
import os, time

class SpaceWar():
    def __init__(self):
        while True:
            if Utils().CheckIfAppIsRunning('steam.exe'):
                time.sleep(1)
                break
            os.system('start steam://open/steam')
            time.sleep(2)

    def InstallSpaceWar(self):
        print('DOWNLOADING|INSTALLING SPACE WAR SO ELDEN RING WORKS!')
        print('SETUP CONTROLLER TEMPLATE ON SPACE WAR FOR ELDEN RING(INSIDE STEAM)!')
        return GameDownloader().SpaceWarDownloadOrUpdate()
