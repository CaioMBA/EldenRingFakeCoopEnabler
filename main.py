from Services.UtilsService import Utils
from Services.MasterService import Master

if '__main__' == __name__:
    try:
        jsonDict = Utils().ReadJsonConfig()
    except Exception as e:
        print("Não foi possível abrir o arquivo appconfig.json")
        print("Por favor, preencha as informações necessárias para o funcionamento do programa.")
        print("Caso não tenha o caminho deixe vazio")
        Utils().CreateJsonConfig()
        jsonDict = Utils().ReadJsonConfig()

    Master(jsonDict).menu()
