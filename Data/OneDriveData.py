import requests
from Data.WebDownloader import WebDownloader
class OneDrive():
    def GetDirectLinkFromOnDriveAPI(self, SharedLink:str):
        api_url = f"https://api.onedrive.com/v1.0/shares/{SharedLink.split("/")[-1]}/root/content"
        response = requests.head(api_url, allow_redirects=True)
        if response.status_code == 200:
            return response.url
        else:
            print(f"Failed to fetch direct download link. Status code: {response.status_code}")
            return None

    def DownloadFile(self, SharedLink:str, file_name:str):
        print(f'Iniciando download do arquivo => {file_name} !')
        direct_download_link = self.GetDirectLinkFromOnDriveAPI(SharedLink)

        return WebDownloader().DownloadFile(direct_download_link, file_name)
