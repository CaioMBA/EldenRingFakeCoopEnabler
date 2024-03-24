import shutil
import winreg, os, json, ctypes, zipfile, rarfile, psutil, time, csv, io
from ctypes import wintypes
from tqdm import tqdm


class Utils():
    def RunShellAsAdmin (self, command, params=None) -> None:
        shell32 = ctypes.windll.shell32
        if params is None:
            params = ''
        show_cmd = wintypes.INT(1)
        wintypes.HINSTANCE(shell32.ShellExecuteW(None, 'runas', command, params, None, show_cmd))

    def get_steam_installation_directory(self) -> str:
        key = ''
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam")
            steam_install_dir = winreg.QueryValueEx(key, "SteamPath")[0]
            steam_install_dir = steam_install_dir.replace('/', '\\')

            return os.path.join(steam_install_dir, "steamapps", "common")
        except FileNotFoundError:
            print("Steam is not installed or registry key not found.")
            return ''
        finally:
            winreg.CloseKey(key)

    def GetSecretAccounts(self) -> dict:
        with open('secretAccounts.json', 'r') as f:
            jsonString = f.read()
            return json.loads(jsonString)

    def DeCompress(self, fileName:str, FinalPath:str) -> str:

        if fileName.endswith('.zip'):
            FinalPath = self.Unzip(fileName, FinalPath)
        elif fileName.endswith('.rar'):
            FinalPath = self.Unrar(fileName, FinalPath)
        print(f'FILE {fileName.upper()} EXTRACTED => {FinalPath}')
        return FinalPath

    def Unzip(self, fileName:str, FinalPath:str) -> str:
        with zipfile.ZipFile(fileName, 'r') as zip_ref:
            file_count = len(zip_ref.infolist())
            with tqdm(total=file_count, desc="Extracting") as pbar:
                for file in zip_ref.infolist():
                    zip_ref.extract(file, FinalPath)
                    pbar.update(1)
        os.remove(fileName)
        return FinalPath
    def Unrar(self, fileName:str, FinalPath:str) -> str:
        with rarfile.RarFile(fileName, 'r') as rar_ref:
            file_count = len(rar_ref.infolist())
            with tqdm(total=file_count, desc="Extracting") as pbar:
                for file in rar_ref.infolist():
                    rar_ref.extract(file, FinalPath)
                    pbar.update(1)
        os.remove(fileName)
        return FinalPath

    def GetDocumentsFolderPath(self) -> str:
        key = winreg.HKEY_CURRENT_USER
        sub_key = r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        try:
            with winreg.OpenKey(key, sub_key) as key:
                documents_path = winreg.QueryValueEx(key, 'Personal')[0]
                return documents_path
        except Exception as e:
            print(f"Error accessing registry: {e}")
            return ''

    def CheckIfPathExists(self, basePath:str, finalDir:str) -> str:
        finalPath = os.path.join(basePath, finalDir)
        if not os.path.exists(basePath):
            finalPath = os.path.join(os.path.expanduser(r'~'), 'Downloads', finalDir)
        if not os.path.exists(finalPath):
            os.makedirs(finalPath)
        return finalPath

    def TransformJsonToDict(self, jsonString:str) -> dict:
        return json.loads(jsonString)

    def TransformDictToJson(self, jsonDict:dict) -> str:
        return json.dumps(jsonDict, indent=4)

    def clear_console(self) -> None:
        operational_system = os.name
        if operational_system == 'posix':  # Linux ou macOS
            os.system('clear')
        elif operational_system == 'nt':  # Windows
            os.system('cls')

    def CheckIfAppIsRunning(self, appName:str) -> bool:
        print(f'Checking if {appName} is running...')
        for process in psutil.process_iter(['pid', 'name']):
            if appName in process.name():
                time.sleep(5)
                print(f'{appName} is running!')
                return True
        print(f'{appName} is not running!')
        return False

    def TryOpenApp(self, appName:str, appPath:str) -> None:
        try:
            os.startfile(appPath)
            print(f'APP {appName} OPENED!')
        except FileNotFoundError:
            print(f"App {appName} not found! Open it manually to proceed")

    def TransformCsvByteStringToDict(self, csvByteString:bytes) -> list[dict]:
        csvfile = io.StringIO(csvByteString.decode('utf-8'))
        reader = csv.DictReader(csvfile)
        result = []
        for row in reader:
            result.append(dict(row))
        return result

    def DeleteSpecificDir(self, path:str) -> None:
        shutil.rmtree(path, ignore_errors=True)
