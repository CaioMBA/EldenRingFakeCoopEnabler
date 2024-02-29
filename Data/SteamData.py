import io,os,zipfile,requests, subprocess, time
from tqdm import tqdm
from Services.UtilsService import Utils
from Data.GoogleDriveData import GoogleDrive

class Steam():
    def InstallSteamCMD(self):
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

    def RunSteamCMDUpdateFunction(self, GameId:str, SteamGameName:str):
        if not os.path.exists("steamcmd"):
            self.InstallSteamCMD()

        SteamCMDPath = os.path.join(os.getcwd(), "steamcmd", "steamcmd.exe")

        CredentialArray = GoogleDrive().GetGoogleDriveSheetAsCsv('1zEglgAorcm5O_cI_-mlxDNL2i6dNrKrKbqDPlHGbzIQ')
        for Credential in CredentialArray:
            User = Credential['User']
            Password = Credential['Pass']
            download_path = Utils().get_steam_installation_directory()
            if download_path is None:
                download_path = os.path.expanduser('~'), 'Downloads'

            download_path = os.path.join(download_path, SteamGameName)


            cmd = [
                SteamCMDPath,
                "+force_install_dir", download_path,
                "+login", User, Password,
                "+app_update", GameId, "validate", "+quit"
            ]

            print('Trying to start download/update...')
            try:
                start_time = time.time()
                subprocess.run(cmd, check=True, shell=True)
                elapsedtime = start_time - time.time()
                if elapsedtime < 30:
                    pass
                return download_path
            except subprocess.CalledProcessError as e:
                print("Failed to download Elden Ring, error:", e)
                return None
        return None
        # ANTIGO CÓDIGO PARA EXECUTAR COMO ADM
        # try:
        #     Utils().RunShellAsAdmin(SteamCMDPath, ' '.join(cmd))
        # except RuntimeError as e:
        #     print("Error:", e)