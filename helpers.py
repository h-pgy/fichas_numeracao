import json
import requests
from impersonator import Impersonate
from encripter import Crypt

# refaz a lista para tirar itens que estao repetidos> função futura
def clean_dup_list(list_dup_items):
    unique_list = list()
    for i in range(len(list_dup_items)):
        if list_dup_items[i] not in list_dup_items[i + 1:]:
            unique_list.append(list_dup_items[i])
    return unique_list

def validar_AD(user, passw):
    url = 'http://10.75.18.36:8083/conexao_ldap/?user={user}&passw={passw}'.format(user=user, passw=passw)

    s = requests.Session()
    s.trust_env = False # obrigando a funcionar dentro da rede da PMSP
    with s.get(url) as f:
        json_resp = f.text

    return json.loads(json_resp)

def log_as_admin(admin_file = 'administrador.json'):

    with open(admin_file) as f:
        admin = json.load(f)

    usuario = admin['usuario']
    senha = admin['senha'].encode('utf-8')
    senha = Crypt.decrypt(senha)


    user = Impersonate(usuario, senha)

    return user
