import time
from Services.Games.GameSwitcherService import GameSwitcher
from Services.Games.SpaceWarService import SpaceWar
from Services.UtilsService import Utils
from Services.Games.GameDownloaderService import GameDownloader
class Master():
    def __init__(self, jsonDict: dict):
        self.jsonDict = jsonDict
        self.jsonDict = Utils().FixJsonConfigValues(self.jsonDict)
        print('App Config Loaded...')
        Utils().clear_console()
        if jsonDict['Spacewar']['GamePath'] == '' or jsonDict['Spacewar']['GamePath'] is None:
            path = SpaceWar().InstallSpaceWar()
            Utils().updateJsonConfig(key='Spacewar', subkey='GamePath', value=path)
    def menu(self):
        DictMenu = {}
        MenuKeys = []
        for index, (key, value) in enumerate(self.jsonDict.items()):
            DictMenu[index + 1] = {
                "key": key,
                "value": value
            }

        try:
            while True:
                print('[ MASTER MENU ]')
                print('Choose a game to manage:')
                for key, value in DictMenu.items():
                    if value['key'] == 'Spacewar':
                        continue
                    valueToChoose = value['key']
                    if valueToChoose in ['Enshrouded', 'ItTakesTwo']:
                        valueToChoose += ' [NOT FULLY IMPLEMENTED YET]'
                    MenuKeys.append(str(key))
                    print(f'[{key}] -> {valueToChoose}')
                print('\t[0.1] -> Spacewar (DOWNLOAD/UPDATE ONLY)')
                print('[0] -> Quit | Exit')
                option = input('Choose an option(Left Number): ')
                if option in MenuKeys:
                    Utils().clear_console()
                    GameSwitcher(DictMenu[int(option)]['key'], self.jsonDict).Menu()
                elif option == '0.1':
                    Utils().clear_console()
                    SpaceWar().Menu()
                    Utils().clear_console()
                elif option == '0':
                    Utils().clear_console()
                    print('Quitting MASTER MENU...')
                    break
                else:
                    Utils().clear_console()
                    print('Invalid Option, or not implemented yet. Try again after next update.')

        except Exception as e:
            Utils().clear_console()
            print("Error:", e)
            time.sleep(5)
            self.menu()
