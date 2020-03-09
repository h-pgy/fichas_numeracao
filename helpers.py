import json
import requests

# refaz a lista para tirar itens que estao repetidos> função futura
def clean_dup_list(list_dup_items):
    unique_list = list()
    for i in range(len(list_dup_items)):
        if list_dup_items[i] not in list_dup_items[i + 1:]:
            unique_list.append(list_dup_items[i])
    return unique_list

def validar_AD(user, passw):
    url = 'http://10.75.18.36:8083/conexao_ldap/?user={user}&passw={passw}'.format(user=user, passw=passw)

    # a linha abaixo pode virar uma função separada depois de resolução de proxy
    proxies = {'http': 'http://{user}:{passw}@10.10.193.25:3128'.format(user=user, passw=passw),
               'https': 'https://{user}:{passw}@10.10.193.25:3128'.format(user=user, passw=passw)}

    # with requests.get(url, proxies=proxies) as f:
    with requests.get(url) as f:
        json_resp = f.text

    return json.loads(json_resp)