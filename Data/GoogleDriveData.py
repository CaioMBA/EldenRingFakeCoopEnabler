import requests
from Services.UtilsService import Utils
from Data.WebDownloader import WebDownloader

class GoogleDrive():
    def DownloadGoogleDriveFile(self, Id: str, fileName:str):
        print(f'INICIANDO DOWNLOAD ARQUIVO! => {fileName} !')
        download_url = f'https://drive.google.com/uc?export=download&id={Id}'

        return WebDownloader().DownloadFile(download_url, fileName)


    def GetGoogleDriveSheetAsCsv(self, Id: str):
        doc_url = f'https://docs.google.com/spreadsheets/d/{Id}/export?format=csv'

        response = requests.get(doc_url, stream=True)
        if response.status_code == 200:
            return Utils().TransformCsvByteStringToDict(response.content)
        else:
            print(f"Failed to download. Status code: {response.status_code}")
            return []