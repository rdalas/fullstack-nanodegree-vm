from flask import Flask, render_template, request, redirect, url_for, jsonify
# Importa arquivo CRUD - acesso ao banco de dados
import crud
from flask import session as login_session, flash
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Project"


@app.route('/login/')
def showLogin():
    state = ''.join(
        random.choice(
            string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = (
        'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
        % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;'
    output += '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("Conectado como %s" % login_session['email'])
    print "done!"
    return output


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = (
        'https://accounts.google.com/o/oauth2/revoke?token=%s'
        % login_session['access_token'])
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        flash('Desconectado com sucesso.')
        return redirect(url_for('siteHome'))
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Inicio dos sites que consultam o banco de dados
@app.route('/catalog/JSON/')
def catalogoJson():
    categorias = crud.catalogoJson()
    return jsonify(
        catalogo=[
            dict(
                c.serialize,
                itens=[i.serialize for i in c.itens]) for c in categorias])


@app.route('/catalog/<int:categoria_id>/<int:item_id>/JSON/')
def itemJson(categoria_id, item_id):
    item = crud.bucaItem_porCategoriaId(categoria_id, item_id)
    return jsonify(item=item.serialize)


@app.route('/')
@app.route('/catalog/')
def siteHome():
    categoriasMenu = crud.buscaTodasCategorias()
    ultimosItens = crud.ultimosItens()
    return render_template(
        'home.html',
        categoriasMenu=categoriasMenu,
        ultimosItens=ultimosItens,
        login_session=login_session)


@app.route('/catalog/<int:categoria_id>/')
@app.route('/catalog/<int:categoria_id>/items/')
def catalogoItens(categoria_id):
    categoriasMenu = crud.buscaTodasCategorias()
    categoria = crud.buscaCategoria_porId(categoria_id)
    itensCategoria = crud.buscaItens_porCategoria(categoria_id)
    contador = crud.contaItens_porCategoria(categoria_id)
    return render_template(
        'items.html',
        categoriasMenu=categoriasMenu,
        categoria=categoria,
        itensCategoria=itensCategoria,
        contador=contador,
        login_session=login_session)


@app.route('/catalog/<int:categoria_id>/<int:item_id>/')
def descricaoItem(categoria_id, item_id):
    categoria = crud.buscaCategoria_porId(categoria_id)
    item = crud.bucaItem_porCategoriaId(categoria_id, item_id)
    return render_template(
        'item.html',
        categoria=categoria,
        item=item,
        login_session=login_session)
# Fim da consulta


# Site para adicionar itens
@app.route('/catalog/new/', methods=['GET', 'POST'])
def adicionaItem():
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    else:
        if request.method == 'POST':
            nome = request.form['nome']
            descricao = request.form['descricao']
            categoria_id = request.form['categoria_id']
            user = login_session['email']
            if nome and descricao and categoria_id:
                crud.novoItem(nome, descricao, int(categoria_id), user)
                flash('Item Adicionado com sucesso !')
                return redirect(url_for('siteHome'))
            else:
                flash('Todos os campos devem ser preenchidos !')
                return redirect(url_for('adicionaItem'))
        else:
            categorias = crud.buscaTodasCategorias()
            return render_template(
                'newitem.html',
                categorias=categorias,
                login_session=login_session)


# Site para alterar itens
@app.route('/catalog/<int:item_id>/edit/', methods=['GET', 'POST'])
def alteraItem(item_id):
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    else:
        item = crud.bucaItem_porId(item_id)
    	if request.method == 'POST':
            if item.user == login_session['email']:
                nome = request.form['nome']
                descricao = request.form['descricao']
                categoria_id = request.form['categoria_id']
                if nome and descricao and categoria_id:
                    item = crud.alteraItem(
                        item_id,
                        nome,
                        descricao,
                        categoria_id)
                    item_id = item[0]
                    categoria_id = item[1]
                    flash('Item Alterado com sucesso !')
                    return redirect(url_for(
                        'descricaoItem',
                        categoria_id=categoria_id,
                        item_id=item_id))
                else:
                    flash('Todos os campos devem ser preenchidos !')
                    return redirect(url_for('alteraItem', item_id=item.id))
            else:
                flash(
                    'Sem permissao para alterar o registro, voce nao e %s !'
                    % item.user)
                return redirect(url_for('alteraItem', item_id=item.id))
        else:
            categorias = crud.buscaTodasCategorias()
            return render_template(
                'edititem.html',
                item=item,
                categorias=categorias,
                login_session=login_session)


# Site para deletar itens
@app.route('/catalog/<int:item_id>/delete/', methods=['GET', 'POST'])
def deletaItem(item_id):
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    else:
        itemToDelete = crud.bucaItem_porId(item_id)
        if request.method == 'POST':
            if itemToDelete.user == login_session['email']:
                crud.apagaItem(item_id)
                flash('Item Apagado com sucesso !')
                return redirect(url_for(
                    'catalogoItens',
                    categoria_id=itemToDelete.categoria_id))
            else:
                flash(
                    'Sem permissao para deletar o registro, voce nao e %s !'
                    % itemToDelete.user)
                return redirect(url_for('deletaItem', item_id=itemToDelete.id))
        else:
            return render_template(
                'deleteitem.html',
                itemToDelete=itemToDelete,
                login_session=login_session)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
