import os

from Services.UtilsService import Utils
from Services.EldenRing.EldenRingService import EldenRing
from Services.LiesOfP.LiesOfPService import LiesOfP
from Services.Palworld.PalworldService import Palworld
from Services.Sekiro.SekiroService import Sekiro
from Services.AWayOut.AWayOutService import AWayOut
from Services.ItTakesTwo.ItTakesTwoService import ItTakesTwo
from Services.GameDownloaderService import GameDownloader

class GameSwitcher():
    def __init__(self, GameName:str, jsonDict:dict):
        self.Game = GameName
        self.gamePath = jsonDict['GamePath']
        self.fixPath = jsonDict['FixPath']
        self.modEnginePath = jsonDict['EnginePath']
        self.mods = jsonDict['ModsPath']
        self.PirateArchives = self.SetGamePirateArchives()
        self.GameService = self.SetGameFunctions()
        self.GamesAvailableChangeTextLanguage = ['ELDEN RING', 'Enshrouded', 'Sekiro: Shadows Die Twice', 'A Way Out']
        self.GamesAvailableModsMenu = ['ELDEN RING']


    def SetGameFunctions(self):
        match self.Game:
            case 'ELDEN RING':
                return EldenRing(self.gamePath, self.fixPath, self.modEnginePath, self.mods, self.PirateArchives)
            case 'Lies of P':
                return LiesOfP(self.gamePath, self.fixPath, self.modEnginePath, self.mods, self.PirateArchives)
            case 'Palworld':
                return Palworld(self.gamePath, self.fixPath, self.modEnginePath, self.mods, self.PirateArchives)
            case 'Sekiro: Shadows Die Twice':
                return Sekiro(self.gamePath, self.fixPath, self.modEnginePath, self.mods, self.PirateArchives)
            case 'A Way Out':
                return AWayOut(self.gamePath, self.fixPath, self.modEnginePath, self.mods, self.PirateArchives)
            case 'It Takes Two':
                return ItTakesTwo(self.gamePath, self.fixPath, self.modEnginePath, self.mods, self.PirateArchives)
            case _:
                print(f'Atenção! função SetGameFunctions não tem implementação para o jogo escolhido. Game: {self.Game}')
    def SetGamePirateArchives(self):
        match self.Game:
            case 'ELDEN RING':
                return {
                    "Files": ['OnlineFix64.dll', 'OnlineFix.url', 'OnlineFix.ini',
                              'winmm.dll', 'dlllist.txt'],
                    "Folders": []
                }
            case 'Enshrouded':
                return {
                    "Files": ['OnlineFix.url', 'OnlineFix.ini', 'OnlineFix64.dll',
                              'winmm.dll', 'dlllist.txt', 'StubDRM64.dll'],
                    "Folders": []
                }
            case 'Palworld':
                return {
                    "Files": ['Palworld_backup.exe'],
                    "Folders": ['Engine_backup', 'Pal_backup']
                }
            case 'Lies of P':
                return {
                    "Files": [],
                    "Folders": ['Engine_backup']
                }
            case 'A Way Out':
                return {
                    "Files": [],
                    "Folders": ['Haze1_backup']
                }
            case 'It Takes Two':
                return {
                    "Files": [],
                    "Folders": ['Nuts_backup']
                }
            case 'Sekiro: Shadows Die Twice':
                return {
                    "Files": ['cream_api.ini', 'dinput8.dll', 'sekiro_backup.exe',
                              'steam_api64.org', 'SekiroOnlineFont.ttf', 'steam_api64_backup.dll'],
                    "Folders": []
                }
            case _:
                return {
                    "Files": [],
                    "Folders": []
                }

    def CallGameDownloader(self):
        match self.Game:
            case 'ELDEN RING':
                return GameDownloader().EldenRingDownloadOrUpdate(self.gamePath)
            case 'Spacewar':
                return GameDownloader().SpaceWarDownloadOrUpdate(self.gamePath)
            case 'Palworld':
                return GameDownloader().PalworldDownloadOrUpdate(self.gamePath)
            case 'Enshrouded':
                return GameDownloader().EnshroudedDownloadOrUpdate(self.gamePath)
            case 'Lies of P':
                return GameDownloader().LiesOfPDownloadOrUpdate(self.gamePath)
            case 'Sekiro: Shadows Die Twice':
                return GameDownloader().SekiroDownloadOrUpdate(self.gamePath)
            case 'A Way Out':
                return GameDownloader().AWayOutDownloadOrUpdate(self.gamePath)
            case 'It Takes Two':
                return GameDownloader().ItTakesTwoDownloadOrUpdate(self.gamePath)
            case _:
                print(f'Atenção! função CallGameDownloader não tem implementação para o jogo escolhido. Game: {self.Game}')
    def CheckIfPirateGameIsEnabled(self):
        for root, dirs, files in os.walk(self.gamePath):
            for fileName in files:
                if any(str(fileName).lower() == str(file).lower() for file in self.PirateArchives['Files']):
                    return True
            for dirName in dirs:
                if any(str(dirName).lower() == Dir.lower() for Dir in self.PirateArchives['Folders']):
                    return True
        return False

    def Menu(self):
        while True:
            try:
                Utils().clear_console()
                print(f"[ {self.Game.upper()} MENU ]")
                print("Choose an option:")
                print(f"[1] -> {'DISABLE' if self.CheckIfPirateGameIsEnabled() else 'ENABLE'} Pirate Game")
                print("[2] -> Change TEXT|SUBTITLE PIRATE game LANGUAGE")
                print("[3] -> Mods Menu")
                print(f"[4] -> Download-Install|Update {self.Game.upper()}")
                print("[0] -> Back to MASTER MENU")
                option = input("Choose an option(Left Number): ")
                match option:
                    case '1':
                        Utils().clear_console()
                        if self.CheckIfPirateGameIsEnabled():
                            self.GameService.DisablePirateGame()
                        else:
                            self.GameService.EnablePirateGame()
                    case '2':
                        Utils().clear_console()
                        if self.Game not in self.GamesAvailableChangeTextLanguage:
                            print('GAME IS NOT AVAILABLE TO CHANGE TEXT/SUBTITLE LANGUAGE')
                            continue
                        self.GameService.ChangeLanguage()
                    case '3':
                        Utils().clear_console()
                        if self.Game not in self.GamesAvailableModsMenu:
                            print('MODS MENU NOT AVAILABLE FOR THIS GAME')
                            continue
                        self.GameService.Mods.menu()
                    case '4':
                        Utils().clear_console()
                        GamePath = self.CallGameDownloader()
                        if GamePath != None:
                            self.gamePath = GamePath
                            Utils().updateJsonConfig(f'{self.Game}', f'GamePath', self.gamePath)
                            print(f'Download and Install {self.Game} completed! Path: {self.gamePath}')
                        else:
                            print(f'Failed to download {self.Game}')

                    case '0':
                        Utils().clear_console()
                        print(f"Quitting {self.Game} MENU...")
                        return
                    case _:
                        Utils().clear_console()
                        print("Invalid Option, or not implemented yet. Try again after next update.")
            except Exception as e:
                Utils().clear_console()
                print("Error:", e)
                continue
