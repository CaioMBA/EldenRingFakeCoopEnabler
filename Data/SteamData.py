import io,os, zipfile, requests, subprocess, time
from tqdm import tqdm
from Data.GoogleDriveData import GoogleDrive
from Data.WebDownloader import WebDownloader
from Services.UtilsService import Utils

class Steam():
    def InstallSteamCMD (self):
        if not os.path.exists("steamcmd"):
            os.makedirs("steamcmd")

        print("Installing SteamCMD...")
        return WebDownloader().DownloadFile("https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip",
                                            "steamcmd.zip",
                                            os.path.relpath("steamcmd"))


    def RunSteamCMDUpdateFunction(self, GameId: str, SteamGameName: str, DownloadPath: str, filePathCheck: str):
        if not os.path.exists("steamcmd"):
            self.InstallSteamCMD()
        SteamCMDPath = os.path.join(os.getcwd(), "steamcmd", "steamcmd.exe")

        CredentialArray = GoogleDrive().GetGoogleDriveSheetAsCsv('1zEglgAorcm5O_cI_-mlxDNL2i6dNrKrKbqDPlHGbzIQ')
        try:
            CredentialArray.extend(Utils().GetSecretAccounts())
        except Exception as e:
            print(f"It was not possible to get secret accounts, error: {e}")

        if (DownloadPath is None or DownloadPath == '' or
                not os.path.exists(DownloadPath) or not os.path.isdir(DownloadPath)):
            DownloadPath = Utils().get_steam_installation_directory()
            if DownloadPath is None:
                DownloadPath = os.path.expanduser('~'), 'Downloads'

        if not DownloadPath.endswith(SteamGameName):
            DownloadPath = os.path.join(DownloadPath, SteamGameName)

        fileToCheck = os.path.join(DownloadPath, filePathCheck)

        for Credential in CredentialArray:
            User = Credential['User']
            Password = Credential['Pass']
            GamesAvailable = Credential['Games'].split(';')
            if SteamGameName not in GamesAvailable:
                continue



            cmd = [
                SteamCMDPath,
                "+force_install_dir", DownloadPath,
                "+login", User, Password,
                "+app_update", GameId, "validate", "+quit"
            ]

            print('Trying to start download/update...')
            try:
                start_time = time.time()
                print(f'Progress {SteamGameName} download/update running... DO NOT CLOSE THE WINDOW!')
                print(f'THIS MIGHT TAKE A WHILE SO BE PATIENT! -> it will go to -> {DownloadPath}')

                try:
                    subprocess.run(cmd, check=True, shell=True)
                except Exception as e:
                    print(f"steamcmd closed without state 0, error: {e}")

                elapsed_time = time.time() - start_time
                minutes = int(elapsed_time // 60)
                seconds = int(elapsed_time % 60)

                print(f"Elapsed Time: {minutes:02d}:{seconds:02d}")
                if not os.path.exists(fileToCheck):
                    print(f"Failed to download {SteamGameName}")
                    continue
                os.rename(DownloadPath.replace(SteamGameName, SteamGameName.lower()), DownloadPath)
                Utils().DeleteSpecificDir(os.path.join(DownloadPath, 'steamapps'))
                Utils().DeleteSpecificDir(os.path.join(DownloadPath, '_CommonRedist'))
                print(f"{SteamGameName} Installation/Update Successful! At: {DownloadPath}")
                return DownloadPath
            except subprocess.CalledProcessError as e:
                print(f"Failed to download {SteamGameName}, error: {e}")
                return ''
        print(f"Failed to download {SteamGameName} it ran out of anonymous credentials!")
        return ''
