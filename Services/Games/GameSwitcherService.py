import os, shutil, configparser
from Services.UtilsService import Utils
from Services.Configs.AppConfigService import AppConfigService
from Services.Games.GameDownloaderService import GameDownloader
from Services.Mods.ModSwitcherService import ModSwitcher

class GameSwitcher():
    def __init__(self, GameName:str, fullJsonDict:dict):
        print(f'Loading GameSwitcher for {GameName}...')
        GameDownloader().DownloadLinks(fullJsonDict, GameName)
        fullJsonDict = AppConfigService().ReadAppConfig()
        jsonDict = fullJsonDict[GameName]
        self.Game = GameName
        self.GamePath = jsonDict['GamePath']
        self.FixPath = jsonDict['FixPath']
        self.ModEnginePath = jsonDict['EnginePath']
        self.ModsPath = jsonDict['ModsPath']

        if self.GamePath == '' or self.GamePath is None:
            path = GameDownloader().DownloadGame(GameName, jsonDict['GamePath'])
            AppConfigService().UpdateAppConfig(GameName, 'GamePath', path)
            print(f'FOR {GameName} TO WORK, YOU NEED TO RESTART THIS PROGRAM')
            self.GamePath = path

        self.ModsService = ModSwitcher(self.Game, self.ModsPath, self.ModEnginePath, self.GamePath)
        self.PirateArchives = self.SetGamePirateArchives()
        self.BackUpFile = self.SetGameBackUpFiles()
        self.LanguagesAvailable = self.SetAvailableLanguages()
        self.LanguageFileConfig = self.SetLanguageFileConfig()
        self.GamesAvailableChangeTextLanguage = ['ELDEN RING', 'Enshrouded',
                                                 'Sekiro', 'AWayOut',
                                                 'Ready Or Not']
        Utils().clear_console()

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
            case 'AWayOut':
                return {
                    "Files": [],
                    "Folders": ['Haze1_backup']
                }
            case 'ItTakesTwo':
                return {
                    "Files": [],
                    "Folders": ['Nuts_backup']
                }
            case 'Sekiro':
                return {
                    "Files": ['cream_api.ini', 'dinput8.dll', 'sekiro_backup.exe',
                              'steam_api64.org', 'SekiroOnlineFont.ttf', 'steam_api64_backup.dll'],
                    "Folders": []
                }
            case 'Sons Of The Forest':
                return {
                    "Files": ['dlllist.txt', 'OnlineFix.ini', 'OnlineFix.url',
                              'OnlineFix64.dll', 'SteamOverlay64.dll', 'winmm.dll'],
                    "Folders": ['SonsOfTheForest_Data_backup']
                }
            case 'Lords of the Fallen':
                return {
                    "Files": ['LOTF2_backup.exe', 'LOTF2.of', 'launch_data.of'],
                    "Folders": ['Engine_backup', 'LOTF2_backup']
                }
            case 'Ready Or Not':
                return {
                    "Files": [],
                    "Folders": ['ReadyOrNot_backup', 'Engine_backup']
                }
            case 'Baldurs Gate 3':
                return {
                    "Files": [],
                    "Folders": ['bin_backup', 'Launcher_backup']
                }
            case 'Sea of Thieves':
                return {
                    "Files": ['GDK_Helper.bat'],
                    "Folders": ['Athena_backup']
                }
            case _:
                return {
                    "Files": [],
                    "Folders": []
                }
    def SetGameBackUpFiles(self):
        match self.Game:
            case 'AWayOut':
                return {
                    "Files": [],
                    "Folders": ['Haze1']
                }
            case 'ItTakesTwo':
                return {
                    "Files": [],
                    "Folders": ['Nuts']
                }
            case 'Lies of P':
                return {
                    "Files": [],
                    "Folders": ['Engine']
                }
            case 'Lords of the Fallen':
                return {
                    "Files": [],
                    "Folders": ['LOTF2', 'Engine']
                }
            case 'Palworld':
                return {
                    "Files": ['Palworld.exe'],
                    "Folders": ['Engine', 'Pal']
                }
            case 'Sekiro':
                return {
                    "Files": ['steam_api64.dll', 'sekiro.exe'],
                    "Folders": []
                }
            case 'Sons Of The Forest':
                return {
                    "Files": [],
                    "Folders": ['SonsOfTheForest_Data']
                }
            case 'Ready Or Not':
                return {
                    "Files": [],
                    "Folders": ['ReadyOrNot', 'Engine']
                }
            case 'Baldurs Gate 3':
                return {
                    "Files": [],
                    "Folders": ['bin', 'Launcher']
                }
            case 'Sea of Thieves':
                return{
                    "Files": [],
                    "Folders": ['Athena']
                }

    def SetAvailableLanguages(self):
        if self.Game in ['ELDEN RING', 'Enshrouded', 'Sekiro', 'Ready Or Not', 'Baldurs Gate 3']:
            return ['english', 'brazilian', 'french', 'german', 'hungarian', 'italian',
                    'japanese', 'koreana', 'latam', 'polish', 'russian', 'schinese',
                    'spanish', 'tchinese', 'thai']
        elif self.Game in ['AWayOut']:
            return ['en_US', 'pt_BR', 'ru_RU']
        else:
            return []
    def SetLanguageFileConfig(self):
        if self.Game in ['ELDEN RING', 'Enshrouded']:
            return {
                'Path': os.path.join(self.GamePath, 'OnlineFix.ini'),
                'ConfigSection': ['Main', 'Language'],
            }
        elif self.Game in ['Sekiro']:
            return {
                'Path': os.path.join(self.GamePath, 'cream_api.ini'),
                'ConfigSection': ['Language', 'Language'],
            }
        elif self.Game in ['AWayOut']:
            return {
                'Path': os.path.join(self.GamePath, 'Haze1', 'Binaries', 'Win64', 'CPY.ini'),
                'ConfigSection': ['Settings', 'Language'],
            }
        elif self.Game in ['Ready Or Not']:
            return {
                'Path': os.path.join(self.GamePath, 'ReadyOrNot', 'Binaries', 'Win64', 'OnlineFix.ini'),
                'ConfigSection': ['Main', 'Language'],
            }
        elif self.Game in ['Baldurs Gate 3']:
            return {
                'Path': os.path.join(self.GamePath, 'bin', 'OnlineFix.ini'),
                'ConfigSection': ['Main', 'Language'],
            }


    def CheckIfPirateGameIsEnabled(self):
        for root, dirs, files in os.walk(self.GamePath):
            for fileName in files:
                if any(str(fileName).lower() == str(file).lower() for file in self.PirateArchives['Files']):
                    return True
            for dirName in dirs:
                if any(str(dirName).lower() == Dir.lower() for Dir in self.PirateArchives['Folders']):
                    return True
        return False


    def EnablePirateGame(self):
        if self.FixPath == '' or not os.path.exists(self.FixPath):
            print(f"The path '{self.FixPath}' does not exist.")
            return
        self.BackUpGameFolder()
        print("Enabling play Pirate Game")
        try:
            for root, dirs, files in os.walk(self.FixPath):

                relative_path = str(os.path.relpath(root, self.FixPath))
                destination_root = os.path.join(self.GamePath, relative_path)

                os.makedirs(destination_root, exist_ok=True)

                for fileName in files:
                    sourceFilePath = str(os.path.join(root, fileName))
                    destinationFilePath = str(os.path.join(destination_root, fileName))

                    if os.path.exists(destinationFilePath):
                        if os.path.isdir(destinationFilePath):
                            shutil.rmtree(destinationFilePath)
                        else:
                            os.remove(destinationFilePath)

                    shutil.copy2(sourceFilePath, destinationFilePath)
            Utils().clear_console()
            print("Pirate Game enabled!")

        except Exception as e:
            print(f"Error: {e}")
    def BackUpGameFolder(self):
        print('Backing up game specific files/folders...')
        if self.BackUpFile == None:
            Utils().clear_console()
            print('No files/folders to backup')
            return
        for file in self.BackUpFile['Files']:
            FileExtension = file.split('.')[-1]
            FileName = file.replace(f'.{FileExtension}', '')
            if not os.path.exists(os.path.join(self.GamePath, f'{FileName}_backup.{FileExtension}')):
                os.rename(os.path.join(self.GamePath, file),
                          os.path.join(self.GamePath, f'{FileName}_backup.{FileExtension}'))
        for folder in self.BackUpFile['Folders']:
            if not os.path.exists(os.path.join(self.GamePath, f'{folder}_backup')):
                shutil.copytree(os.path.join(self.GamePath, folder),
                                os.path.join(self.GamePath, f'{folder}_backup'))
        Utils().clear_console()
        print('Backed-Up Sucessfully!')
    def RestoreGameFolder(self):
        print('Restoring game specific files/folders...')
        if self.BackUpFile == None:
            Utils().clear_console()
            print('No files/folders to restore')
            return
        for file in self.BackUpFile['Files']:
            FileExtension = file.split('.')[-1]
            FileName = file.replace(f'.{FileExtension}', '')
            if os.path.exists(os.path.join(self.GamePath, f'{FileName}_backup.{FileExtension}')):
                os.remove(os.path.join(self.GamePath, file))
                os.rename(os.path.join(self.GamePath, f'{FileName}_backup.{FileExtension}'),
                          os.path.join(self.GamePath, file))
        for folder in self.BackUpFile['Folders']:
            if os.path.exists(os.path.join(self.GamePath, f'{folder}_backup')):
                if os.path.exists(os.path.join(self.GamePath, folder)):
                    shutil.rmtree(os.path.join(self.GamePath, folder))
                os.rename(os.path.join(self.GamePath, f'{folder}_backup'),
                          os.path.join(self.GamePath, folder))

        Utils().clear_console()
        print('Restored Sucessfully!')
    def DisablePirateGame(self):
        print("Disabling play with Pirate Game")
        self.RestoreGameFolder()
        for root, dirs, files in os.walk(self.GamePath):
            for fileName in files:
                if any(str(fileName).lower() == file.lower() for file in self.PirateArchives['Files']):
                    os.remove(os.path.join(root, fileName))
            for dirName in dirs:
                if any(str(dirName).lower() == Dir.lower() for Dir in self.PirateArchives['Folders']):
                    shutil.rmtree(os.path.join(root, dirName))
        Utils().clear_console()
        print("Pirate Game Disabled!")

    def ChangeLanguage(self):
        ChangingPaths = [self.FixPath, self.GamePath]
        languageChoice = ''
        LanguageSetting1 = self.LanguageFileConfig['ConfigSection'][0]
        LanguageSetting2 = self.LanguageFileConfig['ConfigSection'][1]
        for path in ChangingPaths:
            try:
                config = configparser.ConfigParser()
                filePath = self.LanguageFileConfig['Path'].replace(self.GamePath, path)
                if not os.path.exists(filePath):
                    print(f"The file '{filePath}' does not exist.")
                    continue
                config.read(filePath)
                if languageChoice == '':

                    print(f'Current Language: {config[LanguageSetting1][LanguageSetting2]}')
                    languageChoice = self.ShowAvailableLanguages()
                config[LanguageSetting1][LanguageSetting2] = languageChoice
                with open(filePath, 'w') as iniFile:
                    config.write(iniFile)
                print(f'Language changed in {filePath}')
            except Exception as e:
                print(f"Warning: {e}")
        return languageChoice
    def ShowAvailableLanguages(self):
        Utils().clear_console()
        LanguageDict = {}
        for index, language in enumerate(self.LanguagesAvailable):
            LanguageDict[index+1] = language

        while True:
            for key, value in LanguageDict.items():
                tested = '[ TESTED LANGUAGE ]'
                print(f"[{key}] => {value} {tested if value in ['english', 'brazilian', 'en_US', 'pt_BR'] else ''}")

            LanguageChoice = input("Choose the language [ ONLY NUMBER ON THE LEFT ]: ")
            if LanguageChoice.isdigit() and int(LanguageChoice) in LanguageDict.keys():
                return LanguageDict[int(LanguageChoice)]
            Utils().clear_console()
            print("Invalid choice, choose another one")

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
                            self.DisablePirateGame()
                        else:
                            self.EnablePirateGame()
                    case '2':
                        Utils().clear_console()
                        if self.Game not in self.GamesAvailableChangeTextLanguage:
                            print('GAME IS NOT AVAILABLE TO CHANGE TEXT/SUBTITLE LANGUAGE')
                            continue
                        self.ChangeLanguage()
                    case '3':
                        Utils().clear_console()
                        self.ModsService.Switcher()
                    case '4':
                        Utils().clear_console()
                        GamePath = GameDownloader().DownloadGame(self.Game, self.GamePath)
                        if GamePath != None:
                            self.gamePath = GamePath
                            AppConfigService().UpdateAppConfig(f'{self.Game}', f'GamePath', self.gamePath)
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
