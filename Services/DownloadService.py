import requests, os, zipfile
from tqdm import tqdm
from Services.JsonServices import JsonServices

class DownloadAndUnzip():
    def download_google_drive_file(self, Id: str):
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

        else:
            print(f"Failed to download. Status code: {response.status_code}")

    def unzipFile(self, filename:str):
        DocumentRoot = os.path.expanduser(r'~\Documents')
        if os.path.exists(os.path.expanduser(r'~\OneDrive\Documents')):
            DocumentRoot = os.path.expanduser(r'~\OneDrive\Documents')

        with zipfile.ZipFile('downloaded_file.zip', 'r') as zip_ref:
            file_count = len(zip_ref.infolist())
            with tqdm(total=file_count) as pbar:
                for file in zip_ref.infolist():
                    zip_ref.extract(file, DocumentRoot)
                    pbar.update(1)

        os.remove('downloaded_file.zip')
        PathResponse = os.path.join(DocumentRoot, filename)
        keyJson = ''
        match filename.upper():
            case 'ELDENRING_FIX_PIRATE_ORIGINAL':
                keyJson = 'EldenRingFixPath'
            case 'ELDENRINGDUBPT-BR':
                keyJson = 'EldenRingDubPath'
        JsonServices().updateJsonConfig(keyJson, PathResponse)
        print(f'ARQUIVO DESCOMPACTADO!')
        return PathResponse