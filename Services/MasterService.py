import time
from Services.GameSwitcherService import GameSwitcher
from Services.SpaceWarService import SpaceWar
from Services.UtilsService import Utils
from Services.GameDownloaderService import GameDownloader
class Master():
    def __init__(self, jsonDict: dict):
        GameDownloader().DownloadLinks(jsonDict)
        self.jsonDict = Utils().ReadJsonConfig()
        self.jsonDict = Utils().FixJsonConfigValues(self.jsonDict)
        if jsonDict['Spacewar']['GamePath'] == '' or jsonDict['Spacewar']['GamePath'] is None:
            path = SpaceWar().InstallSpaceWar()
            Utils().updateJsonConfig(key='Spacewar', subkey='GamePath', value=path)
    def menu(self):
        try:
            while True:
                print('[ MASTER MENU ]')
                print('Choose a game to manage:')
                print('[1] -> ELDEN RING')
                print('[2] -> Palworld')
                print('[3] -> Enshrouded')
                print('[4] -> Lies of P')
                print('[5] -> Spacewar (DOWNLOAD/UPDATE ONLY)')
                print('[0] -> Quit | Exit')
                option = input('Choose an option(Left Number): ')
                match option:
                    case '1':
                        Utils().clear_console()
                        GameSwitcher('ELDEN RING', self.jsonDict['ELDEN RING']).Menu()
                    case '2':
                        Utils().clear_console()
                        GameSwitcher('Palworld', self.jsonDict['Palworld']).Menu()
                    case '4':
                        Utils().clear_console()
                        GameSwitcher('Lies of P', self.jsonDict['Lies of P']).Menu()
                    case '5':
                        Utils().clear_console()
                        SpaceWar().Menu()
                        Utils().clear_console()
                    case '0':
                        Utils().clear_console()
                        print('Quitting MASTER MENU...')
                        break
                    case _:
                        Utils().clear_console()
                        print('Invalid Option, or not implemented yet. Try again after next update.')
        except Exception as e:
            Utils().clear_console()
            print("Error:", e)
            time.sleep(5)
            self.menu()
