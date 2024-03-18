import os, shutil, configparser
from Services.UtilsService import Utils
from Services.GameDownloaderService import GameDownloader
from Services.EldenRing.ModsService import Mods

class AWayOut():
    def __init__(self, GamePath, fixPath, EnginePath, ModsPath, pirateArchives:dict):
        if GamePath == '' or GamePath is None:
            path = GameDownloader().AWayOutDownloadOrUpdate()
            Utils().updateJsonConfig('AWayOut', 'GamePath', path)
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
        print('Backing up GamePath folder...')
        if not os.path.exists(os.path.join(self.GamePath, 'Haze1_backup')):
            shutil.copytree(os.path.join(self.GamePath, 'Haze1'),
                            os.path.join(self.GamePath, 'Haze1_backup'))

    def RestoreGameFolder(self):
        print('Restoring GamePath folder...')
        if os.path.exists(os.path.join(self.GamePath, 'Haze1_backup')):
            if os.path.exists(os.path.join(self.GamePath, 'Haze1')):
                shutil.rmtree(os.path.join(self.GamePath, 'Haze1'))
            os.rename(os.path.join(self.GamePath, 'Haze1_backup'),
                      os.path.join(self.GamePath, 'Haze1'))

    def DisablePirateGame(self):
        print("Disabling play Pirate Game")
        self.RestoreGameFolder()
        print("Pirate Game disabled!")


    def ChangeLanguage(self):
        ChangingPaths = [self.FixPath, self.GamePath]
        languageChoice = ''
        for path in ChangingPaths:
            try:
                config = configparser.ConfigParser()
                filePath = os.path.join(path, 'Haze1', 'Binaries', 'Win64', 'CPY.ini')
                if not os.path.exists(filePath):
                    print(f"The file '{filePath}' does not exist.")
                    continue
                config.read(filePath)
                if languageChoice == '':
                    print(f'Current Language: {config['Settings']['Language']}')
                    languageChoice = self.ShowAvailableLanguages()
                config['Settings']['Language'] = languageChoice
                with open(filePath, 'w') as iniFile:
                    config.write(iniFile)
                print(f'Language changed in {filePath}')
            except Exception as e:
                print(f"Warning: {e}")
        return languageChoice
    def ShowAvailableLanguages(self):
        Utils().clear_console()
        LanguageDict = {
            1: 'en_US',
            2: 'pt_BR'
        }
        while True:
            for key, value in LanguageDict.items():
                print(f"[{key}] => {value}")

            LanguageChoice = input("Choose the language [ ONLY NUMBER ON THE LEFT ]: ")
            if LanguageChoice.isdigit() and int(LanguageChoice) in LanguageDict.keys():
                return LanguageDict[int(LanguageChoice)]
            Utils().clear_console()
            print("Invalid choice, choose another one")