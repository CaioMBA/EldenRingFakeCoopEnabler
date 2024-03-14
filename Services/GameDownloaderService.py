import os.path

from Data.SteamData import Steam
from Data.GoogleDriveData import GoogleDrive
from Data.OneDriveData import OneDrive
from Data.GitHubData import GitHub
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

    def DownloadLinks(self, jsonDict:dict):
        Links = GoogleDrive().GetGoogleDriveSheetAsCsv('1gOa-GoZt4C5oUtMIHTqyBtxt4CMTK3Y6Qqr5sjrEWek')
        for linkObj in Links:
            if linkObj['Game'] not in jsonDict:
                continue
            if linkObj['JsonSubKey'] not in jsonDict[linkObj['Game']]:
                continue
            if jsonDict[linkObj['Game']][linkObj['JsonSubKey']] != '':
                continue
            if linkObj['Origin'] == 'GitHub':
                shortPath = GitHub().DownloadAsset(linkObj['Links'], linkObj['fileName'])
                shortPath += linkObj['FinalDir']
            elif linkObj['Origin'] == 'GoogleDrive':
                shortPath = GoogleDrive().DownloadGoogleDriveFile(linkObj['Links'], linkObj['fileName'])
            elif linkObj['Origin'] == 'OneDrive':
                shortPath = OneDrive().DownloadFile(linkObj['Links'], linkObj['fileName'])
            shortPath = str(os.path.join(shortPath, linkObj['insideFile']))
            Utils().updateJsonConfig(key=linkObj['Game'], subkey=linkObj['JsonSubKey'], value=shortPath)
            print(f'[{linkObj["Game"]} <-> {linkObj["JsonSubKey"]}] -> {shortPath}')