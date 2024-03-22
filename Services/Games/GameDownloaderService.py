import os.path

from Data.SteamData import Steam
from Data.GoogleDriveData import GoogleDrive
from Data.OneDriveData import OneDrive
from Data.MediaFireData import MediaFire
from Services.UtilsService import Utils
class GameDownloader:
    def DownloadGame(self, gameName:str, DownloadPath:str=''):
        gameSpecificsArray = GoogleDrive().GetGoogleDriveSheetAsCsv('1kQRBe_Ue6Si0RVD0SIWhCXzvCb0v-6bV0njAhaDp97k')
        gameSpecifics = next(filter(lambda obj: obj['GameName'] == gameName and obj['Active'] == '1',
                                    gameSpecificsArray),
                                    None)

        if gameSpecifics is None:
            Utils().clear_console()
            print('GAME NOT FOUND, COULD NOT DOWNLOAD/UPDATE IT')
            return None

        InterfaceResponse = None
        if gameSpecifics['Interface'] == 'Steam':
            InterfaceResponse = Steam().RunSteamCMDUpdateFunction(
                                                 gameSpecifics["SteamGameID"],
                                                 gameSpecifics["GameName"],
                                                 DownloadPath,
                                                 gameSpecifics["GameFilePathCheck"])

        if InterfaceResponse != None and InterfaceResponse != '' and gameName in ['ELDEN RING']:
            InterfaceResponse += r'\Game'

        return InterfaceResponse


    def SpaceWarDownloadOrUpdate(self, DownloadPath:str=''):
        return Steam().RunSteamCMDUpdateFunction("480",
                                                 "Spacewar",
                                                 DownloadPath,
                                                 'SteamworksExample.exe')


    def DownloadLinks(self, jsonDict:dict, gameName:str=''):
        print('Verifiyng and Downloading/Updating files...')
        Links = GoogleDrive().GetGoogleDriveSheetAsCsv('1gOa-GoZt4C5oUtMIHTqyBtxt4CMTK3Y6Qqr5sjrEWek')

        for linkObj in Links:
            if gameName != linkObj['Game']:
                continue
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