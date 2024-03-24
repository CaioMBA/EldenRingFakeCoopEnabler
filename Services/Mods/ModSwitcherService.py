from Services.Mods.EldenRingModsService import Mods as EldenMods


class ModSwitcher():
    def __init__(self, GameName: str, MainModsPath: str, EnginePath: str, GamePath: str):
        self.GameName = GameName
        self.MainModsPath = MainModsPath
        self.EnginePath = EnginePath
        self.GamePath = GamePath

    def Switcher(self) -> None:
        match self.GameName:
            case 'ELDEN RING':
                EldenMods(self.MainModsPath, self.EnginePath, self.GamePath).menu()
            case _:
                print(f'No mods available for {self.GameName} yet.')
