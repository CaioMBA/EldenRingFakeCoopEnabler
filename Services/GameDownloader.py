from Services.SteamService import Steam
class GameDownloader:
    def EldenRingDownloadOrUpdate(self):
        Steam().RunSteamCMDUpdateFunction("1245620", "ELDEN RING")
    def SpaceWarDownloadOrUpdate(self):
        Steam().RunSteamCMDUpdateFunction("480", "Spacewar")