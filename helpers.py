import functools
from flask import session, redirect, url_for
import json
from consumo_ldap import LDAP_SERVICE, validar_ad
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

    return validar_ad(user, passw, LDAP_SERVICE['ip'], LDAP_SERVICE['porta'])

def log_as_admin(admin_file = 'administrador.json'):

    with open(admin_file) as f:
        admin = json.load(f)

    usuario = admin['usuario']
    senha = admin['senha'].encode('utf-8')
    senha = Crypt.decrypt(senha)


    user = Impersonate(usuario, senha)

    return user

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not 'logged_user' in session.keys():
            return redirect(url_for('login'))
        return view(**kwargs)

    return wrapped_view
