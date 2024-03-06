import os, shutil, configparser, toml
from Services.UtilsService import Utils
class Mods():
    def __init__(self, MainModsPath:str, EldenRingGamePath:str):
        self.EldenRingGamePath = EldenRingGamePath
        self.EldenRingDubPath = os.path.join(MainModsPath, 'EldenRingDubPT-BR')

    def CheckIfDubIsEnabled(self):
        for root, dirs, files in os.walk(self.EldenRingGamePath):
            for dir in dirs:
                if dir == 'movie_backup':
                    return True
        return False
    def EnableDub(self):
        if self.EldenRingDubPath == '' or not os.path.exists(self.EldenRingDubPath):
            print(f"The path '{self.EldenRingDubPath}' does not exist.")
            return

        print('Enabling Brazilian-Portuguese Dubbing')
        self.BackUpMovieFolder()

        try:
            for root, dirs, files in os.walk(self.EldenRingDubPath):

                relative_path = os.path.relpath(root, self.EldenRingDubPath)
                destination_root = os.path.join(self.EldenRingGamePath, relative_path)

                os.makedirs(destination_root, exist_ok=True)

                for fileName in files:
                    sourceFilePath = os.path.join(root, fileName)
                    destinationFilePath = os.path.join(destination_root, fileName)

                    if os.path.exists(destinationFilePath):
                        if os.path.isdir(destinationFilePath):
                            shutil.rmtree(destinationFilePath)
                        else:
                            os.remove(destinationFilePath)

                    shutil.copy2(sourceFilePath, destinationFilePath)
            Utils().clear_console()
            print('Brazilian-Portuguese dubbing enabled!')
        except Exception as e:
            print(f"Error: {e}")
    def BackUpMovieFolder(self):
        backup_name = 'movie_backup'
        backup_path = os.path.join(self.EldenRingGamePath, backup_name)
        try:
            shutil.copytree(os.path.join(self.EldenRingGamePath, 'movie'), backup_path)
            print(f'Backup successful. Folder "movie" backed up to "{backup_path}".')
        except Exception as e:
            print(f"Error: {e}")
    def DisableDub(self):
        print("Disabling Brazilian-Portuguese Dubbing")
        backup_path = os.path.join(self.EldenRingGamePath, 'movie_backup')
        for root, dirs, files in os.walk(self.EldenRingGamePath):
            for fileName in files:
                if str(fileName).lower() in self.DubArchives['Files']:
                    os.remove(os.path.join(root,fileName))
            for dirName in dirs:
                if str(dirName).lower() in self.DubArchives['Folders']:
                    if not os.path.exists(backup_path) and dirName == 'movie':
                        continue
                    shutil.rmtree(os.path.join(root, dirName))
        try:
            shutil.copytree(backup_path, os.path.join(self.EldenRingGamePath, 'movie'))
            shutil.rmtree(backup_path)
            Utils().clear_console()
            print("Brazilian-Portuguese Dubbing disabled!")
        except Exception as e:
            print(f"Warning: {e}")

    def SetModEngineToml(self):
        tomlPath = os.path.join(self.EldenRingDubPath, 'config_eldenring.toml')
        with open(tomlPath, 'r') as file:
            data = toml.load(file)
        if os.path.exists(os.path.join(self.EldenRingGamePath, 'SeamlessCoop')) and not os.path.exists(os.path.join(self.EldenRingGamePath, 'winmm.dll')):
            data['modengine']['external_dlls'] = [r'SeamlessCoop\elden_ring_seamless_coop.dll']
        else:
            data['modengine']['external_dlls'] = []
        with open(tomlPath, 'w') as file:
            toml.dump(data, file)