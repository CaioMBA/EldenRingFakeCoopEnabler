from Services.UtilsService import Utils
from Services.Games.GameDownloaderService import GameDownloader
import os, time, subprocess

class SpaceWar():
    def __init__(self):
        while True:
            if Utils().CheckIfAppIsRunning('steam.exe'):
                time.sleep(1)
                break
            os.system('start steam://open/steam')
            time.sleep(2)

    def InstallSpaceWar(self):
        print('DOWNLOADING|INSTALLING SPACE WAR SO PIRATE GAMES WORK!')
        print('SETUP CONTROLLER TEMPLATE ON SPACE WAR FOR THE GAME YOU WANNA PLAY(INSIDE STEAM)!')
        return GameDownloader().SpaceWarDownloadOrUpdate()

    def InstallSpaceWarBySteamInterface(self):
        print('KEEP YOUR PROGRESS, AND INSTALL SPACE WAR BY STEAM INTERFACE')
        print('SETUP CONTROLLER TEMPLATE ON SPACE WAR FOR THE GAME YOU WANNA PLAY(INSIDE STEAM)!')
        os.system('start steam://install/480')


    def Menu(self):
        while True:
            print('[ SPACEWAR MENU ]')
            print('[1] -> Install Spacewar by Steam Interface')
            print('[2] -> Install Spacewar by this program')
            print('[0] -> Back to MASTER MENU')
            option = input('Choose an option(Left Number): ')
            match option:
                case '1':
                    Utils().clear_console()
                    self.InstallSpaceWarBySteamInterface()
                case '2':
                    Utils().clear_console()
                    self.InstallSpaceWar()
                case '0':
                    Utils().clear_console()
                    print('Back to MASTER MENU...')
                    break
                case _:
                    print('Invalid Option, or not implemented yet. Try again after next update.')