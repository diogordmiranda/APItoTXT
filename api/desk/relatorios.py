import json
import traceback
import requests as requests


class Relatorios:
    baseApi = " "
    api = None

    _token = ''

    def __init__(self, chaves, registros):
        self.lista = []
        self.getToken()
        self._chaves = chaves
        self._registros = registros

    def run(self):
        for chave in self._chaves:
            pagina_final = False
            pagina = 150
            with open("relatorio.txt", "w") as arquivo:
                while (pagina_final is False):
                    pagina_final = self.imprimirRelatorio(chave=chave, pagina=pagina, registros=self._registros)
                    self.gravaDados()
                    pagina += 1
            arquivo.close()

    def getToken(self):
        api = " "
        secret = ""
        url = self.baseApi + ""
        data = {
            "PublicKey": secret
        }
        with requests.post(url=url, json=data, headers={"Authorization": api}) as response:
            try:
                result_data = response.text.replace('"', '')
                if (result_data != "Prefixo Expirado ou não Existe"):
                    self._token = result_data
            except Exception:
                traceback.print_exc()

    def imprimirRelatorio(self, chave, pagina, registros):

        header = {
            "Authorization": self._token
        }
        data = {
            "Chave": str(chave),
            "APartirDe": str(pagina * registros),
            "Total": str(registros),
        }
        url = self.baseApi + "Relatorios/Imprimir"
        response = requests.post(url=url, json=data, headers=header)
        if (response.status_code == 200):
            print("The request was a success: " + str(pagina))
            self.result_data = response.json()
            if 'hasMore' in self.result_data and self.result_data['hasMore'] == 'true':
                return False
            return True
        elif (response.status_code == 404):
            print("Result not found!")
            return True

    def gravaDados(self):
        json_obj = json.dumps(self.result_data, indent=3)
        with open("relatorio.txt", "a") as arquivo:
            arquivo.write(json_obj)


