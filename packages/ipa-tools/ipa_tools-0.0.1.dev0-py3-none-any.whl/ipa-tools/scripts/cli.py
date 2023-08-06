import json
import requests 
import sys
import jsonschema


class ipaResponse(requests.Response):
    url = "https://www.indicepa.gov.it/public-ws/WS01_SFE_CF.php"
    url_jsonschema = "https://www.indicepa.gov.it/public-services/docs-read-service.php?dstype=FS&filename=WS01_SFE_CF_SCHEMA.json"

    def __request(self):
        data = {'AUTH_ID': self.auth_id, 'CF': self.fiscal_code}
        r = requests.post(url = self.url, data = data)
        return r.json()

    def __request_jsonschema(self):
        r = requests.get(url = self.url_jsonschema)
        return r.json()

    @property
    def raw(self):
        return self.__request()

    @property
    def raw_jsonschema(self):
        return self.__request_jsonschema()

    @property
    def result(self):
        return self.raw['result']

    @property
    def data(self):
        return self.raw['data'][0]

    def validate(self):
        return jsonschema.validate(instance=self.__request(), schema=self.__request_jsonschema())

    def __init__(self, auth_id, fiscal_code):
        self.auth_id = auth_id
        self.fiscal_code = fiscal_code


class publicBody(ipaResponse):
    @property
    def cod_amm(self):
        return self.data['cod_amm']

    @property
    def des_amm(self):
        return self.data['des_amm']

    def __init__(self, auth_id, fiscal_code):
        super().__init__(auth_id, fiscal_code)


i = publicBody(sys.argv[1], sys.argv[2])
print(i.result)
print(i.data)
print(i.cod_amm)
print(i.des_amm)
print(i.raw_jsonschema)
print(i.validate())
