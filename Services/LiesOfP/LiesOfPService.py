import os, shutil, configparser
from Services.UtilsService import Utils
from Services.GameDownloaderService import GameDownloader
class LiesOfP():
    def __init__(self, GamePath, fixPath, EnginePath, ModsPath, pirateArchives:dict):
        if GamePath == '' or GamePath is None:
            path = GameDownloader().LiesOfPDownloadOrUpdate()
            Utils().updateJsonConfig('Lies of P', 'GamePath', path)
            print('FOR THE GAME TO WORK, YOU NEED TO RESTART THIS PROGRAM')
            return

        self.GamePath = GamePath
        self.FixPath = fixPath
        self.ModEnginePath = EnginePath
        #self.Mods = Mods(ModsPath, self.EldenRingModEnginePath, self.EldenRingGamePath)
        self.PirateArchives = pirateArchives

    def EnablePirateGame(self):
        print("Enabling play Pirate Game")
        if self.FixPath == '' or not os.path.exists(self.FixPath):
            print(f"The path '{self.FixPath}' does not exist.")
            return
        self.BackUpEngineFolder()
        try:
            for root, dirs, files in os.walk(self.FixPath):

                relative_path = str(os.path.relpath(root, self.FixPath))
                destination_root = os.path.join(self.GamePath, relative_path)

                os.makedirs(destination_root, exist_ok=True)

                for fileName in files:
                    sourceFilePath = str(os.path.join(root, fileName))
                    destinationFilePath = str(os.path.join(destination_root, fileName))

                    if os.path.exists(destinationFilePath):
                        continue

                    shutil.copy2(sourceFilePath, destinationFilePath)
            Utils().clear_console()
            print("Pirate Game CO-OP enabled!")

        except Exception as e:
            print(f"Error: {e}")

    def BackUpEngineFolder(self):
        print('Backing up GamePath folder...')
        if not os.path.exists(os.path.join(self.GamePath, 'Engine_backup')):
            shutil.copytree(os.path.join(self.GamePath, 'Engine'),
                            os.path.join(self.GamePath, 'Engine_backup'))

    def RestoreEngineFolder(self):
        if os.path.exists(os.path.join(self.GamePath, 'Engine_backup')):
            if os.path.exists(os.path.join(self.GamePath, 'Engine')):
                shutil.rmtree(os.path.join(self.GamePath, 'Engine'))
            os.rename(os.path.join(self.GamePath, 'Engine_backup'),
                      os.path.join(self.GamePath, 'Engine'))

    def DisablePirateGame(self):
        self.RestoreEngineFolder()
