import requests, os
from tqdm import tqdm
from Services.UtilsService import Utils
class WebDownloader():
    def DownloadFile(self, download_url:str, fileName:str, finalDir:str = '') -> str:
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
            if finalDir == '':
                finalDir = Utils().GetDocumentsFolderPath()
                finalDir = Utils().CheckIfPathExists(finalDir, 'Multi-Enabler Downloads')
            if fileName.endswith('.zip') or fileName.endswith('.rar'):
                return Utils().DeCompress(fileName, finalDir)
            return filepath

        else:
            print(f"Failed to download. Status code: {response.status_code}")
            return ""