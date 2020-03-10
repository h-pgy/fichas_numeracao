from flask import Flask
import socket

app = Flask(__name__)
app.config.from_pyfile('app_config.py')

# importar as views somente após criar o app pois se tratam apenas das rotas do app e caso importado no começo da pagina
# causaria um erro de "loop" pois o app é chamado dentro das views

from views import *


if __name__ == "__main__":

    ip = socket.gethostbyname(socket.gethostname())
    app.run(debug=True, host=ip, port='8086')


