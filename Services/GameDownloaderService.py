import os.path

from Data.SteamData import Steam
from Data.GoogleDriveData import GoogleDrive
from Data.OneDriveData import OneDrive
from Data.MediaFireData import MediaFire
from Services.UtilsService import Utils
class GameDownloader:
    def EldenRingDownloadOrUpdate(self, DownloadPath: str=''):
        return Steam().RunSteamCMDUpdateFunction("1245620",
                                                 "ELDEN RING",
                                                 DownloadPath,
                                                 r'Game\eldenring.exe')
    def SpaceWarDownloadOrUpdate(self, DownloadPath:str=''):
        return Steam().RunSteamCMDUpdateFunction("480",
                                                 "Spacewar",
                                                 DownloadPath,
                                                 'SteamworksExample.exe')
    def PalworldDownloadOrUpdate(self, DownloadPath:str=''):
        return Steam().RunSteamCMDUpdateFunction("1623730",
                                                 "Palworld",
                                                 DownloadPath,
                                                 'Palworld.exe')
    def EnshroudedDownloadOrUpdate(self, DownloadPath:str=''):
        return Steam().RunSteamCMDUpdateFunction("1203620",
                                                 "Enshrouded",
                                                 DownloadPath,
                                                 'enshrouded.exe')

    def LiesOfPDownloadOrUpdate(self, DownloadPath:str=''):
        return Steam().RunSteamCMDUpdateFunction("1627720",
                                                 "Lies of P",
                                                 DownloadPath,
                                                 'LOP.exe')
    def SekiroDownloadOrUpdate(self, DownloadPath:str=''):
        return Steam().RunSteamCMDUpdateFunction("814380",
                                                 "Sekiro",
                                                 DownloadPath,
                                                 'sekiro.exe')

    def AWayOutDownloadOrUpdate(self, DownloadPath:str=''):
        return Steam().RunSteamCMDUpdateFunction("1222700",
                                                 "AWayOut",
                                                 DownloadPath,
                                                 r'installScript.vdf')
    def  ItTakesTwoDownloadOrUpdate(self, DownloadPath:str=''):
        return Steam().RunSteamCMDUpdateFunction("1426210",
                                                 "ItTakesTwo",
                                                 DownloadPath,
                                                 r'installScript.vdf')
    def SonsOfTheForestDownloadOrUpdate(self, DownloadPath:str=''):
        return Steam().RunSteamCMDUpdateFunction("1326470",
                                                 "Sons Of The Forest",
                                                 DownloadPath,
                                                 r'SonsOfTheForest.exe')
    def LordsOfTheFallenDownloadOrUpdate(self, DownloadPath:str=''):
        return Steam().RunSteamCMDUpdateFunction("1501750",
                                                 "Lords of the Fallen",
                                                 DownloadPath,
                                                 r'LOTF2.exe')

    def DownloadLinks(self, jsonDict:dict):
        print('Verifiyng and Downloading/Updating files...')
        Links = GoogleDrive().GetGoogleDriveSheetAsCsv('1gOa-GoZt4C5oUtMIHTqyBtxt4CMTK3Y6Qqr5sjrEWek')

        for linkObj in Links:
            if linkObj['Game'] not in jsonDict:
                continue
            if linkObj['JsonSubKey'] not in jsonDict[linkObj['Game']]:
                continue
            if jsonDict[linkObj['Game']][linkObj['JsonSubKey']] != '':
                continue
            if linkObj['Origin'] == 'MediaFire':
                shortPath = MediaFire().DownloadFile(linkObj['Links'], linkObj['fileName'])
            elif linkObj['Origin'] == 'GoogleDrive':
                shortPath = GoogleDrive().DownloadGoogleDriveFile(linkObj['Links'], linkObj['fileName'])
            elif linkObj['Origin'] == 'OneDrive':
                shortPath = OneDrive().DownloadFile(linkObj['Links'], linkObj['fileName'])
            shortPath = str(os.path.join(shortPath, linkObj['insideFile']))
            Utils().updateJsonConfig(key=linkObj['Game'], subkey=linkObj['JsonSubKey'], value=shortPath)
            print(f'[{linkObj["Game"]} <-> {linkObj["JsonSubKey"]}] -> {shortPath}')
        print('All files are up to date')