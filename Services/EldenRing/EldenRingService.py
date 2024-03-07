import os, shutil, time, configparser
from Services.UtilsService import Utils
from Services.GameDownloaderService import GameDownloader
from Services.EldenRing.ModsService import Mods
class EldenRing():
    def __init__(self, jsonDict:dict):
        if jsonDict['GamePath'] == '' or jsonDict['GamePath'] is None:
            path = GameDownloader().EldenRingDownloadOrUpdate()
            Utils().updateJsonConfig('ELDEN RING', 'GamePath', path + r'\Game')
            Utils().ReadJsonConfig()
        jsonDict = Utils().FixJsonConfigValues(jsonDict)
        self.EldenRingGamePath = jsonDict['GamePath']
        self.EldenRingFixPath = jsonDict['FixPath']
        self.EldenRingModEnginePath = jsonDict['EnginePath']
        self.EldenRingMods = Mods(jsonDict['ModsPath'], self.EldenRingModEnginePath, self.EldenRingGamePath)
        self.PirateArchives = {
            "Files": ['winmm.dll', 'OnlineFix64.dll', 'OnlineFix.url', 'OnlineFix.ini', 'dlllist.txt'],
            "Folders": []
        }

    def CheckIfPirateGameIsEnabled(self):
        for root, dirs, files in os.walk(self.EldenRingGamePath):
            for fileName in files:
                if fileName.lower() == 'winmm.dll':
                    return True
        return False
    def EnablePirateGame(self):
        print("Enabling play with Pirate Game")
        if self.EldenRingFixPath == '' or not os.path.exists(self.EldenRingFixPath):
            print(f"The path '{self.EldenRingFixPath}' does not exist.")
            return
        try:
            for root, dirs, files in os.walk(self.EldenRingFixPath):

                relative_path = str(os.path.relpath(root, self.EldenRingFixPath))
                destination_root = os.path.join(self.EldenRingGamePath, relative_path)

                os.makedirs(destination_root, exist_ok=True)

                for fileName in files:
                    sourceFilePath = str(os.path.join(root, fileName))
                    destinationFilePath = str(os.path.join(destination_root, fileName))

                    if os.path.exists(destinationFilePath):
                        continue

                    shutil.copy2(sourceFilePath, destinationFilePath)
            Utils().clear_console()
            print("Pirate Game CO-OP enabled!")

        except Exception as e:
            print(f"Error: {e}")
    def DisablePirateGame(self):
        print("Disabling play with Pirate Game")
        for root, dirs, files in os.walk(self.EldenRingGamePath):
            for fileName in files:
                if any(str(fileName).lower() == file.lower() for file in self.PirateArchives['Files']):
                    os.remove(os.path.join(root,fileName))
            for dirName in dirs:
                if any(str(dirName).lower() == Dir.lower() for Dir in self.PirateArchives['Folders']):
                    shutil.rmtree(os.path.join(root,dirName))
        Utils().clear_console()
        print("Pirate Game CO-OP disabled!")

    def ChangeLanguage(self):
        ChangingPaths = [self.EldenRingFixPath, self.EldenRingGamePath]
        languageChoice = ''
        for path in ChangingPaths:
            try:
                config = configparser.ConfigParser()
                filePath = os.path.join(path, 'OnlineFix.ini')
                config.read(filePath)
                if languageChoice == '':
                    languageChoice = self.ShowAvailableLanguages()
                config['Main']['Language'] = languageChoice
                with open(filePath, 'w') as iniFile:
                    config.write(iniFile)
                print(f'Language changed in {filePath}')
            except Exception as e:
                print(f"Warning: {e}")
    def ShowAvailableLanguages(self):
        Utils().clear_console()
        LanguageDict = {
            1: 'english',
            2: 'brazilian',
            3: 'french',
            4: 'german',
            5: 'hungarian',
            6: 'italian',
            7: 'japanese',
            8: 'koreana',
            9: 'latam',
            10: 'polish',
            11: 'russian',
            12: 'schinese',
            13: 'spanish',
            14: 'tchinese',
            15: 'thai'
        }
        while True:
            for key, value in LanguageDict.items():
                tested = '[ TESTED LANGUAGE ]'
                print(f"[{key}] => {value} {tested if key in [1, 2] else ''}")

            LanguageChoice = input("Choose the language [ ONLY NUMBER ON THE LEFT ]: ")
            if LanguageChoice.isdigit() and int(LanguageChoice) in LanguageDict.keys():
                return LanguageDict[int(LanguageChoice)]
            Utils().clear_console()
            print("Invalid choice, choose another one")




    def menu(self):
        Utils().clear_console()
        try:
            while True:
                print("[ ELDEN RING GENERAL MENU ]")
                print(f"1. {'DISABLE' if self.CheckIfPirateGameIsEnabled() else 'ENABLE'} play pirate game")
                print("2. Change TEXT/SUBTITLE pirate game LANGUAGE")
                print("3. MODS MENU")
                print("4. Change co-op password")
                print("5. Download-Install|Update Elden Ring")
                print("0. Exit")
                choice = input("Enter choice: ")
                match choice:
                    case "1":
                        if self.CheckIfPirateGameIsEnabled():
                            self.DisablePirateGame()
                        else:
                            self.EnablePirateGame()
                    case "2":
                        print("Changing Language")
                        self.ChangeLanguage()
                        Utils().clear_console()
                        print("Language changed!")
                    case "3":
                        Utils().clear_console()
                        self.EldenRingMods.menu()
                    case "4":
                        print("Changing Coop Password")
                        newPass = self.EldenRingMods.ChangeCoopPassword()
                        Utils().clear_console()
                        print(f"Coop Password changed! Now: {newPass}")
                    case "5":
                        print("Downloading and Installing Elden Ring")
                        GamePath = GameDownloader().EldenRingDownloadOrUpdate(self.EldenRingGamePath.replace(r'\Game', ''))
                        if GamePath != None:
                            self.EldenRingGamePath = GamePath + r'\Game'
                            Utils().updateJsonConfig('EldenRingGamePath', 'GamePath', self.EldenRingGamePath)
                        time.sleep(2.5)
                        Utils().clear_console()
                        if GamePath != None:
                            print(f'Download and Install Elden Ring completed! Path: {self.EldenRingGamePath}')
                        else:
                            print(f'Failed to download Elden Ring')
                    case "0":
                        print("Exiting Elden Ring Menu...")
                        Utils().clear_console()
                        break
                    case _:
                        Utils().clear_console()
                        print(f"Invalid choice: {choice}, choose another one")

        except Exception as e:
            Utils().clear_console()
            print(f"Error: {e}")
            self.menu()