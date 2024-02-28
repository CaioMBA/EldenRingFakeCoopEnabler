import winreg, os, json, ctypes, zipfile, psutil, time
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

            return os.path.join(steam_install_dir, "steamapps", "common")
        except FileNotFoundError:
            print("Steam is not installed or registry key not found.")
            return None
        finally:
            winreg.CloseKey(key)

    def CreateJsonConfig(self):
        with open(f'./appconfig.json', 'w') as f:
            jsonDict = {
                "EldenRingGamePath": input("SET ELDEN RING GAME PATH (Ex: "
                                           r"%programfiles(x86)%\Steam\steamapps\common\ELDEN RING\Game): "),
                "EldenRingFixPath": input(
                    "SET ELDEN RING FIX PATH (IF YOU DON'T HAVE IT PRESS [ ENTER ]): "),
                "EldenRingDubPath": input(
                    "SET ELDEN RING DUB PATH (IF YOU DON'T HAVE IT PRESS [ ENTER ]): "),
                "SpaceWarGamePath": input("SET SPACE WAR GAME PATH (Ex: "
                                          r"%programfiles(x86)%\Steam\steamapps\common\SpaceWar): ")
            }
            f.write(self.TransformDictToJson(jsonDict))
        print("File appconfig.json successfully made!")

    def updateJsonConfig(self, key:str, value:str):
        with open(f'./appconfig.json', 'r+') as f:
            jsonDict = json.load(f)
            jsonDict[key] = value
            f.seek(0)
            f.truncate()
            json.dump(jsonDict, f, indent=4)

    def ReadJsonConfig(self):
        with open('appconfig.json', 'r') as f:
            jsonString = f.read()
            return json.loads(jsonString)

    def DeCompress(self, fileName:str, FinalPath:str):
        with zipfile.ZipFile(fileName, 'r') as zip_ref:
            file_count = len(zip_ref.infolist())
            with tqdm(total=file_count, desc="Extracting") as pbar:
                for file in zip_ref.infolist():
                    zip_ref.extract(file, FinalPath)
                    pbar.update(1)
        os.remove(fileName)
        print(f'FILE {fileName.upper()} EXTRACTED!')
        return FinalPath

    def CheckIfOneDriveExists(self, finalDir:str):
        if os.path.exists(os.path.expanduser(r'~\OneDrive')):
            return os.path.join(os.path.expanduser(r'~\OneDrive'), finalDir)
        return os.path.expanduser(f'~\\{finalDir}')

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
        for process in psutil.process_iter(['pid', 'name']):
            if appName in process.name():
                time.sleep(5)
                return True
        return False

    def TryOpenApp(self, appName:str, appPath:str):
        try:
            os.startfile(appPath)
            print(f'APP {appName} OPENED!')
        except FileNotFoundError:
            print(f"App {appName} not found! Open it manually to proceed")
