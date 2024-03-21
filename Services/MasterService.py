import time
from Services.Games.GameSwitcherService import GameSwitcher
from Services.Games.SpaceWarService import SpaceWar
from Services.UtilsService import Utils
from Services.Games.GameDownloaderService import GameDownloader
class Master():
    def __init__(self, jsonDict: dict):
        GameDownloader().DownloadLinks(jsonDict)
        self.jsonDict = jsonDict
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
                print('[3] -> Enshrouded [NOT FULLY IMPLEMENTED YET]')
                print('[4] -> Lies of P')
                print('[5] -> Sekiro: Shadows Die Twice')
                print('[6] -> A Way Out')
                print('[7] -> It Takes Two')
                print('[8] -> Sons of the Forest')
                print('[9] -> Lords of the Fallen')
                print('[10] -> Ready or Not')
                print('\t[0.1] -> Spacewar (DOWNLOAD/UPDATE ONLY)')
                print('[0] -> Quit | Exit')
                option = input('Choose an option(Left Number): ')
                match option:
                    case '1':
                        Utils().clear_console()
                        GameSwitcher('ELDEN RING', self.jsonDict['ELDEN RING']).Menu()
                    case '2':
                        Utils().clear_console()
                        GameSwitcher('Palworld', self.jsonDict['Palworld']).Menu()
                    case '3':
                        Utils().clear_console()
                        GameSwitcher('Enshrouded', self.jsonDict['Enshrouded']).Menu()
                        time.sleep(5)
                    case '4':
                        Utils().clear_console()
                        GameSwitcher('Lies of P', self.jsonDict['Lies of P']).Menu()
                    case '5':
                        Utils().clear_console()
                        GameSwitcher('Sekiro', self.jsonDict['Sekiro']).Menu()
                    case '6':
                        Utils().clear_console()
                        GameSwitcher('AWayOut', self.jsonDict['AWayOut']).Menu()
                    case '7':
                        Utils().clear_console()
                        GameSwitcher('ItTakesTwo', self.jsonDict['ItTakesTwo']).Menu()
                    case '8':
                        Utils().clear_console()
                        GameSwitcher('SonsOfTheForest', self.jsonDict['SonsOfTheForest']).Menu()
                    case '9':
                        Utils().clear_console()
                        GameSwitcher('LordsOfTheFallen', self.jsonDict['LordsOfTheFallen']).Menu()
                    case '10':
                        Utils().clear_console()
                        GameSwitcher('Ready Or Not', self.jsonDict['Ready Or Not']).Menu()
                    case '0.1':
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
