from flask import request, render_template, flash, send_from_directory, redirect, url_for, session
import os
from helpers import validar_AD, log_as_admin, login_required, valida_super_adm
from app import app
import json
from encripter import Crypt, ChaveInvalida
from models import Ficha

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/authenticate', methods=['POST', ])
def authenticate():
    login = request.form['user']
    passw = request.form['passw']

    super_adm = valida_super_adm(login, passw)

    if super_adm:
        session['logged_user'] = login
        session.permanent = True
        flash('Bem vindo(a)!')
        return redirect(url_for('cadastro_admin'))
    else:
        validacao_ad = validar_AD(login, passw)
        if validacao_ad:
            session['logged_user'] = login
            session.permanent = True
            flash('Bem vindo(a)!')
            next = request.form['next']
            return redirect(next)
        else:
            flash('Nao foi possivel fazer login')
            return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

#--------------------------------------------------------------------------------------------------------------------
@app.route('/cadastro-admin')
@login_required
def cadastro_admin():
    return render_template('cadastroAdmin.html', titulo="Cadastro de administrador do sistema")

@app.route('/admin', methods=['POST',])
def admin():
    form_data = request.form
    dados_admin = dict(request.form)
    dados_admin['senha'] = Crypt.encrypt(form_data['senha']).decode('utf-8')
    with open('administrador.json', 'w') as f:
        json.dump(dados_admin, f)
    flash('Administrador cadastrado com sucesso!')
    log_as_admin()

    return redirect(url_for('index'))

@app.route('/exibe-admin')
@login_required
def exibe_admin(admin_file = 'administrador.json'):
    with open(admin_file) as f:
        admin = json.load(f)
    return render_template('exibeAdmin.html', titulo='Administrador do sistema', admin=admin)

# -------------------------------------------------------------------------------------------------------------------
@app.route('/fichas')
@login_required
def index():
    return render_template('fichasSearch.html', titulo='Fichas de Numeração')

@app.route('/search_fichas', methods=['POST', ])
@login_required
def search_fichas():
    try:
        codlog = request.form['cd_codlog']
        path = r"\\nas.prodam\SL0104_Fichas_Numeracao"
        user = log_as_admin()
        user.logon()
        walk = os.walk(path)
        result = []
        for root, dirs, files in walk:

            for file in files:
                if file.endswith('.pdf') or file.endswith('.tif'):
                    if file[:8] == codlog:
                        ficha = Ficha(path = root, filename=file)
                        result.append(ficha)

        flash('Para documentos com extensão .tif confira a pasta de download!')

        user.logoff()

        return render_template('fichasList.html', titulo='Fichas de Numeração', path=path,
                               file_list=result)
    except ChaveInvalida:
        flash('Acesso Negado!\n'
              'Necessario recadastrar o administrador do sistema.\n '
              'Entre em contato com o diretor da divisão ou com a equipe de desenvolvimento.')
        return redirect(url_for('login'))


@app.route('/view_fichas', methods=['GET', ])
@login_required
def view_fichas():
    path = request.args['path']
    file = request.args['file']

    return send_from_directory(path, file)

@app.before_request
def set_domain_session():
    session['domain'] = request.headers['Host']
