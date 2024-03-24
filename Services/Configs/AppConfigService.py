from Data.GoogleDriveData import GoogleDrive
from Services.UtilsService import Utils
import json, os


class AppConfigService():
    def CreateAppConfig(self) -> None:
        GamesAvailable = GoogleDrive().GetGoogleDriveSheetAsCsv('1kQRBe_Ue6Si0RVD0SIWhCXzvCb0v-6bV0njAhaDp97k')
        AppConfig = {}
        for game in GamesAvailable:
            if game['GameName'] == 'Spacewar':
                AppConfig[game['GameName']] = {
                    "GamePath": ''
                }
                continue
            AppConfig[game['GameName']] = {
                "GamePath": '',
                "FixPath": '',
                "ModsPath": '',
                "EnginePath": ''
            }
        with open(f'./appconfig.json', 'w') as f:
            f.write(Utils().TransformDictToJson(AppConfig))
        print("File appconfig.json successfully made!")

    def UpdateAppConfig(self, key: str, subkey: str, value: str) -> None:
        with open(f'./appconfig.json', 'r+') as f:
            jsonDict = json.load(f)
            if subkey is not None or subkey != '':
                jsonDict[key][subkey] = value
            else:
                jsonDict[key] = value
            f.seek(0)
            f.truncate()
            json.dump(jsonDict, f, indent=4)

    def ReadAppConfig(self) -> dict:
        with open('appconfig.json', 'r') as f:
            jsonString = f.read()
            return json.loads(jsonString)

    def FixAppConfigValues(self, jsonDict: dict) -> dict:
        print('Fixing appconfig values...')
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
                if not os.path.exists(jsonDict[key][subkey]):
                    jsonDict[key][subkey] = ''
        print('Appconfig values fixed!')
        return jsonDict
