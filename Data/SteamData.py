import io,os, zipfile, requests, subprocess, time, sys, threading
from tqdm import tqdm
from Services.UtilsService import Utils
from Data.GoogleDriveData import GoogleDrive
from Services.UtilsService import Utils

class Steam():
    def InstallSteamCMD (self):
        if not os.path.exists("steamcmd"):
            os.makedirs("steamcmd")

        print("Installing SteamCMD...")
        response = requests.get("https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip", stream=True)

        if response.status_code == 200:
            with io.BytesIO() as zip_buffer:
                total_size = int(response.headers.get('content-length', 0))

                progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)

                for data in response.iter_content(chunk_size=1024):
                    progress_bar.update(len(data))
                    zip_buffer.write(data)

                progress_bar.close()

                zip_buffer.seek(0)

                with zipfile.ZipFile(zip_buffer, "r") as zip_ref:
                    zip_ref.extractall("steamcmd")

            print("SteamCMD installed successfully!")
        else:
            print("Failed to download SteamCMD")

    def RunSteamCMDUpdateFunction(self, GameId: str, SteamGameName: str, DownloadPath: str):
        if not os.path.exists("steamcmd"):
            self.InstallSteamCMD()
        SteamCMDPath = os.path.join(os.getcwd(), "steamcmd", "steamcmd.exe")

        CredentialArray = GoogleDrive().GetGoogleDriveSheetAsCsv('1zEglgAorcm5O_cI_-mlxDNL2i6dNrKrKbqDPlHGbzIQ')
        if DownloadPath is None or DownloadPath == '' or not os.path.exists(DownloadPath) or not os.path.isdir(
                DownloadPath):
            DownloadPath = Utils().get_steam_installation_directory()
            if DownloadPath is None:
                DownloadPath = os.path.expanduser('~'), 'Downloads'

            DownloadPath = os.path.join(DownloadPath, SteamGameName)

        for Credential in CredentialArray:
            User = Credential['User']
            Password = Credential['Pass']

            cmd = [
                SteamCMDPath,
                "+force_install_dir", DownloadPath,
                "+login", User, Password,
                "+app_update", GameId, "validate", "+quit"
            ]

            print('Trying to start download/update...')
            try:
                start_time = time.time()
                print(f'Progress running... {SteamGameName} download/update running DO NOT CLOSE THE WINDOW!')
                print(f'THIS MIGHT TAKE A WHILE SO BE PATIENT! -> it will go to -> {DownloadPath}')
                result = subprocess.run(cmd, check=True, shell=True, capture_output=True, text=True)
                elapsedtime = time.time() - start_time
                print(f"Elapsed Time: {int(elapsedtime // 60)}/{int(elapsedtime % 60)}")

                if 'Success! App' in result.stdout and 'fully installed' in result.stdout:
                    print(f"{SteamGameName} Installation/Update Successful!")
                else:
                    Utils().clear_console()
                    print(f"{SteamGameName} Installation/Update Failed!")
                    continue

                return DownloadPath
            except subprocess.CalledProcessError as e:
                print(f"Failed to download {SteamGameName}, error: {e}")
                return None
        return None
        # ANTIGO CÓDIGO PARA EXECUTAR COMO ADM
        # try:
        #     Utils().RunShellAsAdmin(SteamCMDPath, ' '.join(cmd))
        # except RuntimeError as e:
        #     print("Error:", e)
