import os, shutil, time, psutil, configparser, json
from Services.UtilsService import Utils
from Services.GoogleDriveService import GoogleDrive
from Services.GameDownloader import GameDownloader
class ReplaceFiles():
    def __init__(self, jsonDict:dict):
        for key in jsonDict.keys():
            jsonDict[key] = jsonDict[key].replace('%programfiles(x86)%', os.environ.get('ProgramFiles(x86)', ''))
            jsonDict[key] = jsonDict[key].replace('%userprofile%', os.path.expanduser('~'))
            jsonDict[key] = jsonDict[key].replace('%programdata%', os.environ.get('ProgramData', ''))
            jsonDict[key] = jsonDict[key].replace('%localappdata%', os.environ.get('LocalAppData', ''))
            jsonDict[key] = jsonDict[key].replace('%appdata%', os.environ.get('AppData', ''))
            jsonDict[key] = jsonDict[key].replace('%temp%', os.environ.get('TEMP', ''))
            jsonDict[key] = jsonDict[key].replace('%windir%', os.environ.get('WINDIR', ''))
            jsonDict[key] = jsonDict[key].replace('%systemroot%', os.environ.get('SystemRoot', ''))
            jsonDict[key] = jsonDict[key].replace('%systemdrive%', os.environ.get('SystemDrive', ''))
        self.EldenRingGamePath = jsonDict['EldenRingGamePath']
        self.SpaceWarGamePath = jsonDict['SpaceWarGamePath']
        self.EldenRingFixPath = jsonDict['EldenRingFixPath']
        self.EldenRingDubPath = jsonDict['EldenRingDubPath']
        self.PirateFiles = ['dlllist.txt', 'onlinefix.ini', 'onlinefix.url', 'onlinefix64.dll', 'winmm.dll']
        self.DubArchives = {
            'Files': ['config_armoredcore6.toml', 'config_darksouls3.toml', 'config_eldenring.toml',
                      'launchmod_armoredcore6.bat', 'launchmod_darksouls3.bat', 'launchmod_eldenring.bat',
                      'modengine2_launcher.exe', 'readme.txt'],
            'Folders': ['mod', 'modengine2', 'movie']
        }
        if jsonDict['EldenRingFixPath'] == '':
            self.EldenRingFixPath = GoogleDrive().DownloadGoogleDriveFile('1gUqZSvDwGTloZDqVHqxNzJVBqVDEQpIt')
            self.EldenRingFixPath += r'\EldenRing_FIX_PIRATE_ORIGINAL'
            Utils().updateJsonConfig('EldenRingFixPath', self.EldenRingFixPath)
        if jsonDict['EldenRingDubPath'] == '':
            self.EldenRingDubPath = GoogleDrive().DownloadGoogleDriveFile('1Rl-93Ki29EK3M--RGX4JmClD5xizy8uB')
            self.EldenRingDubPath += r'\EldenRingDubPT-BR'
            Utils().updateJsonConfig('EldenRingDubPath', self.EldenRingDubPath)



    def is_steam_running(self):
        for process in psutil.process_iter(['pid', 'name']):
            if 'steam.exe' in process.name():
                time.sleep(5)
                return True
        return False

    def CheckSpaceWar(self):
        if self.SpaceWarGamePath != '' and os.path.exists(self.SpaceWarGamePath):
            return
        print('ABRA A STEAM PARA PROSSEGUIR!')
        while True:
            if self.is_steam_running():
                print('Steam aberta!')
                break
        print('INSTALE O SPACE WAR PARA FUNCIONAR CORRETAMENTE!')
        print('CONFIGURE O CONTROLE NO SPACE WAR PARA!')
        print('O TEMPLATE DE ELDEN RING(DENTRO DA STEAM)!')
        time.sleep(2)
        os.system('start steam://install/480')
        time.sleep(7.5)
        self.SpaceWarGamePath = input("Coloque o caminho para a pasta Game do SpaceWar (Ex: "
                                     r"%programfiles(x86)%\Steam\steamapps\common\SpaceWar): ")
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
                    if os.path.exists(backup_path) and dirName == 'movie':
                        continue
                    shutil.rmtree(os.path.join(root, dirName))
        try:
            shutil.copytree(backup_path, os.path.join(self.EldenRingGamePath, 'movie'))
        except Exception as e:
            print(f"Warning: {e}")

    def ChangeLanguage(self):
        config = configparser.ConfigParser()
        filePath = os.path.join(self.EldenRingFixPath, 'OnlineFix.ini')
        config.read(filePath)
        config['Main']['Language'] = self.ShowAvailableLanguages()
        with open(filePath, 'w') as iniFile:
            config.write(iniFile)

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
        return config['PASSWORD']['cooppassword']

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
                        self.CheckSpaceWar()
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
                            self.EldenRingGamePath = GamePath
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
        with open('appconfig.json', 'r') as f:
            jsonString = f.read()
            jsonDict = json.loads(jsonString)
    except Exception as e:
        print("Não foi possível abrir o arquivo appconfig.json")
        print("Por favor, preencha as informações necessárias para o funcionamento do programa.")
        print("Caso não tenha o caminho deixe vazio")
        Utils().CreateJsonConfig()
        with open('appconfig.json', 'r') as f:
            jsonString = f.read()
            jsonDict = json.loads(jsonString)

    replacer = ReplaceFiles(jsonDict)
    replacer.menu()
