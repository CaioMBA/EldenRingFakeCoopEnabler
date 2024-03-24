import requests
from bs4 import BeautifulSoup
from Data.WebDownloader import WebDownloader
class MediaFire():
    def ExtractMediaFireDirectLink(self, url) -> str:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        download_button = soup.find('a', {'aria-label': 'Download file'})
        if download_button:
            return download_button['href']
        else:
            return ''

    def DownloadFile(self, SharedUrl, fileName) -> str:
        direct_download_link = self.ExtractMediaFireDirectLink(SharedUrl)
        if not direct_download_link:
            print("Failed to extract direct download link.")
            return ""
        return WebDownloader().DownloadFile(direct_download_link, fileName)