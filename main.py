import os, shutil, time, configparser, toml
from Services.UtilsService import Utils
from Data.GoogleDriveData import GoogleDrive
from Services.GameDownloader import GameDownloader
from Data.OneDriveData import OneDrive
class ReplaceFiles():
    def __init__(self, jsonDict:dict):
        jsonDict = Utils().FixJsonConfigValues(jsonDict)
        if jsonDict['EldenRingFixPath'] == '':
            self.EldenRingFixPath = GameDownloader().DownloadOnlineFix()
            Utils().updateJsonConfig('EldenRingFixPath', self.EldenRingFixPath)
        if jsonDict['EldenRingDubPath'] == '':
            self.EldenRingDubPath = GameDownloader().DownloadPT_BRDubbing()
            Utils().updateJsonConfig('EldenRingDubPath', self.EldenRingDubPath)
        self.EldenRingGamePath = jsonDict['EldenRingGamePath']
        self.SpaceWarGamePath = jsonDict['SpaceWarGamePath']
        self.EldenRingFixPath = jsonDict['EldenRingFixPath']
        self.EldenRingDubPath = jsonDict['EldenRingDubPath']
        self.PirateFiles = ['dlllist.txt', 'onlinefix.ini', 'onlinefix.url', 'onlinefix64.dll', 'winmm.dll']
        self.CoopFiles = ['elden_ring_seamless_coop.dll', 'seamlesscoopsettings.ini']
        self.DubArchives = {
            'Files': ['config_eldenring.toml', 'modengine2_launcher.exe'],
            'Folders': ['mod', 'modengine2', 'movie']
        }

    def CheckSpaceWarInstallation(self):
        if not Utils().CheckIfAppIsRunning('steam.exe'):
            os.system('start steam://open/steam')
        if self.SpaceWarGamePath != '' and os.path.exists(self.SpaceWarGamePath):
            return
        while True:
            if Utils().CheckIfAppIsRunning('steam.exe'):
                print('Steam aberta! com sucesso')
                break
        print('DOWNLOADING|INSTALLING SPACE WAR SO ELDEN RING WORKS!')
        print('SETUP CONTROLLER TEMPLATE ON SPACE WAR FOR ELDEN RING(INSIDE STEAM)!')
        time.sleep(2)
        self.SpaceWarGamePath = GameDownloader().SpaceWarDownloadOrUpdate()
        #Old way to download SpaceWar
        #os.system('start steam://install/480')
        time.sleep(7.5)
        Utils().updateJsonConfig('SpaceWarGamePath', self.SpaceWarGamePath)

    def EnablePirateGame(self):
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
        for root, dirs, files in os.walk(self.EldenRingGamePath):
            for fileName in files:
                if str(fileName).lower() in self.PirateFiles:
                    os.remove(os.path.join(root,fileName))
            for dirName in dirs:
                if str(dirName).lower() in self.PirateFiles:
                    shutil.rmtree(os.path.join(root,dirName))

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
        config = configparser.ConfigParser()
        filePath = os.path.join(self.EldenRingFixPath, 'OnlineFix.ini')
        config.read(filePath)
        languageChoice = self.ShowAvailableLanguages()
        config['Main']['Language'] = languageChoice
        with open(filePath, 'w') as iniFile:
            config.write(iniFile)
        try:
            config = configparser.ConfigParser()
            filePath = os.path.join(self.EldenRingGamePath, 'OnlineFix.ini')
            config.read(filePath)
            config['Main']['Language'] = languageChoice
            with open(filePath, 'w') as iniFile:
                config.write(iniFile)
        except Exception as e:
            print(f"Warning, OnlineFix Not in Game folder: {e}")

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

    def ChangeCoopPassword(self):
        config = configparser.ConfigParser()
        filePath = os.path.join(self.EldenRingGamePath, r'SeamlessCoop\seamlesscoopsettings.ini')
        config.read(filePath)
        print(f'Current Password: {config['PASSWORD']['cooppassword']}')
        config['PASSWORD']['cooppassword'] = str(input('Set the new password: '))
        with open(filePath, 'w') as iniFile:
            config.write(iniFile)
        newPassword = config['PASSWORD']['cooppassword']
        config = configparser.ConfigParser()
        filePath = os.path.join(self.EldenRingFixPath, r'SeamlessCoop\seamlesscoopsettings.ini')
        config.read(filePath)
        config['PASSWORD']['cooppassword'] = newPassword
        with open(filePath, 'w') as iniFile:
            config.write(iniFile)
        return newPassword

    def SetModEngineToml(self):
        tomlPath = os.path.join(self.EldenRingDubPath, 'config_eldenring.toml')
        with open(tomlPath, 'r') as file:
            data = toml.load(file)
        data['modengine']['external_dlls'] = [] if not os.path.exists(os.path.join(self.EldenRingGamePath, 'SeamlessCoop')) else ['elden_ring_seamless_coop.dll']
        with open(tomlPath, 'w') as file:
            toml.dump(data, file)

    def MoveCOOPFilesToRootFolder(self):
        for root, dirs, files in os.walk(os.path.join(self.EldenRingGamePath, 'SeamlessCoop')):
            for fileName in files:
                if str(fileName).lower() in self.CoopFiles:
                    sourceFilePath = os.path.join(root,fileName)
                    destinationFilePath = os.path.join(self.EldenRingGamePath, fileName)
                    if os.path.exists(destinationFilePath):
                        continue
                    shutil.copy2(sourceFilePath, destinationFilePath)

    def DeleteCOOPFilesFromRootFolder(self):
        for root, dirs, files in os.walk(self.EldenRingGamePath):
            for fileName in files:
                if str(fileName).lower() in self.CoopFiles and not root.endswith('SeamlessCoop'):
                    os.remove(os.path.join(root, fileName))

    def menu(self):
        Utils().clear_console()
        try:
            while True:
                print("1. Enable play with Pirate Game")
                print("2. Disable play with Pirate Game")
                print("3. Change Text/Subtitle Game Language")
                print("4. Enable Brazilian-Portuguese Dubbing")
                print("5. Disable Brazilian-Portuguese Dubbing")
                print("6. Change Coop Password")
                print("7. Download-Install/Update Elden Ring")
                print("0. Exit")
                choice = input("Enter choice: ")
                match choice:
                    case "1":
                        print("Enabling play with Pirate Game")
                        self.CheckSpaceWarInstallation()
                        self.EnablePirateGame()
                        Utils().clear_console()
                        print("Pirate Game CO-OP enabled!")
                    case "2":
                        print("Disable play with Pirate Game")
                        self.DisablePirateGame()
                        Utils().clear_console()
                        print("Pirate Game CO-OP disabled!")
                    case "3":
                        print("Changing Language")
                        self.ChangeLanguage()
                        Utils().clear_console()
                        print("Language changed!")
                    case "4":
                        print("Enabling Brazilian-Portuguese Dubbing")
                        self.MoveCOOPFilesToRootFolder()
                        self.SetModEngineToml()
                        self.EnableDub()
                        Utils().clear_console()
                        print("Brazilian-Portuguese Dubbing enabled!")
                    case "5":
                        print("Disabling Brazilian-Portuguese Dubbing")
                        self.DeleteCOOPFilesFromRootFolder()
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
                            self.EldenRingGamePath = os.path.join(GamePath,r'\Game')
                            Utils().updateJsonConfig('EldenRingGamePath', self.EldenRingGamePath)
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

if '__main__' == __name__:
    try:
        jsonDict = Utils().ReadJsonConfig()
    except Exception as e:
        print("Não foi possível abrir o arquivo appconfig.json")
        print("Por favor, preencha as informações necessárias para o funcionamento do programa.")
        print("Caso não tenha o caminho deixe vazio")
        Utils().CreateJsonConfig()
        jsonDict = Utils().ReadJsonConfig()

    ReplaceFiles(jsonDict).menu()
