import shutil
import winreg, os, json, ctypes, zipfile, rarfile, psutil, time, csv, io
from ctypes import wintypes
from tqdm import tqdm

class Utils():
    def RunShellAsAdmin(self, command, params=None):
        shell32 = ctypes.windll.shell32
        if params is None:
            params = ''
        show_cmd = wintypes.INT(1)
        wintypes.HINSTANCE(shell32.ShellExecuteW(None, 'runas', command, params, None, show_cmd))

    def get_steam_installation_directory(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam")
            steam_install_dir = winreg.QueryValueEx(key, "SteamPath")[0]
            steam_install_dir = steam_install_dir.replace('/', '\\')

            return os.path.join(steam_install_dir, "steamapps", "common")
        except FileNotFoundError:
            print("Steam is not installed or registry key not found.")
            return None
        finally:
            winreg.CloseKey(key)

    def CreateJsonConfig(self):
        with open(f'./appconfig.json', 'w') as f:
            jsonDict = {
                {
                    "ELDEN RING": {
                        "GamePath": input("SET ELDEN RING GAME PATH (Ex: "
                                           r"%programfiles(x86)%\Steam\steamapps\common\ELDEN RING\Game): "),
                        "FixPath": input("SET ELDEN RING FIX PATH (IF YOU DON'T HAVE IT PRESS [ ENTER ]): "),
                        "EnginePath": input("SET ELDEN RING ENGINE PATH (IF YOU DON'T HAVE IT PRESS [ ENTER ]): "),
                        "ModsPath": input("SET ELDEN RING MODS PATH (IF YOU DON'T HAVE IT PRESS [ ENTER ]): ")
                    },
                    "Spacewar":{
                        "GamePath": input("SET SPACE WAR GAME PATH (Ex: "
                                          r"%programfiles(x86)%\Steam\steamapps\common\SpaceWar): ")
                    }
                }
            }
            f.write(self.TransformDictToJson(jsonDict))
        print("File appconfig.json successfully made!")

    def updateJsonConfig(self, key: str, subkey: str, value: str):
        with open(f'./appconfig.json', 'r+') as f:
            jsonDict = json.load(f)
            if subkey is not None or subkey != '':
                jsonDict[key][subkey] = value
            else:
                jsonDict[key] = value
            f.seek(0)
            f.truncate()
            json.dump(jsonDict, f, indent=4)

    def ReadJsonConfig(self):
        with open('appconfig.json', 'r') as f:
            jsonString = f.read()
            return json.loads(jsonString)

    def GetSecretAccounts(self):
        with open('secretAccounts.json', 'r') as f:
            jsonString = f.read()
            return json.loads(jsonString)

    def FixJsonConfigValues(self, jsonDict:dict):
        for key in jsonDict.keys():
            for subkey in jsonDict[key].keys():
                if jsonDict[key][subkey] is None:
                    jsonDict[key][subkey] = ''
                    continue
                jsonDict[key][subkey] = jsonDict[key][subkey].replace('%programfiles(x86)%', os.environ.get('ProgramFiles(x86)', ''))
                jsonDict[key][subkey] = jsonDict[key][subkey].replace('%userprofile%', os.path.expanduser('~'))
                jsonDict[key][subkey] = jsonDict[key][subkey].replace('%programdata%', os.environ.get('ProgramData', ''))
                jsonDict[key][subkey] = jsonDict[key][subkey].replace('%localappdata%', os.environ.get('LocalAppData', ''))
                jsonDict[key][subkey] = jsonDict[key][subkey].replace('%appdata%', os.environ.get('AppData', ''))
                jsonDict[key][subkey] = jsonDict[key][subkey].replace('%temp%', os.environ.get('TEMP', ''))
                jsonDict[key][subkey] = jsonDict[key][subkey].replace('%windir%', os.environ.get('WINDIR', ''))
                jsonDict[key][subkey] = jsonDict[key][subkey].replace('%systemroot%', os.environ.get('SystemRoot', ''))
                jsonDict[key][subkey] = jsonDict[key][subkey].replace('%systemdrive%', os.environ.get('SystemDrive', ''))
        return jsonDict

    def DeCompress(self, fileName:str, FinalPath:str):
        if fileName.endswith('.zip'):
            return self.Unzip(fileName, FinalPath)
        elif fileName.endswith('.rar'):
            return self.Unrar(fileName, FinalPath)

    def Unzip(self, fileName:str, FinalPath:str):
        with zipfile.ZipFile(fileName, 'r') as zip_ref:
            file_count = len(zip_ref.infolist())
            with tqdm(total=file_count, desc="Extracting") as pbar:
                for file in zip_ref.infolist():
                    zip_ref.extract(file, FinalPath)
                    pbar.update(1)
        os.remove(fileName)
        print(f'FILE {fileName.upper()} EXTRACTED!')
        return FinalPath
    def Unrar(self, fileName:str, FinalPath:str):
        with rarfile.RarFile(fileName, 'r') as rar_ref:
            file_count = len(rar_ref.infolist())
            with tqdm(total=file_count, desc="Extracting") as pbar:
                for file in rar_ref.infolist():
                    rar_ref.extract(file, FinalPath)
                    pbar.update(1)
        os.remove(fileName)
        print(f'FILE {fileName.upper()} EXTRACTED!')
        return FinalPath

    def CheckIfOneDriveExists(self, finalDir:str):
        finalPath = os.path.join(os.path.expanduser(r'~'), finalDir)
        if os.path.exists(os.path.join(os.path.expanduser(r'~'), 'OneDrive')):
            finalPath = os.path.join(os.path.expanduser(r'~'), 'OneDrive', finalDir)
        if not os.path.exists(finalPath):
            finalPath = os.path.join(os.path.expanduser(r'~'), 'Downloads')
        return finalPath

    def TransformJsonToDict(self, jsonString:str):
        return json.loads(jsonString)

    def TransformDictToJson(self, jsonDict:dict):
        return json.dumps(jsonDict, indent=4)

    def clear_console(self):
        operational_system = os.name
        if operational_system == 'posix':  # Linux ou macOS
            os.system('clear')
        elif operational_system == 'nt':  # Windows
            os.system('cls')

    def CheckIfAppIsRunning(self, appName:str):
        print(f'Checking if {appName} is running...')
        for process in psutil.process_iter(['pid', 'name']):
            if appName in process.name():
                time.sleep(5)
                print(f'{appName} is running!')
                return True
        print(f'{appName} is not running!')
        return False

    def TryOpenApp(self, appName:str, appPath:str):
        try:
            os.startfile(appPath)
            print(f'APP {appName} OPENED!')
        except FileNotFoundError:
            print(f"App {appName} not found! Open it manually to proceed")

    def TransformCsvByteStringToDict(self, csvByteString:bytes):
        csvfile = io.StringIO(csvByteString.decode('utf-8'))
        reader = csv.DictReader(csvfile)
        result = []
        for row in reader:
            result.append(dict(row))
        return result

    def DeleteSpecificDir(self, path:str):
        shutil.rmtree(path, ignore_errors=True)
