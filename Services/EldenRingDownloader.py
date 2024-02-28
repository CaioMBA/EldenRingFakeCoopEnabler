import io,os,zipfile,requests, subprocess, ctypes
from tqdm import tqdm
from ctypes import wintypes
from Services.UtilsService import Utils
class DownloadAndInstallEldenRing():
    def run_as_admin(self, command, params=None):
        shell32 = ctypes.windll.shell32
        if params is None:
            params = ''
        show_cmd = wintypes.INT(1)
        wintypes.HINSTANCE(shell32.ShellExecuteW(None, 'runas', command, params, None, show_cmd))

    def install_steamcmd(self):
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

    def run_steamcmd_command(self):
        if not os.path.exists("steamcmd"):
            self.install_steamcmd()

        SteamCMDPath = os.path.join(os.getcwd(), "steamcmd", "steamcmd.exe")

        user = "qq270606505"
        password = "SNSD0O123456789"
        EldenRingGameID = "1245620"
        download_path = os.path.join(Utils().get_steam_installation_directory(), 'ELDEN RING')
        if download_path is None:
            download_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'ELDEN RING')



        cmd = [
            SteamCMDPath,
            "+force_install_dir", download_path,
            "+login", user, password,
            "+app_update", EldenRingGameID, "validate", "+quit"
        ]

        print('Starting download...')
        try:
            subprocess.run(cmd, check=True, shell=True)
            return download_path
        except subprocess.CalledProcessError as e:
            print("Failed to download Elden Ring, error:", e)
            return None
        #ANTIGO CÓDIGO PARA EXECUTAR COMO ADM
        # try:
        #     self.run_as_admin(SteamCMDPath, ' '.join(cmd))
        # except RuntimeError as e:
        #     print("Error:", e)

    def download_elden_ring(self):
        try:
            self.run_steamcmd_command()
        except Exception as e:
            print(f'Failed to download Elden Ring, erro: {e}')