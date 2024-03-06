import time
from Services.EldenRing.EldenRingService import EldenRing
from Services.SpaceWarService import SpaceWar
from Services.UtilsService import Utils
from Services.GameDownloaderService import GameDownloader
class Master():
    def __init__(self, jsonDict: dict):
        GameDownloader().DownloadLinks(jsonDict)
        self.jsonDict = Utils().ReadJsonConfig()
        if jsonDict['Spacewar']['GamePath'] == '' or jsonDict['Spacewar']['GamePath'] is None:
            path = SpaceWar().InstallSpaceWar()
            Utils().updateJsonConfig(key='Spacewar', subkey='GamePath', value=path)
    def menu(self):
        try:
            while True:
                print('[ MASTER MENU ]')
                print('[1] -> ELDEN RING')
                print('[0] -> Quit | Exit')
                option = input('Choose an option(Left Number): ')
                match option:
                    case '1':
                        Utils().clear_console()
                        EldenRing(self.jsonDict['ELDEN RING']).menu()
                    case '0':
                        Utils().clear_console()
                        print('Quitting MASTER MENU...')
                        break
                    case _:
                        Utils().clear_console()
                        print('Invalid Option')
                        self.menu()
        except Exception as e:
            Utils().clear_console()
            print("Error:", e)
            time.sleep(5)
            self.menu()
