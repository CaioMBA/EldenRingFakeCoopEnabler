import os.path

from Data.SteamData import Steam
from Data.GoogleDriveData import GoogleDrive
from Data.OneDriveData import OneDrive
from Data.MediaFireData import MediaFire
from Services.UtilsService import Utils
class GameDownloader:
    def DownloadGame(self, gameName:str, DownloadPath:str=''):
        gameSpecifics = {}
        match gameName:
            case "ELDEN RING":
                gameSpecifics={
                    "SteamGameName": "ELDEN RING",
                    "SteamGameID": "1245620",
                    "FilePathCheck": r'Game\eldenring.exe',
                    "DownloadPath": DownloadPath
                }
            case "Spacewar":
                gameSpecifics = {
                    "SteamGameName": "Spacewar",
                    "SteamGameID": "480",
                    "FilePathCheck": r'SteamworksExample.exe',
                    "DownloadPath": DownloadPath
                }
            case "Palworld":
                gameSpecifics = {
                    "SteamGameName": "Palworld",
                    "SteamGameID": "1623730",
                    "FilePathCheck": r'Palworld.exe',
                    "DownloadPath": DownloadPath
                }
            case "Enshrouded":
                gameSpecifics = {
                    "SteamGameName": "Enshrouded",
                    "SteamGameID": "1203620",
                    "FilePathCheck": r'enshrouded.exe',
                    "DownloadPath": DownloadPath
                }
            case "Lies of P":
                gameSpecifics = {
                    "SteamGameName": "Lies of P",
                    "SteamGameID": "1627720",
                    "FilePathCheck": r'LOP.exe',
                    "DownloadPath": DownloadPath
                }
            case "Sekiro":
                gameSpecifics = {
                    "SteamGameName": "Sekiro",
                    "SteamGameID": "814380",
                    "FilePathCheck": r'sekiro.exe',
                    "DownloadPath": DownloadPath
                }
            case "AWayOut":
                gameSpecifics = {
                    "SteamGameName": "AWayOut",
                    "SteamGameID": "1222700",
                    "FilePathCheck": r'installScript.vdf',
                    "DownloadPath": DownloadPath
                }
            case "ItTakesTwo":
                gameSpecifics = {
                    "SteamGameName": "ItTakesTwo",
                    "SteamGameID": "1426210",
                    "FilePathCheck": r'installScript.vdf',
                    "DownloadPath": DownloadPath
                }
            case "SonsOfTheForest":
                gameSpecifics = {
                    "SteamGameName": "Sons Of The Forest",
                    "SteamGameID": "1326470",
                    "FilePathCheck": r'SonsOfTheForest.exe',
                    "DownloadPath": DownloadPath
                }
            case "LordsOfTheFallen":
                gameSpecifics = {
                    "SteamGameName": "Lords of the Fallen",
                    "SteamGameID": "1501750",
                    "FilePathCheck": r'LOTF2.exe',
                    "DownloadPath": DownloadPath
                }
            case _:
                Utils().clear_console()
                print('GAME NOT FOUND, COULD NOT DOWNLOAD/UPDATE IT')
                return None
        return Steam().RunSteamCMDUpdateFunction(gameSpecifics["SteamGameID"],
                                                 gameSpecifics["SteamGameName"],
                                                 gameSpecifics["DownloadPath"],
                                                 gameSpecifics["FilePathCheck"])


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