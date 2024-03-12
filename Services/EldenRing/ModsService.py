import os, shutil, configparser, toml
from Services.UtilsService import Utils
class Mods():
    def __init__(self, MainModsPath:str, EnginePath: str, EldenRingGamePath:str):
        self.EldenRingGamePath = EldenRingGamePath
        self.EldenRingEnginePath = EnginePath
        self.EldenRingCoopPath = os.path.join(MainModsPath, 'EldenRing_CO-OP')
        self.EldenRingDisableSharpenFilter = os.path.join(MainModsPath, 'EldenRing_DisableSharpenFilter')
        self.EldenRingDubPath = os.path.join(MainModsPath, 'EldenRing_DubPT-BR')
        self.EldenRingFSR3 = os.path.join(MainModsPath, 'EldenRing_FSR3')
        self.EldenRingIncreaseAnimationDistance = os.path.join(MainModsPath, 'EldenRing_IncreaseAnimationDistance')
        self.EldenRingRemoveBlackBars = os.path.join(MainModsPath, 'EldenRing_RemoveBlackBars')
        self.EldenRingRemoveChromaticAberrationPath = os.path.join(MainModsPath, 'EldenRing_RemoveChromaticAberration')
        self.EldenRingRemoveVignette = os.path.join(MainModsPath, 'EldenRing_RemoveVignette')
        self.EldenRingUnlockFPS = os.path.join(MainModsPath, 'EldenRing_UnlockFPS')

        self.EnabledEngineMods = []
        self.ModLoaderOrder = []
        self.ModsArchives = {
            'EldenRing_DubPT-BR': {
                'Files': [],
                'Folders': ['movie', 'sd']
            },
            'EldenRing_CO-OP': {
                'Files': ['launch_elden_ring_seamlesscoop.exe',],
                'Folders': ['SeamlessCoop']
            },
            'EldenRing_UnlockFPS': {
                'Files': ['UnlockTheFps.dll'],
                'Folders': ['UnlockTheFps']
            },
            'EldenRing_IncreaseAnimationDistance': {
                'Files': ['IncreaseAnimationDistance.dll'],
                'Folders': []
            },
            'EldenRing_FSR3': {
                'Files': ['EldenRingUpscaler.dll', 'EldenRingUpscaler.ini', 'EldenRingUpscalerPreset.ini', 'RDR2Upscaler.org',
                          'd3dcompiler_47.dll', 'dxgi.dll', 'EldenRingUpscalerPreset.ini', 'ReShade.ini', 'ReShade.log', 'ReShadePreset.ini'],
                'Folders': ['UpscalerBasePlugin', 'reshade-shaders']
            },
            'EldenRing_RemoveBlackBars': {
                'Files': ['UltrawideFix.dll'],
                'Folders': ['UltrawideFix']
            },
            'EldenRing_DisableSharpenFilter': {
                'Files': ['DisableSharpenFilter.dll'],
                'Folders': []
            },
            'EldenRing_RemoveChromaticAberration': {
                'Files': ['RemoveChromaticAberration.dll'],
                'Folders': []
            },
            'EldenRing_RemoveVignette': {
                'Files': ['RemoveVignette.dll'],
                'Folders': []
            },
            "EldenRing_ModEngine": {
                'Files': ['config_eldenring.toml', 'dinput8.dll', 'mod_loader_config.ini', 'mod_loader_log.txt', 'modengine2_launcher.exe'],
                'Folders': ['mod', 'modengine2', 'mods']
            }
        }
        self.ValidadeInstalledMods()
    def GetModPath(self, modName):
        match modName:
            case 'EldenRing_CO-OP':
                return self.EldenRingCoopPath
            case 'EldenRing_DubPT-BR':
                return self.EldenRingDubPath
            case 'EldenRing_UnlockFPS':
                return self.EldenRingUnlockFPS
            case 'EldenRing_RemoveChromaticAberration':
                return self.EldenRingRemoveChromaticAberrationPath
            case 'EldenRing_RemoveVignette':
                return self.EldenRingRemoveVignette
            case 'EldenRing_FSR3':
                return self.EldenRingFSR3
            case 'EldenRing_DisableSharpenFilter':
                return self.EldenRingDisableSharpenFilter
            case 'EldenRing_RemoveBlackBars':
                return self.EldenRingRemoveBlackBars
            case 'EldenRing_IncreaseAnimationDistance':
                return self.EldenRingIncreaseAnimationDistance
            case _:
                Exception = f"Mod '{modName}' not found"
                raise Exception
    def MoveModFilesToEldenRingMod(self, modPath:str):
        if modPath == '' or not os.path.exists(modPath):
            print(f"The path '{modPath}' does not exist.")
            return
        if modPath == self.EldenRingDubPath:
            self.BackUpMovieFolder()

        for root, dirs, files in os.walk(modPath):
            relative_path = os.path.relpath(root, modPath)
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
        print(f"{modPath.split('\\')[-1]} enabled!")
    def DisableMod(self, modPath:str, modArchives: dict):
        modName = modPath.split('\\')[-1]
        print(f"Disabling {modName}")
        for root, dirs, files in os.walk(self.EldenRingGamePath):
            for fileName in files:
                if any(str(fileName).lower() == file.lower() for file in modArchives['Files']):
                    os.remove(os.path.join(root,fileName))
            for dirName in dirs:
                if any(str(dirName).lower() == Dir.lower() for Dir in modArchives['Folders']):
                    if modName == 'EldenRing_DubPT-BR' and dirName == 'sd' and root != os.path.join(self.EldenRingGamePath,'mod'):
                        continue
                    shutil.rmtree(os.path.join(root, dirName))
        Utils().clear_console()
        if modName == 'EldenRing_DubPT-BR':
            self.RestoreMovieFolder()
        print(f"{modName} disabled!")
    def BackUpMovieFolder(self):
        print('Backing up movie folder...')
        if not os.path.exists(os.path.join(self.EldenRingGamePath, 'movie_backup')):
            # os.rename(os.path.join(self.EldenRingGamePath, 'movie'),
            #           os.path.join(self.EldenRingGamePath, 'movie_backup'))
            shutil.copytree(os.path.join(self.EldenRingGamePath, 'movie'),
                            os.path.join(self.EldenRingGamePath, 'movie_backup'))
    def RestoreMovieFolder(self):
        if os.path.exists(os.path.join(self.EldenRingGamePath, 'movie_backup')):
            if os.path.exists(os.path.join(self.EldenRingGamePath, 'movie')):
                shutil.rmtree(os.path.join(self.EldenRingGamePath, 'movie'))
            os.rename(os.path.join(self.EldenRingGamePath, 'movie_backup'),
                      os.path.join(self.EldenRingGamePath, 'movie'))
    def SetModEngineToml(self):
        self.ValidadeInstalledMods()
        paths = [self.EldenRingEnginePath, self.EldenRingGamePath]
        for path in paths:
            try:
                tomlPath = os.path.join(path, 'config_eldenring.toml')
                with open(tomlPath, 'r') as file:
                    data = toml.load(file)

                #THIS IS NOT NECESSARY ANYMORE
                # if (os.path.exists(os.path.join(path, 'winmm.dll'))
                #         and r'SeamlessCoop\elden_ring_seamless_coop.dll' in self.EnabledEngineMods):
                #     self.EnabledEngineMods.pop(self.EnabledEngineMods.index(r'SeamlessCoop\elden_ring_seamless_coop.dll'))

                data['modengine']['external_dlls'] = self.EnabledEngineMods
                with open(tomlPath, 'w') as file:
                    toml.dump(data, file)
            except Exception as e:
                continue
    def SetModLoaderOrderIni(self):
        self.ValidadeInstalledMods()
        paths = [self.EldenRingEnginePath, self.EldenRingGamePath]

        for path in paths:
            try:
                iniPath = os.path.join(path, 'mod_loader_config.ini')
                config = configparser.RawConfigParser()
                config.optionxform = str
                config.read(iniPath)
                config.remove_section('modloader')
                config.add_section('modloader')
                config.set('modloader','load_delay', str(5000))
                config.set('modloader','show_terminal', str(0))
                config.remove_section('loadorder')
                config.add_section('loadorder')
                for index, dll in enumerate(self.ModLoaderOrder):
                    config.set('loadorder', dll, str(index + 1))
                with open(iniPath, 'w') as iniFile:
                    config.write(iniFile)
            except Exception as e:
                continue
    def CheckIfModIsEnabled(self, modArchives: dict):
        if modArchives == self.ModsArchives['EldenRing_DubPT-BR'] and not os.path.exists(os.path.join(self.EldenRingGamePath, 'movie_backup')):
            return False
        for root, dirs, files in os.walk(self.EldenRingGamePath):
            for fileName in files:
                if any(str(fileName).lower() == file.lower() for file in modArchives['Files']):
                    return True
            for dirName in dirs:
                if any(str(dirName).lower() == Dir.lower() for Dir in modArchives['Folders']):
                    return True
        return False
    def ChooseExecution(self, ModArchives:dict, ModPath:str):
        Utils().clear_console()
        self.ValidadeInstalledMods()
        if self.CheckIfModIsEnabled(ModArchives):
            self.DisableMod(ModPath, ModArchives)
            self.SetModEngineToml()
            self.SetModLoaderOrderIni()
            if (len(self.EnabledEngineMods) == 0 and len(self.ModLoaderOrder) == 0
                    and self.CheckIfModIsEnabled(self.ModsArchives['EldenRing_ModEngine'])
                    and not os.path.exists(os.path.join(self.EldenRingGamePath, 'mod', 'sd'))):
                self.DisableMod(self.EldenRingEnginePath, self.ModsArchives['EldenRing_ModEngine'])
        else:
            self.MoveModFilesToEldenRingMod(ModPath)
            self.SetModEngineToml()
            if (len(self.EnabledEngineMods) > 0 or len(self.ModLoaderOrder) > 0):
                if not os.path.exists(os.path.join(self.EldenRingGamePath, 'modengine2_launcher.exe')):
                    self.GetModEngine()
            elif len(self.EnabledEngineMods) == 0 and len(self.ModLoaderOrder) == 0 and ModPath == self.EldenRingDubPath:
                if not os.path.exists(os.path.join(self.EldenRingGamePath, 'modengine2_launcher.exe')):
                    self.GetModEngine()
            self.SetModLoaderOrderIni()

    def ValidadeInstalledMods(self):
        self.EnabledEngineMods = []
        self.ModLoaderOrder = []
        for mod in self.ModsArchives:
            if self.CheckIfModIsEnabled(self.ModsArchives[mod]):
                match mod:
                    case 'EldenRing_ModEngine':
                        continue
                    case 'EldenRing_DubPT-BR':
                        continue
                    case 'EldenRing_CO-OP':
                        self.EnabledEngineMods.append(r'SeamlessCoop\elden_ring_seamless_coop.dll')
                    case _:
                        if 'dinput8.dll' not in self.EnabledEngineMods:
                            self.EnabledEngineMods.append('dinput8.dll')
                        match mod:
                            case 'EldenRing_UnlockFPS':
                                self.ModLoaderOrder.append('UnlockTheFps.dll')
                            case 'EldenRing_RemoveChromaticAberration':
                                self.ModLoaderOrder.append('RemoveChromaticAberration.dll')
                            case 'EldenRing_RemoveVignette':
                                self.ModLoaderOrder.append('RemoveVignette.dll')
                            case 'EldenRing_FSR3':
                                self.ModLoaderOrder.append('EldenRingUpscaler.dll')
                            case 'EldenRing_DisableSharpenFilter':
                                self.ModLoaderOrder.append('DisableSharpenFilter.dll')
                            case 'EldenRing_RemoveBlackBars':
                                self.ModLoaderOrder.append('UltrawideFix.dll')
                            case 'EldenRing_IncreaseAnimationDistance':
                                self.ModLoaderOrder.append('IncreaseAnimationDistance.dll')

    def DisableAllMods(self):
        print('Disabling all mods')
        for mod in self.ModsArchives:
            if self.CheckIfModIsEnabled(self.ModsArchives[mod]) and mod != 'EldenRing_ModEngine':
                path = self.GetModPath(mod)
                self.DisableMod(path, self.ModsArchives[mod])
        self.SetModEngineToml()
        self.SetModLoaderOrderIni()
        if (len(self.EnabledEngineMods) == 0 and len(self.ModLoaderOrder) == 0
                and self.CheckIfModIsEnabled(self.ModsArchives['EldenRing_ModEngine'])
                and not os.path.exists(os.path.join(self.EldenRingGamePath, 'mod', 'sd'))):
            self.DisableMod(self.EldenRingEnginePath, self.ModsArchives['EldenRing_ModEngine'])
        Utils().clear_console()
        print('All mods disabled!')

    def ChangeCoopPassword(self):
        ChangingPaths = [self.EldenRingGamePath, self.EldenRingCoopPath]
        newPassword = ''
        for path in ChangingPaths:
            try:
                config = configparser.ConfigParser()
                filePath = os.path.join(path, r'SeamlessCoop\seamlesscoopsettings.ini')
                config.read(filePath)
                if newPassword == '':
                    print(f'Current Password: {config['PASSWORD']['cooppassword']}')
                    newPassword = str(input('Set the new password: '))
                config['PASSWORD']['cooppassword'] = newPassword
                with open(filePath, 'w') as iniFile:
                    config.write(iniFile)
                print(f'Password changed in {filePath}')
            except Exception as e:
                print(f"Warning: {e}")
        return newPassword

    def GetModEngine(self):
        if self.EldenRingEnginePath == '' or not os.path.exists(self.EldenRingEnginePath):
            print(f"The path '{self.EldenRingEnginePath}' does not exist.")
            return
        try:
            for root, dirs, files in os.walk(self.EldenRingEnginePath):

                relative_path = str(os.path.relpath(root, self.EldenRingEnginePath))
                destination_root = os.path.join(self.EldenRingGamePath, relative_path)

                os.makedirs(destination_root, exist_ok=True)

                for fileName in files:
                    sourceFilePath = str(os.path.join(root, fileName))
                    destinationFilePath = str(os.path.join(destination_root, fileName))

                    if os.path.exists(destinationFilePath):
                        continue

                    shutil.copy2(sourceFilePath, destinationFilePath)
            Utils().clear_console()
            print("ModEngine enabled!")

        except Exception as e:
            print(f"Error: {e}")

    def ReturningEnableDisable(self, modArchives: dict):
        if self.CheckIfModIsEnabled(modArchives):
            return 'DISABLE'
        else:
            return 'ENABLE'

    def menu(self):
        try:
            while True:
                print('[ ELDEN RING MODS MENU ]')
                print(f' 1. {self.ReturningEnableDisable(self.ModsArchives['EldenRing_CO-OP'])} SEAMLESS CO-OP')
                print(f' 2. {self.ReturningEnableDisable(self.ModsArchives['EldenRing_DubPT-BR'])} BRAZILIAN-PORTUGUESE DUB')
                print(f' 3. {self.ReturningEnableDisable(self.ModsArchives['EldenRing_UnlockFPS'])} UNLOCK FPS')
                print(f' 4. {self.ReturningEnableDisable(self.ModsArchives['EldenRing_RemoveChromaticAberration'])} REMOVE CHROMATIC ABERRATION')
                print(f' 5. {self.ReturningEnableDisable(self.ModsArchives['EldenRing_RemoveVignette'])} REMOVE VIGNETTE')
                print(f' 6. {self.ReturningEnableDisable(self.ModsArchives['EldenRing_FSR3'])} FSR3')
                print(f' 7. {self.ReturningEnableDisable(self.ModsArchives['EldenRing_DisableSharpenFilter'])} DISABLE SHARPEN FILTER')
                print(f' 8. {self.ReturningEnableDisable(self.ModsArchives['EldenRing_RemoveBlackBars'])} REMOVE BLACK BARS')
                print(f' 9. {self.ReturningEnableDisable(self.ModsArchives['EldenRing_IncreaseAnimationDistance'])} INCREASE ANIMATION DISTANCE')
                print(f'10. DISABLE ALL MODS')
                print(f' 0. EXIT MODS MENU')
                choice = str(input('Enter your choice: '))
                match choice:
                    case '1':
                        self.ChooseExecution(self.ModsArchives['EldenRing_CO-OP'], self.EldenRingCoopPath)
                    case '2':
                        self.ChooseExecution(self.ModsArchives['EldenRing_DubPT-BR'], self.EldenRingDubPath)
                    case '3':
                        self.ChooseExecution(self.ModsArchives['EldenRing_UnlockFPS'], self.EldenRingUnlockFPS)
                    case '4':
                        self.ChooseExecution(self.ModsArchives['EldenRing_RemoveChromaticAberration'], self.EldenRingRemoveChromaticAberrationPath)
                    case '5':
                        self.ChooseExecution(self.ModsArchives['EldenRing_RemoveVignette'], self.EldenRingRemoveVignette)
                    case '6':
                        self.ChooseExecution(self.ModsArchives['EldenRing_FSR3'], self.EldenRingFSR3)
                    case '7':
                        self.ChooseExecution(self.ModsArchives['EldenRing_DisableSharpenFilter'], self.EldenRingDisableSharpenFilter)
                    case '8':
                        self.ChooseExecution(self.ModsArchives['EldenRing_RemoveBlackBars'], self.EldenRingRemoveBlackBars)
                    case '9':
                        self.ChooseExecution(self.ModsArchives['EldenRing_IncreaseAnimationDistance'], self.EldenRingIncreaseAnimationDistance)
                    case '10':
                        self.DisableAllMods()
                    case '0':
                        print("Exiting Mods Menu...")
                        Utils().clear_console()
                        break
                    case _:
                        Utils().clear_console()
                        print(f"Invalid choice: {choice}, choose another one")
        except Exception as e:
            Utils().clear_console()
            print(f"Error: {e}")
            self.menu()
