from Services.Configs.AppConfigService import AppConfigService
from Services.MasterService import Master

if '__main__' == __name__:
    print('Loading App Config...')
    try:
        jsonDict = AppConfigService().ReadAppConfig()
    except Exception as e:
        print("It was not possible to load the appconfig.json file.")
        print('Getting online data...')
        AppConfigService().CreateAppConfig()
        jsonDict = AppConfigService().ReadAppConfig()

    Master(jsonDict).menu()
