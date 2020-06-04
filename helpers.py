import functools
from flask import session, redirect, url_for
import json
from consumo_ldap import LDAP_SERVICE, validar_ad
from impersonator import Impersonate
from encripter import Crypt
from app_config import USUARIO_SUPER_ADM, SENHA_SUPER_ADM

def valida_super_adm(user, passw):
    return user == USUARIO_SUPER_ADM and passw == SENHA_SUPER_ADM

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

