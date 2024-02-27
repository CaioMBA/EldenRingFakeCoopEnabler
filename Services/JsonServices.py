import json

class JsonServices():
    def CreateJsonConfi(self):
        with open(f'../appconfig.json', 'w') as f:
            jsonDict = {
                "EldenRingGamePath": input("Coloque o caminho para a pasta Game do EldenRing (Ex: "
                                           r"%programfiles(x86)%\Steam\steamapps\common\ELDEN RING\Game): "),
                "EldenRingFixPath": input(
                    "Coloque o caminho para a pasta Game do EldenRing (Caso não a tenha apenas pressione Enter): "),
                "EldenRingDubPath": input(
                    "Coloque o caminho para a pasta da dublagem do EldenRing (Caso não a tenha apenas pressione Enter): "),
                "SpaceWarGamePath": input("Coloque o caminho para a pasta Game do SpaceWar (Ex: "
                                          r"%programfiles(x86)%\Steam\steamapps\common\SpaceWar): ")
            }
            f.write(json.dumps(jsonDict, indent=4))
        print("Arquivo appconfig.json criado com sucesso!")
    def updateJsonConfig(self, key:str, value:str):
        with open(f'../appconfig.json', 'r+') as f:
            jsonDict = json.load(f)
            jsonDict[key] = value
            f.seek(0)
            f.truncate()
            json.dump(jsonDict, f, indent=4)