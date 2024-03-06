from Services.UtilsService import Utils
from tqdm import tqdm
import requests, os
class GitHub():
    def DownloadAsset(self, url, fileName):
        response = requests.get(url)

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