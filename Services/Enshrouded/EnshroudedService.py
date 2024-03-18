import os, shutil, configparser
from Services.UtilsService import Utils
from Services.GameDownloaderService import GameDownloader

class Enshrouded():
    def __init__(self, GamePath, fixPath, EnginePath, ModsPath, pirateArchives:dict):
        if GamePath == '' or GamePath is None:
            path = GameDownloader().EnshroudedDownloadOrUpdate()
            Utils().updateJsonConfig('Enshrouded', 'GamePath', path)
            print('FOR THE GAME TO WORK, YOU NEED TO RESTART THIS PROGRAM')
            return

        self.GamePath = GamePath
        self.FixPath = fixPath
        self.ModEnginePath = EnginePath
        #self.Mods = Mods(ModsPath, self.ModEnginePath, self.GamePath)
        self.PirateArchives = pirateArchives

