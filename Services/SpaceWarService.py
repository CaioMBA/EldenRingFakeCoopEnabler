from Services.UtilsService import Utils
from Data.SteamData import Steam
from Services.GameDownloaderService import GameDownloader
import os, time

class SpaceWar():
    def __init__(self):
        if not Utils().CheckIfAppIsRunning('steam.exe'):
            os.system('start steam://open/steam')

    def InstallSpaceWar(self):
        while True:
            if Utils().CheckIfAppIsRunning('steam.exe'):
                print('Steam aberta! com sucesso')
                break
        print('DOWNLOADING|INSTALLING SPACE WAR SO ELDEN RING WORKS!')
        print('SETUP CONTROLLER TEMPLATE ON SPACE WAR FOR ELDEN RING(INSIDE STEAM)!')
        time.sleep(2)
        return GameDownloader().SpaceWarDownloadOrUpdate()
