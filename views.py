from flask import request, render_template, flash, send_from_directory, redirect, url_for, session
import os
from helpers import clean_dup_list, validar_AD, log_as_admin
from app import app
import json
from encripter import Crypt

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/authenticate', methods=['POST', ])
def authenticate():
    login = request.form['user']
    passw = request.form['passw']

    super_admin = 'superadministrador'
    senha_super_admin = 'Prodam'


    if login == super_admin and passw == senha_super_admin:
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

# -------------------------------------------------------------------------------------------------------------------
@app.route('/fichas')
def index():
    return render_template('fichasSearch.html', titulo='Fichas de Numeração')

@app.route('/search_fichas', methods=['POST', ])
def search_fichas():
    flash('Para documentos com extensão .tif confira a pasta de download!')
    codlog = request.form['cd_codlog']

    path = r"\\nas.prodam\SL0104_Fichas_Numeracao"
    # path = r"C:\Users\x369482\Desktop\DLE_Fichas_renomeadas"
    user = log_as_admin()
    user.logon()
    main_folder_files = os.listdir(path)
    result_list = list()
    inside_files_list = list()
    pdf_dict = dict()

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


@app.route('/view_fichas', methods=['GET', ])
def view_fichas():
    path = request.args['path']
    file = request.args['file']
    folder = request.args['folder']

    if file.endswith('.tif'):
        path = path + r'/' + folder
        return send_from_directory(path, file)

    return send_from_directory(path, file)
