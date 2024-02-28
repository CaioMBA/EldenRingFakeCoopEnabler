import winreg, os, json

class Utils():
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
                "EldenRingGamePath": input("Coloque o caminho para a pasta Game do EldenRing (Ex: "
                                           r"%programfiles(x86)%\Steam\steamapps\common\ELDEN RING\Game): "),
                "EldenRingFixPath": input(
                    "Coloque o caminho para a pasta FIX do EldenRing (Caso não a tenha apenas pressione Enter): "),
                "EldenRingDubPath": input(
                    "Coloque o caminho para a pasta da dublagem do EldenRing (Caso não a tenha apenas pressione Enter): "),
                "SpaceWarGamePath": input("Coloque o caminho para a pasta Game do SpaceWar (Ex: "
                                          r"%programfiles(x86)%\Steam\steamapps\common\SpaceWar): ")
            }
            f.write(json.dumps(jsonDict, indent=4))
        print("Arquivo appconfig.json criado com sucesso!")
    def updateJsonConfig(self, key:str, value:str):
        with open(f'./appconfig.json', 'r+') as f:
            jsonDict = json.load(f)
            jsonDict[key] = value
            f.seek(0)
            f.truncate()
            json.dump(jsonDict, f, indent=4)
