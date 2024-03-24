import os.path

from Data.SteamData import Steam
from Data.GoogleDriveData import GoogleDrive
from Data.OneDriveData import OneDrive
from Data.MediaFireData import MediaFire
from Services.UtilsService import Utils
from Services.Configs.AppConfigService import AppConfigService


class GameDownloader:
    def DownloadGame(self, gameName: str, DownloadPath: str = '') -> str:
        gameSpecificsArray = GoogleDrive().GetGoogleDriveSheetAsCsv('1kQRBe_Ue6Si0RVD0SIWhCXzvCb0v-6bV0njAhaDp97k')
        if not isinstance(gameSpecificsArray, list):
            Utils().clear_console()
            print(f'It was not possible to reach the game list. Try again later.')
            return ''

        gameSpecifics = next(filter(lambda obj: obj['GameName'] == gameName and obj['Active'] == '1',
                                    gameSpecificsArray), None)

        if gameSpecifics is None:
            Utils().clear_console()
            print(f'GAME {gameName} NOT FOUND, COULD NOT DOWNLOAD/UPDATE IT')
            return ''

        self.ShowGameValues(gameSpecifics)
        InterfaceResponse = None
        if gameSpecifics['Interface'] == 'Steam':
            InterfaceResponse = Steam().RunSteamCMDUpdateFunction(
                gameSpecifics["SteamGameID"],
                gameSpecifics["GameName"],
                DownloadPath,
                gameSpecifics["GameFilePathCheck"])

        if InterfaceResponse is not None and InterfaceResponse != '' and gameName == 'ELDEN RING':
            InterfaceResponse += r'\Game'

        return InterfaceResponse

    def SpaceWarDownloadOrUpdate(self, DownloadPath: str = '') -> str:
        return Steam().RunSteamCMDUpdateFunction("480",
                                                 "Spacewar",
                                                 DownloadPath,
                                                 'SteamworksExample.exe')

    def ShowGameValues(self, gameSpecifics: dict) -> None:
        try:
            print('[ GAME VALUES ]')
            print(f'Steam ID: {gameSpecifics["SteamGameID"]}')
            print(f'Game Name: {gameSpecifics["GameName"]}')
            print(f'File Path Check: {gameSpecifics["GameFilePathCheck"]}')
            print(f'Interface: {gameSpecifics["Interface"]}')
        except Exception as e:
            print(f'Error while trying to show game values, Error: {e}')

    def DownloadLinks(self, jsonDict: dict, gameName: str = '') -> None:
        print(f'Verifiyng and Downloading/Updating files for {gameName}...')
        Links = GoogleDrive().GetGoogleDriveSheetAsCsv('1gOa-GoZt4C5oUtMIHTqyBtxt4CMTK3Y6Qqr5sjrEWek')
        if not isinstance(Links, list) or len(Links) == 0:
            Utils().clear_console()
            print(f'It was not possible to reach the links list. Try again later.')
            return
        listDownloaded = []
        for linkObj in Links:
            if (gameName != linkObj['Game'] or
                    linkObj['JsonSubKey'] not in jsonDict[gameName] or
                    linkObj['Game'] not in jsonDict or
                    jsonDict[gameName][linkObj['JsonSubKey']] != ''):
                continue
            shortPath = ''
            print(f'Downloading {gameName} -> {linkObj["JsonSubKey"]}...')
            match linkObj['Origin']:
                case 'MediaFire':
                    shortPath = MediaFire().DownloadFile(linkObj['Links'], linkObj['fileName'])
                case 'GoogleDrive':
                    shortPath = GoogleDrive().DownloadGoogleDriveFile(linkObj['Links'], linkObj['fileName'])
                case 'OneDrive':
                    shortPath = OneDrive().DownloadFile(linkObj['Links'], linkObj['fileName'])

            shortPath = str(os.path.join(shortPath, linkObj['insideFile']))
            AppConfigService().UpdateAppConfig(key=linkObj['Game'], subkey=linkObj['JsonSubKey'], value=shortPath)
            listDownloaded.append(f'[{linkObj["Game"]} <-> {linkObj["JsonSubKey"]}] -> {shortPath}')
        print('All files are up to date')
        print(f"List of Downloads and it's Paths: {listDownloaded}")
