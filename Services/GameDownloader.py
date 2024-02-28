from Services.SteamService import Steam
class GameDownloader:
    def EldenRingDownloadOrUpdate(self):
        return Steam().RunSteamCMDUpdateFunction("1245620", "ELDEN RING")
    def SpaceWarDownloadOrUpdate(self):
        return Steam().RunSteamCMDUpdateFunction("480", "Spacewar")