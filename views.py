from flask import request, render_template, flash, send_from_directory, redirect, url_for, session
import os
from helpers import clean_dup_list, validar_AD, log_as_admin, login_required, valida_super_adm
from app import app
import json
from encripter import Crypt, ChaveInvalida

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
        # path = r"C:\Users\x369482\Desktop\DLE_Fichas_renomeadas"
        user = log_as_admin()
        user.logon()
        main_folder_files = os.listdir(path)
        result_list = list()
        inside_files_list = list()
        pdf_dict = dict()
        flash('Para documentos com extensão .tif confira a pasta de download!')
        # lista com o nome dos arquivos e das pastas que estao dentro da pasta principal que estao de acordo com a pesquisa
        for file in main_folder_files:
            if file[:8] == codlog:
                result_list.append(file)

        # lista os items que foram encontrados na pesquisa e separa .pdf das Pastas
        for item in result_list:
            if item.endswith('.pdf'):
                pdf_dict = {item: item}
            else:
                # quando é pasta deve abrir a pasta e listar os arquivos contidos la dentro
                path2 = r"\\nas.prodam\SL0104_Fichas_Numeracao\{}".format(item)
                # path2 = r"C:\Users\x369482\Desktop\DLE_Fichas_renomeadas\{}".format(item)
                inside_files = os.listdir(path2)
                for i in inside_files:
                    if not i.endswith('.db'):
                        item_dict = {item: inside_files}
                        inside_files_list.append(item_dict)
            inside_files_list.append(pdf_dict)
        unique_list = clean_dup_list(inside_files_list)

        user.logoff()

        return render_template('fichasList.html', titulo='Fichas de Numeração', path=path,
                               inside_files_list=unique_list)
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
    folder = request.args['folder']

    if file.endswith('.tif'):
        path = path + r'/' + folder
        return send_from_directory(path, file)

    return send_from_directory(path, file)
