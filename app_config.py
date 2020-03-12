from datetime import timedelta

SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "case"
PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)

USUARIO_SUPER_ADM = "superadministrador"
SENHA_SUPER_ADM = "Agil"