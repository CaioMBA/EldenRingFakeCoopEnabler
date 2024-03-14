from Services.UtilsService import Utils

class GameSwitcher():
    def __init__(self,GameName, jsonDict):
        self.Game = GameName
        self.gamePath = jsonDict['GamePath']
        self.fixPath = jsonDict['FixPath']
        self.modEnginePath = jsonDict['EnginePath']
        self.mods = jsonDict['ModsPath']
        match self.Game:
            case 'ELDEN RING':
                self.pirateArchives = {
                    "Files": ['OnlineFix64.dll', 'OnlineFix.url', 'OnlineFix.ini',
                              'winmm.dll', 'dlllist.txt'],
                    "Folders": []
                }
            case 'Enshrouded':
                self.pirateArchives = {
                    "Files": ['OnlineFix.url', 'OnlineFix.ini', 'OnlineFix64.dll',
                              'winmm.dll', 'dlllist.txt', 'StubDRM64.dll'],
                    "Folders": []
                }
            case 'Palworld':
                self.pirateArchives = {
                    "Files": ['Palworld-backup.exe'],
                    "Folders": ['Engine-backup', 'Pal-backup']
                }
            case _:
                self.pirateArchives = {
                    "Files": [],
                    "Folders": []
                }
