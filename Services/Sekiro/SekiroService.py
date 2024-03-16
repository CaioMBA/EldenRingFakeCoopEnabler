import os, shutil, configparser
from Services.UtilsService import Utils
from Services.GameDownloaderService import GameDownloader
from Services.EldenRing.ModsService import Mods

class Sekiro():
    def __init__(self, GamePath, fixPath, EnginePath, ModsPath, pirateArchives:dict):
        if GamePath == '' or GamePath is None:
            path = GameDownloader().SekiroDownloadOrUpdate()
            Utils().updateJsonConfig('Sekiro', 'GamePath', path)
            print('FOR THE GAME TO WORK, YOU NEED TO RESTART THIS PROGRAM')
            return

        self.GamePath = GamePath
        self.FixPath = fixPath
        self.ModEnginePath = EnginePath
        self.Mods = Mods(ModsPath, self.ModEnginePath, self.GamePath)
        self.PirateArchives = pirateArchives

    def EnablePirateGame(self):
        print("Enabling play Pirate Game")
        if self.FixPath == '' or not os.path.exists(self.FixPath):
            print(f"The path '{self.FixPath}' does not exist.")
            return
        self.BackUpGameFolder()
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
        if not os.path.exists(os.path.join(self.GamePath, 'steam_api64_backup.dll')):
            os.rename(os.path.join(self.GamePath, 'steam_api64.dll'),
                      os.path.join(self.GamePath, 'steam_api64_backup.dll'))
        if not os.path.exists(os.path.join(self.GamePath, 'sekiro_backup.exe')):
            os.rename(os.path.join(self.GamePath, 'sekiro.exe'),
                      os.path.join(self.GamePath, 'sekiro_backup.exe'))

    def RestoreBackUp(self):
        if os.path.exists(os.path.join(self.GamePath, 'steam_api64_backup.dll')):
            os.remove(os.path.join(self.GamePath, 'steam_api64.dll'))
            os.rename(os.path.join(self.GamePath, 'steam_api64_backup.dll'),
                      os.path.join(self.GamePath, 'steam_api64.dll'))
        if os.path.exists(os.path.join(self.GamePath, 'sekiro_backup.exe')):
            os.remove(os.path.join(self.GamePath, 'sekiro.exe'))
            os.rename(os.path.join(self.GamePath, 'sekiro_backup.exe'),
                      os.path.join(self.GamePath, 'sekiro.exe'))

    def DisablePirateGame(self):
        print("Disabling play with Pirate Game")
        self.RestoreBackUp()
        for root, dirs, files in os.walk(self.GamePath):
            for fileName in files:
                if any(str(fileName).lower() == file.lower() for file in self.PirateArchives['Files']):
                    os.remove(os.path.join(root, fileName))
            for dirName in dirs:
                if any(str(dirName).lower() == Dir.lower() for Dir in self.PirateArchives['Folders']):
                    shutil.rmtree(os.path.join(root, dirName))
        Utils().clear_console()

        print("Pirate Game disabled!")

    def ChangeLanguage(self):
        ChangingPaths = [self.FixPath, self.GamePath]
        languageChoice = ''
        for path in ChangingPaths:
            try:
                config = configparser.ConfigParser()
                filePath = os.path.join(path, 'cream_api.ini')
                if not os.path.exists(filePath):
                    print(f"The file '{filePath}' does not exist.")
                    continue
                config.read(filePath)
                if languageChoice == '':
                    print(f'Current Language: {config['steam']['language']}')
                    languageChoice = self.ShowAvailableLanguages()
                config['steam']['language'] = languageChoice
                with open(filePath, 'w') as iniFile:
                    config.write(iniFile)
                print(f'Language changed in {filePath}')
            except Exception as e:
                print(f"Warning: {e}")
        return languageChoice
    def ShowAvailableLanguages(self):
        Utils().clear_console()
        LanguageDict = {
            1: 'english',
            2: 'brazilian',
            3: 'russian',
            4: 'spanish'
        }
        while True:
            for key, value in LanguageDict.items():
                tested = '[ TESTED LANGUAGE ]'
                print(f"[{key}] => {value} {tested if key in [1, 2, 3] else ''}")

            LanguageChoice = input("Choose the language [ ONLY NUMBER ON THE LEFT ]: ")
            if LanguageChoice.isdigit() and int(LanguageChoice) in LanguageDict.keys():
                return LanguageDict[int(LanguageChoice)]
            Utils().clear_console()
            print("Invalid choice, choose another one")