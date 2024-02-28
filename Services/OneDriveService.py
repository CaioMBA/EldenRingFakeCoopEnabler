import requests, os
from tqdm import tqdm
from Services.UtilsService import Utils
class OneDrive():
    def GetDirectLinkFromOnDriveAPI(self, SharedLink:str):
        api_url = "https://api.onedrive.com/v1.0/shares/{0}/root/content".format(SharedLink.split("/")[-1])
        response = requests.head(api_url, allow_redirects=True)
        if response.status_code == 200:
            return response.url
        else:
            print(f"Failed to fetch direct download link. Status code: {response.status_code}")
            return None

    def DownloadFile(self, SharedLink:str, file_name:str):
        print(f'Iniciando download do arquivo => {file_name} !')
        direct_download_link = self.GetDirectLinkFromOnDriveAPI(SharedLink)
        response = requests.get(direct_download_link, stream=True)
        if response.status_code == 200:
            file_size = int(response.headers.get('content-length', 0))
            with open(file_name, 'wb') as f:
                with tqdm(total=file_size, unit='B', unit_scale=True, desc='Downloading') as progress_bar:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            progress_bar.update(len(chunk))

            filepath = os.path.relpath(file_name)
            if file_name.endswith('.zip'):
                return Utils().DeCompress(file_name, Utils().CheckIfOneDriveExists('Documents'))
            return filepath
        else:
            print(f"Failed to download file. Status code: {response.status_code}")
            return ""