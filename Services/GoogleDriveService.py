import requests, os
from Services.UtilsService import Utils
from tqdm import tqdm

class GoogleDrive():
    def DownloadGoogleDriveFile(self, Id: str):
        print(f'INICIANDO DOWNLOAD ARQUIVO! id:{Id}')
        download_url = f'https://drive.google.com/uc?export=download&id={Id}'

        response = requests.get(download_url, stream=True)

        if response.status_code == 200:
            file_size = int(response.headers.get('content-length', 0))

            with open('downloaded_file.zip', 'wb') as f:
                with tqdm(total=file_size, unit='B', unit_scale=True, desc='Downloading') as progress_bar:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            progress_bar.update(len(chunk))
            return Utils().DeCompress('downloaded_file.zip', Utils().CheckIfOneDriveExists('Documents'))

        else:
            print(f"Failed to download. Status code: {response.status_code}")
            return ""