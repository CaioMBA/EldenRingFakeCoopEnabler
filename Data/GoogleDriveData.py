import requests, os
from Services.UtilsService import Utils
from tqdm import tqdm

class GoogleDrive():
    def DownloadGoogleDriveFile(self, Id: str, fileName:str):
        print(f'INICIANDO DOWNLOAD ARQUIVO! => {fileName} !')
        download_url = f'https://drive.google.com/uc?export=download&id={Id}'

        response = requests.get(download_url, stream=True)

        if response.status_code == 200:
            file_size = int(response.headers.get('content-length', 0))

            with open(fileName, 'wb') as f:
                with tqdm(total=file_size, unit='B', unit_scale=True, desc='Downloading') as progress_bar:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            progress_bar.update(len(chunk))
            filepath = os.path.relpath(fileName)
            if fileName.endswith('.zip'):
                return Utils().DeCompress(fileName, Utils().CheckIfOneDriveExists('Documents'))
            return filepath

        else:
            print(f"Failed to download. Status code: {response.status_code}")
            return ""

    def GetGoogleDriveJsonDocument(self, Id: str):
        doc_url = f'https://docs.google.com/document/d/{Id}/pub'

        response = requests.get(doc_url, stream=True)
        if response.status_code == 200:
            return Utils().TransformJsonToDict(response.text)
        else:
            print(f"Failed to download. Status code: {response.status_code}")
            return {}

if __name__ == '__main__':
    print(GoogleDrive().GetGoogleDriveJsonDocument('1vy3cUs7L7AQkq8LVsvR8pMUo6u3WpKebFX3TMR6fJOw'))