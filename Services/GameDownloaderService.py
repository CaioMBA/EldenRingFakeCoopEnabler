import os.path

from Data.SteamData import Steam
from Data.GoogleDriveData import GoogleDrive
from Data.OneDriveData import OneDrive
from Data.GitHubData import GitHub
from Services.UtilsService import Utils
class GameDownloader:
    def EldenRingDownloadOrUpdate(self):
        return Steam().RunSteamCMDUpdateFunction("1245620", "ELDEN RING", '')
    def SpaceWarDownloadOrUpdate(self):
        return Steam().RunSteamCMDUpdateFunction("480", "Spacewar", '')

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
                shortPath = GitHub().DownloadAsset(linkObj['Links'], linkObj['ID'])
                shortPath += linkObj['FinalDir']
            elif linkObj['Origin'] == 'GoogleDrive':
                shortPath = GoogleDrive().DownloadGoogleDriveFile(linkObj['Links'], linkObj['ID'])
            elif linkObj['Origin'] == 'OneDrive':
                shortPath = OneDrive().DownloadFile(linkObj['Links'], linkObj['ID'])
            shortPath = str(os.path.join(shortPath, linkObj['FinalDir']))
            Utils().updateJsonConfig(key=linkObj['Game'], subkey=linkObj['JsonSubKey'], value=shortPath)
            print(f'[{linkObj["Game"]} <-> {linkObj["JsonSubKey"]}] -> {shortPath}')