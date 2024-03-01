from Data.SteamData import Steam
from Data.GoogleDriveData import GoogleDrive
from Data.OneDriveData import OneDrive
class GameDownloader:
    def EldenRingDownloadOrUpdate(self):
        return Steam().RunSteamCMDUpdateFunction("1245620", "ELDEN RING")
    def SpaceWarDownloadOrUpdate(self):
        return Steam().RunSteamCMDUpdateFunction("480", "Spacewar")

    def DownloadOnlineFix(self):
        shortPath = GoogleDrive().DownloadGoogleDriveFile('1MbN7kdGujji0rkDejIfaRD6_BcBfprb0', 'EldenRing_FIX_PIRATE_ORIGINAL.zip')
        shortPath += r'\EldenRing_FIX_PIRATE_ORIGINAL'
        return shortPath

    def DownloadPT_BRDubbing(self):
        shortPath = OneDrive().DownloadFile('https://1drv.ms/u/s!Au9PHb822TTUpP1rGwnHbRpERa682Q','EldenRingDubPT-BR.zip')
        shortPath += r'\EldenRingDubPT-BR'
        return shortPath