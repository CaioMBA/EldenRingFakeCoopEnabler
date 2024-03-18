import os, shutil, configparser
from Services.UtilsService import Utils
from Services.GameDownloaderService import GameDownloader

class ItTakesTwo():
    def __init__(self, GamePath, fixPath, EnginePath, ModsPath, pirateArchives:dict):
        if GamePath == '' or GamePath is None:
            path = GameDownloader().ItTakesTwoDownloadOrUpdate()
            Utils().updateJsonConfig('ItTakesTwo', 'GamePath', path)
            print('FOR THE GAME TO WORK, YOU NEED TO RESTART THIS PROGRAM')
            return

        self.GamePath = GamePath
        self.FixPath = fixPath
        self.ModEnginePath = EnginePath
        #self.Mods = Mods(ModsPath, self.ModEnginePath, self.GamePath)
        self.PirateArchives = pirateArchives


    def EnablePirateGame(self):
        print("Enabling play Pirate Game")
        if self.FixPath == '' or not os.path.exists(self.FixPath):
            print(f"The path '{self.FixPath}' does not exist.")
            return
        self.BackUpGameFolder()
        try:
            for root, dirs, files in os.walk(self.FixPath):

                relative_path = str(os.path.relpath(root, self.FixPath))
                destination_root = os.path.join(self.GamePath, relative_path)

                os.makedirs(destination_root, exist_ok=True)

                for fileName in files:
                    sourceFilePath = str(os.path.join(root, fileName))
                    destinationFilePath = str(os.path.join(destination_root, fileName))

                    if os.path.exists(destinationFilePath):
                        if os.path.isdir(destinationFilePath):
                            shutil.rmtree(destinationFilePath)
                        else:
                            os.remove(destinationFilePath)

                    shutil.copy2(sourceFilePath, destinationFilePath)
            Utils().clear_console()
            print("Pirate Game enabled!")

        except Exception as e:
            print(f"Error: {e}")

    def BackUpGameFolder(self):
        print('Backing up GamePath folder...')
        if not os.path.exists(os.path.join(self.GamePath, 'Nuts_backup')):
            shutil.copytree(os.path.join(self.GamePath, 'Nuts'),
                            os.path.join(self.GamePath, 'Nuts_backup'))

    def RestoreGameFolder(self):
        print('Restoring GamePath folder...')
        if os.path.exists(os.path.join(self.GamePath, 'Nuts_backup')):
            if os.path.exists(os.path.join(self.GamePath, 'Nuts')):
                shutil.rmtree(os.path.join(self.GamePath, 'Nuts'))
            os.rename(os.path.join(self.GamePath, 'Nuts_backup'),
                      os.path.join(self.GamePath, 'Nuts'))

    def DisablePirateGame(self):
        print("Disabling play Pirate Game")
        self.RestoreGameFolder()
        print("Pirate Game disabled!")