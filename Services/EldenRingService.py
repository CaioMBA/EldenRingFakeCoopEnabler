import os, shutil, time, configparser, toml
from Services.UtilsService import Utils
from Data.GoogleDriveData import GoogleDrive
from Services.GameDownloaderService import GameDownloader
from Data.OneDriveData import OneDrive
class EldenRing():
    def __init__(self, jsonDict:dict):
        if jsonDict['GamePath'] == '' or jsonDict['GamePath'] is None:
            path = GameDownloader().EldenRingDownloadOrUpdate()
            Utils().updateJsonConfig('ELDEN RING', 'GamePath', path + r'\Game')
            Utils().ReadJsonConfig()
        jsonDict = Utils().FixJsonConfigValues(jsonDict)
        self.EldenRingGamePath = jsonDict['GamePath']
        self.EldenRingFixPath = jsonDict['FixPath']
        self.EldenRingDubPath = jsonDict['ModsPath']
        self.EldenRingDubPath = jsonDict['EnginePath']
        self.PirateFiles = ['dlllist.txt', 'onlinefix.ini', 'onlinefix.url', 'onlinefix64.dll', 'winmm.dll']
        self.DubArchives = {
            'Files': ['config_eldenring.toml', 'modengine2_launcher.exe'],
            'Folders': ['mod', 'modengine2', 'movie']
        }

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

                # Copy files into the destination directory
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

    def EnableDub(self):
        if self.EldenRingDubPath == '' or not os.path.exists(self.EldenRingDubPath):
            print(f"The path '{self.EldenRingDubPath}' does not exist.")
            return

        self.BackUpMovieFolder()

        try:
            for root, dirs, files in os.walk(self.EldenRingDubPath):

                relative_path = os.path.relpath(root, self.EldenRingDubPath)
                destination_root = os.path.join(self.EldenRingGamePath, relative_path)

                os.makedirs(destination_root, exist_ok=True)

                for fileName in files:
                    sourceFilePath = os.path.join(root, fileName)
                    destinationFilePath = os.path.join(destination_root, fileName)

                    if os.path.exists(destinationFilePath):
                        if os.path.isdir(destinationFilePath):
                            shutil.rmtree(destinationFilePath)
                        else:
                            os.remove(destinationFilePath)

                    shutil.copy2(sourceFilePath, destinationFilePath)

        except Exception as e:
            print(f"Error: {e}")

    def BackUpMovieFolder(self):
        backup_name = 'movie_backup'
        backup_path = os.path.join(self.EldenRingGamePath, backup_name)
        try:
            shutil.copytree(os.path.join(self.EldenRingGamePath, 'movie'), backup_path)
            print(f'Backup successful. Folder "movie" backed up to "{backup_path}".')
        except Exception as e:
            print(f"Error: {e}")

    def DisablePirateGame(self):
        print("Disable play with Pirate Game")
        for root, dirs, files in os.walk(self.EldenRingGamePath):
            for fileName in files:
                if str(fileName).lower() in self.PirateFiles:
                    os.remove(os.path.join(root,fileName))
            for dirName in dirs:
                if str(dirName).lower() in self.PirateFiles:
                    shutil.rmtree(os.path.join(root,dirName))
        Utils().clear_console()
        print("Pirate Game CO-OP disabled!")

    def DisableDub(self):
        backup_path = os.path.join(self.EldenRingGamePath, 'movie_backup')
        for root, dirs, files in os.walk(self.EldenRingGamePath):
            for fileName in files:
                if str(fileName).lower() in self.DubArchives['Files']:
                    os.remove(os.path.join(root,fileName))
            for dirName in dirs:
                if str(dirName).lower() in self.DubArchives['Folders']:
                    if not os.path.exists(backup_path) and dirName == 'movie':
                        continue
                    shutil.rmtree(os.path.join(root, dirName))
        try:
            shutil.copytree(backup_path, os.path.join(self.EldenRingGamePath, 'movie'))
            shutil.rmtree(backup_path)
        except Exception as e:
            print(f"Warning: {e}")

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

    def ChangeCoopPassword(self):
        ChangingPaths = [self.EldenRingGamePath, self.EldenRingFixPath]
        newPassword = ''
        for path in ChangingPaths:
            try:
                config = configparser.ConfigParser()
                filePath = os.path.join(path, r'SeamlessCoop\seamlesscoopsettings.ini')
                config.read(filePath)
                print(f'Current Password: {config['PASSWORD']['cooppassword']}')
                if newPassword == '':
                    newPassword = str(input('Set the new password: '))
                config['PASSWORD']['cooppassword'] = newPassword
                with open(filePath, 'w') as iniFile:
                    config.write(iniFile)
                print(f'Password changed in {filePath}')
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

    def SetModEngineToml(self):
        tomlPath = os.path.join(self.EldenRingDubPath, 'config_eldenring.toml')
        with open(tomlPath, 'r') as file:
            data = toml.load(file)
        if os.path.exists(os.path.join(self.EldenRingGamePath, 'SeamlessCoop')) and not os.path.exists(os.path.join(self.EldenRingGamePath, 'winmm.dll')):
            data['modengine']['external_dlls'] = [r'SeamlessCoop\elden_ring_seamless_coop.dll']
        else:
            data['modengine']['external_dlls'] = []
        with open(tomlPath, 'w') as file:
            toml.dump(data, file)

    def CheckIfPirateGameIsEnabled(self):
        for root, dirs, files in os.walk(self.EldenRingGamePath):
            for fileName in files:
                if str(fileName).lower() in self.PirateFiles and not root.endswith('SeamlessCoop'):
                    return True
        return False
    def menu(self):
        Utils().clear_console()
        try:
            while True:
                print(f"1. {'Disable' if self.CheckIfPirateGameIsEnabled() else 'Enable'} play Pirate Game")
                print("3. Change Text/Subtitle Game Language")
                print("4. Enable Brazilian-Portuguese Dubbing")
                print("5. Disable Brazilian-Portuguese Dubbing")
                print("6. Change Coop Password")
                print("7. Download-Install/Update Elden Ring")
                print("0. Exit")
                choice = input("Enter choice: ")
                match choice:
                    case "1":
                        if self.CheckIfPirateGameIsEnabled():
                            self.DisablePirateGame()
                        else:
                            self.EnablePirateGame()
                    case "3":
                        print("Changing Language")
                        self.ChangeLanguage()
                        Utils().clear_console()
                        print("Language changed!")
                    case "4":
                        print("Enabling Brazilian-Portuguese Dubbing")
                        self.SetModEngineToml()
                        self.EnableDub()
                        Utils().clear_console()
                        print("Brazilian-Portuguese Dubbing enabled!")
                    case "5":
                        print("Disabling Brazilian-Portuguese Dubbing")
                        self.DisableDub()
                        Utils().clear_console()
                        print("Brazilian-Portuguese Dubbing disabled!")
                    case "6":
                        print("Changing Coop Password")
                        newPass = self.ChangeCoopPassword()
                        Utils().clear_console()
                        print(f"Coop Password changed! Now: {newPass}")
                    case "7":
                        print("Downloading and Installing Elden Ring")
                        GamePath = GameDownloader().EldenRingDownloadOrUpdate()
                        if GamePath != None:
                            self.EldenRingGamePath = GamePath + r'\Game'
                            Utils().updateJsonConfig('EldenRingGamePath', self.EldenRingGamePath)
                        time.sleep(2.5)
                        Utils().clear_console()
                        if GamePath != None:
                            print(f'Download and Install Elden Ring completed! Path: {self.EldenRingGamePath}')
                        else:
                            print(f'Failed to download Elden Ring')
                    case "0":
                        print("Exiting...")
                        Utils().clear_console()
                        break
                    case _:
                        print("Invalid choice, choose another one")
                        time.sleep(2.5)
                        Utils().clear_console()
        except Exception as e:
            Utils().clear_console()
            print(f"Error: {e}")
            self.menu()