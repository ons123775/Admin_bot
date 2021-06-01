from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask.helpers import flash
from werkzeug.security import check_password_hash

import functools
import os

from config.connection import open_connection

app = Flask(__name__)
app.debug = True
app.secret_key = 'MON_APP'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
target = os.path.join(APP_ROOT, r"static\images")


def login_required(view):

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'logged_in' not in session:
            return redirect(url_for("login"))

        return view(**kwargs)

    return wrapped_view


@app.route('/')
@login_required # decorator
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        mot_de_passe = request.form['mot_de_passe']

        con = open_connection()
        cur = con.cursor()

        query = ' SELECT * FROM admin WHERE email = %s '
        cur.execute(query, [email])

        admin = cur.fetchone()
        if admin:
            if check_password_hash(admin[4], mot_de_passe):
                session['logged_in'] = True
                return redirect(url_for('index'))
        
        flash('vérifier votre email et mot de passe', 'danger')

    return render_template('login.html')


@app.route('/categorie')
@login_required
def categorie_index():
    con = open_connection()
    cur = con.cursor()

    query = ' SELECT * FROM categorie ORDER BY nom ASC '
    cur.execute(query)

    categories = cur.fetchall()

    return render_template('categorie/index.html', categories=categories)


@app.route('/categorie/ajouter', methods=['GET', 'POST'])
@login_required
def categorie_ajouter():
    if request.method == 'POST':
        nom = request.form['nom']
        description = request.form['description']

        con = open_connection()
        cur = con.cursor()

        # upload image
        for upload in request.files.getlist('img'):
            # get file name
            logo = upload.filename
            if logo == '':
                flash('svp, ajouter une image au catégorie', 'danger')
                return render_template('categorie/ajouter.html')

            # get file extension
            ext = logo.split('.')[1]
            if ext in ['png', 'jpg', 'jpeg']:
                # save image in target
                destination = '/'.join([target, logo])
                upload.save(destination)

                query = 'INSERT INTO categorie(nom, img, description) VALUES(%s, %s, %s)'
                cur.execute(query, [nom, logo, description])
                con.commit()

                flash('Catégorie ajouter', 'success')
                return redirect(url_for('categorie_index'))

            flash(
                'Seuls les fichiers {png, jpg, jpeg} sont autorisés...', 'danger')
            return render_template('categorie/ajouter.html')

    else:  # method == 'GET'
        return render_template('categorie/ajouter.html')


@app.route('/categorie/modifier/<string:id>', methods=['GET', 'POST'])
@login_required
def categorie_modifier(id):
    con = open_connection()
    cur = con.cursor()

    if request.method == 'POST':
        nom = request.form['nom']
        description = request.form['description']

        # upload image
        for upload in request.files.getlist('img'):
            # get file name
            logo = upload.filename
            if logo == '':
                query = 'UPDATE categorie SET nom=%s, description=%s WHERE id=%s'
                cur.execute(query, [nom, description, id])
                con.commit()

                flash('Catégorie modifier', 'success')
                return redirect(url_for('categorie_index'))

            # get file extension
            ext = logo.split('.')[1]
            if ext in ['png', 'jpg', 'jpeg']:
                # save image in target
                destination = '/'.join([target, logo])
                upload.save(destination)

                query = 'UPDATE categorie SET nom=%s,img=%s,  description=%s WHERE id=%s'
                cur.execute(query, [nom, logo, description, id])
                con.commit()

                flash('Catégorie modifier', 'success')
                return redirect(url_for('categorie_index'))

            flash(
                'Seuls les fichiers {png, jpg, jpeg} sont autorisés...', 'danger')
            return render_template('categorie/modifier.html')

    else:  # method == 'GET'
        query = ' SELECT * FROM categorie WHERE id=%s '
        cur.execute(query, [id])

        categorie = cur.fetchone()
        if categorie:
            return render_template('categorie/modifier.html', categorie=categorie)

        flash('Catégorie introuvable', 'danger')
        return redirect(url_for('categorie_index'))


@app.route('/categorie/supprimer/<string:id>', methods=['GET', 'POST'])
@login_required
def categorie_supprimer(id):
    con = open_connection()
    cur = con.cursor()

    query = ' SELECT * FROM categorie WHERE id=%s '
    cur.execute(query, [id])

    categorie = cur.fetchone()
    if categorie:
        query = ' DELETE FROM categorie WHERE id=%s '
        cur.execute(query, [id])
        con.commit()

        flash('Catégorie supprimer', 'success')
        return redirect(url_for('categorie_index'))

    flash('Catégorie introuvable', 'danger')
    return redirect(url_for('categorie_index'))

@app.route('/categorie/search')
@login_required
def categorie_search():
    keyword = request.args.get('keyword')

    str_keyword = '%'+keyword+'%'

    con = open_connection()
    cur = con.cursor()

    query = '''
        SELECT * 
        FROM categorie 
        WHERE nom LIKE %s 
        ORDER BY nom
    '''
    cur.execute(query, [str_keyword])

    categories = cur.fetchall()

    return render_template('categorie/result.html', categories=categories, keyword=keyword)

# gestion des clients

@app.route('/client')
@login_required
def client_index():
    con = open_connection()
    cur = con.cursor()

    query = ' SELECT * FROM client ORDER BY nom,prenom  '
    cur.execute(query)

    clients = cur.fetchall()

    return render_template('client/index.html', clients=clients)


@app.route('/client/details/<string:id>')
@login_required
def client_details(id):
    con = open_connection()
    cur = con.cursor()

    query = ''' 
            SELECT * FROM client WHERE id = %s
        '''

    cur.execute(query, [id])

    client = cur.fetchone()

    if client:
        return render_template('client/details.html', client=client)

    flash('client introuvable', 'danger')
    return redirect(url_for('client_index'))


@app.route('/client/ajouter', methods=['GET', 'POST'])
@login_required
def client_ajouter():
    if request.method == 'POST':

        nom = request.form['nom']
        prenom = request.form['prenom']
        date_naissance = request.form['date_naissance']
        tel = request.form['tel']
        email = request.form['email']
        pays = request.form['pays']
        ville = request.form['ville']
        adresse = request.form['adresse']

        con = open_connection()
        cur = con.cursor()

        query = '''
            INSERT INTO client( nom, prenom, date_naissance, tel, email, pays, ville, adresse) 
            VALUES( %s, %s, %s, %s, %s, %s, %s, %s)
            '''
        cur.execute(query, [nom, prenom, date_naissance,
                    tel, email, pays, ville, adresse])
        con.commit()

        flash('Client ajouté', 'success')
        return redirect(url_for('client_index'))

    # method == 'GET'
    return render_template('client/ajouter.html')


@app.route('/client/modifier/<string:id>', methods=['GET', 'POST'])
@login_required
def client_modifier(id):
    con = open_connection()
    cur = con.cursor()

    query = ''' 
            SELECT * FROM client WHERE id = %s
        '''

    cur.execute(query, [id])

    client = cur.fetchone()

    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        date_naissance = request.form['date_naissance']
        tel = request.form['tel']
        email = request.form['email']
        pays = request.form['pays']
        ville = request.form['ville']
        adresse = request.form['adresse']

        con = open_connection()
        cur = con.cursor()

        query = '''
            UPDATE client
            SET nom=%s, 
             prenom=%s,
             date_naissance=%s,
             tel=%s,
             email=%s,
             adresse=%s,
             ville=%s,
             pays=%s
            WHERE id=%s
            '''
        cur.execute(query, [nom, prenom, date_naissance,
                    tel, email, adresse, ville, pays, id])
        con.commit()

        flash('Client modifier', 'success')
        return redirect(url_for('client_details', id=id))

    if client:
        return render_template('client/modifier.html', client=client)

    flash('client introuvable', 'danger')
    return redirect(url_for('client_index'))


@app.route('/client/activer_desactiver/<string:id>/<string:etat>', methods=['POST'])
@login_required
def client_activer_desactiver(id, etat):
    con = open_connection()
    cur = con.cursor()

    query = ' SELECT * FROM client WHERE id=%s '
    cur.execute(query, [id])

    client = cur.fetchone()
    if client:
        print(id, etat)
        query = 'UPDATE client SET etat=%s WHERE id=%s'
        cur.execute(query, [etat, id])
        con.commit()

        if etat != '1':
            flash('client désactive', 'success')
        else:
            flash('client active', 'success')

        return redirect(url_for('client_details', id=id))

    flash('Client introuvable', 'danger')
    return redirect(url_for('client_index'))

@app.route('/client/search')
@login_required
def client_search():
    keyword = request.args.get('keyword')

    str_keyword = '%'+keyword+'%'

    con = open_connection()
    cur = con.cursor()

    query = '''
        SELECT * 
        FROM client 
        WHERE nom LIKE %s 
            OR prenom LIKE %s 
            OR email LIKE %s
            OR adresse LIKE %s
            OR ville LIKE %s
            OR pays LIKE %s
        ORDER BY nom,prenom
    '''
    cur.execute(query, [str_keyword, str_keyword, str_keyword, str_keyword, str_keyword, str_keyword])

    clients = cur.fetchall()

    return render_template('client/result.html', clients=clients, keyword=keyword)

# gestion des gammes


@app.route('/gamme')
@login_required
def gamme_index():
    con = open_connection()
    cur = con.cursor()

    query = ''' 
        SELECT * 
        FROM gamme 
        LEFT JOIN categorie ON gamme.id_categorie=categorie.id
        ORDER BY gamme.nom 
    '''
    cur.execute(query)

    gammes = cur.fetchall()

    return render_template('gamme/index.html', gammes=gammes)


@app.route('/gamme/ajouter', methods=['GET', 'POST'])
@login_required
def gamme_ajouter():
    con = open_connection()
    cur = con.cursor()

    if request.method == 'POST':

        categorie = request.form['categorie']
        gamme = request.form['gamme']
        description = request.form['description']

        # upload image
        for upload in request.files.getlist('img'):
            # get file name
            logo = upload.filename
            if logo == '':
                flash('svp, ajouter une image au gamme', 'danger')
                return render_template('gamme/ajouter.html')

            # get file extension
            ext = logo.split('.')[1]
            if ext in ['png', 'jpg', 'jpeg']:
                # save image in target
                destination = '/'.join([target, logo])

                upload.save(destination)

                query = 'INSERT INTO gamme(id_categorie, nom, img, description) VALUES(%s, %s, %s, %s)'
                cur.execute(query, [categorie, gamme, logo, description])
                con.commit()

                flash('gamme ajoutée', 'success')
                return redirect(url_for('gamme_index'))

            flash(
                'Seuls les fichiers {png, jpg, jpeg} sont autorisés...', 'danger')
            return render_template('gamme/ajouter.html')

    else:  # method == 'GET'
        query = '''
            SELECT * FROM categorie ORDER BY nom
        '''
        cur.execute(query)
        categories = cur.fetchall()

        return render_template('gamme/ajouter.html', categories=categories)


@app.route('/gamme/modifier/<string:id>', methods=['GET', 'POST'])
@login_required
def gamme_modifier(id):
    con = open_connection()
    cur = con.cursor()

    if request.method == 'POST':
        categorie = request.form['categorie']
        gamme = request.form['gamme']
        description = request.form['description']

        # upload image
        for upload in request.files.getlist('img'):
            # get file name
            logo = upload.filename
            if logo == '':
                query = 'UPDATE gamme SET id_categorie=%s, nom=%s, description=%s WHERE id=%s'
                cur.execute(query, [categorie, gamme, description, id])
                con.commit()

                flash('gamme modifiée', 'success')
                return redirect(url_for('gamme_index'))

            # get file extension
            ext = logo.split('.')[1]
            if ext in ['png', 'jpg', 'jpeg']:
                # save image in target
                destination = '/'.join([target, logo])
                upload.save(destination)

                query = 'UPDATE gamme SET id_categorie=%s, nom=%s,img=%s, description=%s WHERE id=%s'
                cur.execute(query, [categorie, gamme, logo, description, id])
                con.commit()

                flash('gamme modifiée', 'success')
                return redirect(url_for('gamme_index'))

            flash(
                'Seuls les fichiers {png, jpg, jpeg} sont autorisés...', 'danger')
            return render_template('gamme/modifier.html')

    else:  # method == 'GET'
        query = '''
            SELECT * FROM categorie ORDER BY nom
        '''
        cur.execute(query)
        categories = cur.fetchall()

        query = ' SELECT * FROM gamme WHERE id=%s '
        cur.execute(query, [id])

        gamme = cur.fetchone()
        if gamme:
            return render_template('gamme/modifier.html', gamme=gamme, categories=categories)

        flash('gamme introuvable', 'danger')
        return redirect(url_for('gamme_index'))


@app.route('/gamme/supprimer/<string:id>', methods=['GET', 'POST'])
@login_required
def gamme_supprimer(id):
    con = open_connection()
    cur = con.cursor()

    query = ' SELECT * FROM gamme WHERE id=%s '
    cur.execute(query, [id])

    gamme = cur.fetchone()
    if gamme:
        query = ' DELETE FROM gamme WHERE id=%s '
        cur.execute(query, [id])
        con.commit()

        flash('gamme supprimée', 'success')
        return redirect(url_for('gamme_index'))

    flash('gamme introuvable', 'danger')
    return redirect(url_for('gamme_index'))

@app.route('/gamme/search')
@login_required
def gamme_search():
    keyword = request.args.get('keyword')

    str_keyword = '%'+keyword+'%'

    con = open_connection()
    cur = con.cursor()

    query = '''
        SELECT * 
        FROM gamme 
        LEFT JOIN categorie ON gamme.id_categorie=categorie.id
        WHERE gamme.nom  LIKE %s 
            OR categorie.nom LIKE %s
        ORDER BY gamme.nom
    '''
    cur.execute(query, [str_keyword, str_keyword])

    gammes = cur.fetchall()

    return render_template('gamme/result.html', gammes=gammes, keyword=keyword)

#gestion des produits


@app.route('/produit')
@login_required
def produit_index():
    con = open_connection()
    cur = con.cursor()

    query = ''' 
        SELECT * 
        FROM produit
        LEFT JOIN gamme ON produit.id_gamme=gamme.id
        LEFT JOIN categorie ON gamme.id_categorie=categorie.id
        ORDER BY produit.nom
    '''
    cur.execute(query)

    produits = cur.fetchall()

    return render_template('produit/index.html', produits=produits)


@app.route('/produit/details/<string:id>')
@login_required
def produit_details(id):
    con = open_connection()
    cur = con.cursor()

   
   
    query = ''' 
            SELECT * 
            FROM produit
            LEFT JOIN gamme ON produit.id_gamme=gamme.id
            LEFT JOIN categorie ON gamme.id_categorie=categorie.id
            WHERE produit.id = %s
            
        '''

    cur.execute(query, [id])

    produit = cur.fetchone()

    if produit:
        return render_template('produit/details.html', produit=produit)

    flash('produit introuvable', 'danger')
    return redirect(url_for('produit_index'))

@app.route('/produit/ajouter', methods=['GET', 'POST'])
@login_required
def produit_ajouter():
    con = open_connection()
    cur = con.cursor()

    if request.method == 'POST':
        
        gamme = request.form['gamme']
        produit = request.form['produit']
        description = request.form['description']
        qte_stock = request.form['qte_stock']
        prix_unitaire = request.form['prix_unitaire']
        volume_bouteille = request.form['volume_bouteille']
        
        
        

        # upload image
        for upload in request.files.getlist('img'):
            # get file name
            logo = upload.filename
            if logo == '':
                flash('svp, ajouter une image à produit', 'danger')
                return render_template('produit/ajouter.html')

            # get file extension
            ext = logo.split('.')[1]
            if ext in ['png', 'jpg', 'jpeg']:
                # save image in target
                destination = '/'.join([target, logo])

                upload.save(destination)

                query = 'INSERT INTO produit(id_gamme, nom, img, description, qte_stock, prix_unitaire, volume_bouteille) VALUES(%s, %s, %s, %s,  %s,  %s, %s)'
                cur.execute(query, [gamme, produit, logo, description, qte_stock, prix_unitaire, volume_bouteille])
                con.commit()

                flash('produit ajoutée', 'success')
                return redirect(url_for('produit_index'))

            flash(
                'Seuls les fichiers {png, jpg, jpeg} sont autorisés...', 'danger')
            return render_template('produit/ajouter.html')

    else:  # method == 'GET'
        query = '''
            SELECT * FROM gamme ORDER BY nom
        '''
        cur.execute(query)
        gammes = cur.fetchall()

        return render_template('produit/ajouter.html', gammes=gammes)

@app.route('/produit/modifier/<string:id>', methods=['GET', 'POST'])
@login_required
def produit_modifier(id):
    con = open_connection()
    cur = con.cursor()

    if request.method == 'POST':
        gamme = request.form['gamme']
        produit = request.form['produit']
        description = request.form['description']
        qte_stock = request.form['qte_stock']
        prix_unitaire = request.form['prix_unitaire']
        volume_bouteille = request.form['volume_bouteille']

        # upload image
        for upload in request.files.getlist('img'):
            # get file name
            logo = upload.filename
            if logo == '':
                query = 'UPDATE gamme SET id_gamme=%s, nom=%s, description=%s, qte_stock=%s, prix_unitaire=%s, volume_bouteille=%s WHERE id=%s'
                cur.execute(query, [ gamme, produit, description, qte_stock, prix_unitaire, volume_bouteille, id])
                con.commit()

                flash('produit modifié', 'success')
                return redirect(url_for('produit_index'))

            # get file extension
            ext = logo.split('.')[1]
            if ext in ['png', 'jpg', 'jpeg']:
                # save image in target
                destination = '/'.join([target, logo])
                upload.save(destination)

                query = 'UPDATE gamme SET id_gamme=%s, nom=%s, img=%s, description=%s, qte_stock=%s, prix_unitaire=%s, volume_bouteille=%s WHERE id=%s'
                cur.execute(query, [gamme, produit, logo, description, qte_stock, prix_unitaire, volume_bouteille, id])
                con.commit()

                flash('produit modifié', 'success')
                return redirect(url_for('produit_index'))

            flash(
                'Seuls les fichiers {png, jpg, jpeg} sont autorisés...', 'danger')
            return render_template('produit/modifier.html')

    else:  # method == 'GET'
        query = '''
            SELECT * FROM gamme ORDER BY nom
        '''
        cur.execute(query)
        gammes = cur.fetchall()

        query = ' SELECT * FROM produit WHERE id=%s '
        cur.execute(query, [id])

        produit = cur.fetchone()
        if produit:
            return render_template('produit/modifier.html', produit=produit, gammes=gammes)

        flash('produit introuvable', 'danger')
        return redirect(url_for('produit_index'))

@app.route('/produit/supprimer/<string:id>', methods=['GET', 'POST'])
@login_required
def produit_supprimer(id):
    con = open_connection()
    cur = con.cursor()

    query = ' SELECT * FROM produit WHERE id=%s '
    cur.execute(query, [id])

    produit = cur.fetchone()
    if produit:
        query = ' DELETE FROM produit WHERE id=%s '
        cur.execute(query, [id])
        con.commit()

        flash('produit supprimé', 'success')
        return redirect(url_for('produit_index'))

    flash('produit introuvable', 'danger')
    return redirect(url_for('produit_index'))

@app.route('/produit/search')
@login_required
def produit_search():
    keyword = request.args.get('keyword')

    str_keyword = '%'+keyword+'%'

    con = open_connection()
    cur = con.cursor()

    query = '''
        SELECT * 
        FROM produit
        LEFT JOIN gamme ON produit.id_gamme=gamme.id
        LEFT JOIN categorie ON gamme.id_categorie=categorie.id
        WHERE produit.nom LIKE %s 
            OR gamme.nom  LIKE %s 
            OR categorie.nom LIKE %s
            OR qte_stock	 LIKE %s
            OR prix_unitaire  LIKE %s
            OR volume_bouteille	 LIKE %s
        ORDER BY produit.nom     
    '''
    cur.execute(query, [str_keyword, str_keyword, str_keyword, str_keyword, str_keyword, str_keyword])

    produits = cur.fetchall()

    return render_template('produit/result.html', produits=produits, keyword=keyword)

#gestion des réclamtions

@app.route('/reclamation')
@login_required
def reclamation_index():
    con = open_connection()
    cur = con.cursor()

    query = ''' 
        SELECT * 
        FROM reclamation 
        LEFT JOIN client ON reclamation.id_client=client.id
        ORDER BY reclamation.date_creation
    '''
    cur.execute(query)

    reclamations = cur.fetchall()

    return render_template('reclamation/index.html', reclamations=reclamations)


@app.route('/reclamation/supprimer/<string:id>', methods=['GET', 'POST'])
@login_required
def reclamation_supprimer(id):
    con = open_connection()
    cur = con.cursor()

    query = ' SELECT * FROM reclamation WHERE id=%s '
    cur.execute(query, [id])

    reclamation = cur.fetchone()
    if reclamation:
        query = ' DELETE FROM reclamation WHERE id=%s '
        cur.execute(query, [id])
        con.commit()

        flash('réclamation supprimée', 'success')
        return redirect(url_for('reclamation_index'))

    flash('reclamation introuvable', 'danger')
    return redirect(url_for('reclamation_index'))

@app.route('/reclamation/details/<string:id>')
@login_required
def reclamation_details(id):
    con = open_connection()
    cur = con.cursor()

   
   
    query = ''' 
            SELECT * 
            FROM reclamation
            LEFT JOIN client ON reclamation.id_client=client.id
            WHERE reclamation.id = %s
            
        '''

    cur.execute(query, [id])

    reclamation = cur.fetchone()

    if reclamation:
        return render_template('reclamation/details.html', reclamation=reclamation)

    flash('reclamation introuvable', 'danger')
    return redirect(url_for('reclamation_index'))

@app.route('/reclamation/search')
@login_required
def reclamation_search():
    keyword = request.args.get('keyword')

    str_keyword = '%'+keyword+'%'

    con = open_connection()
    cur = con.cursor()

    query = '''
        SELECT * 
        FROM reclamation
        LEFT JOIN client ON reclamation.id_client=client.id
        
        WHERE reclamation.id LIKE %s 
            OR client.nom  LIKE %s 
            OR client.prenom LIKE %s
            OR sens  LIKE %s
            OR date_creation  LIKE %s
           
        ORDER BY reclamation.id   
    '''
    cur.execute(query, [str_keyword, str_keyword, str_keyword, str_keyword, str_keyword])

    reclamations = cur.fetchall()

    return render_template('reclamation/result.html', reclamations=reclamations, keyword=keyword)


#gestion des questions 

@app.route('/question')
@login_required
def question_index():
    con = open_connection()
    cur = con.cursor()

    query = ''' 
        SELECT * 
        FROM question
        LEFT JOIN client ON question.id_client=client.id
        ORDER BY question.date_creation
    '''
    cur.execute(query)

    questions = cur.fetchall()

    return render_template('question/index.html', questions=questions)

@app.route('/question/details/<string:id>')
@login_required
def question_details(id):
    con = open_connection()
    cur = con.cursor()

   
   
    query = ''' 
            SELECT * 
            FROM question
            LEFT JOIN client ON question.id_client=client.id
            WHERE question.id = %s
            
        '''

    cur.execute(query, [id])

    question = cur.fetchone()

    if question:
        return render_template('question/details.html', question=question)

    flash('question introuvable', 'danger')
    return redirect(url_for('question_index'))


@app.route('/question/supprimer/<string:id>', methods=['GET', 'POST'])
@login_required
def question_supprimer(id):
    con = open_connection()
    cur = con.cursor()

    query = ' SELECT * FROM question WHERE id=%s '
    cur.execute(query, [id])

    question = cur.fetchone()
    if question:
        query = ' DELETE FROM question WHERE id=%s '
        cur.execute(query, [id])
        con.commit()

        flash('question supprimée', 'success')
        return redirect(url_for('question_index'))

    flash('question introuvable', 'danger')
    return redirect(url_for('question_index'))

@app.route('/question/search')
@login_required
def question_search():
    keyword = request.args.get('keyword')

    str_keyword = '%'+keyword+'%'

    con = open_connection()
    cur = con.cursor()

    query = '''
        SELECT * 
        FROM question
        LEFT JOIN client ON question.id_client=client.id
        
        WHERE question.id LIKE %s 
            OR client.nom  LIKE %s 
            OR client.prenom LIKE %s
            OR date_creation  LIKE %s
           
        ORDER BY question.id   
    '''
    cur.execute(query, [str_keyword, str_keyword, str_keyword, str_keyword])

    questions = cur.fetchall()

    return render_template('question/result.html', questions=questions, keyword=keyword)

#gestion des commandes

@app.route('/commande')
@login_required
def commande_index():
    con = open_connection()
    cur = con.cursor()

    query = ''' 
        SELECT * 
        FROM commande
        LEFT JOIN client ON commande.id_client=client.id
        ORDER BY commande.date_creation
    '''
    cur.execute(query)

    commandes = cur.fetchall()

    return render_template('commande/index.html', commandes=commandes)


@app.route('/commande/modifier/<string:id>', methods=['GET', 'POST'])
@login_required
def commande_modifier(id):
    con = open_connection()
    cur = con.cursor()

   

    if request.method == 'POST':
        Nom_Client = request.form['Nom_Client']
        Prenom_Client = request.form['Prenom_Client']
        Date_Creation= request.form['Date_Creation']
        Total = request.form['Total']
        État = request.form['État']

        

        query = '''
            UPDATE commande
            SET nom=%s, 
            Prenom =%s,
            date_creation=%s,
            total_commande=%s,
            etat=%s
            WHERE id=%s
            '''
        cur.execute(query, [Nom_Client, Prenom_Client, Date_Creation, Total, État, id])
        con.commit()

        flash('Commande modifiée', 'success')
        return redirect(url_for('commnande_modifier', id=id))
    else:  # method == 'GET'
        query = '''
            SELECT * FROM client ORDER BY nom
        '''
        cur.execute(query)
        clients = cur.fetchall()

        query = ' SELECT * FROM commande WHERE id=%s '
        cur.execute(query, [id])

        commande = cur.fetchone()
        if commande:
            return render_template('commande/modifier.html', commande=commande, cliens=clients)

        flash('commande introuvable', 'danger')
        return redirect(url_for('commande_index'))
  

@app.route('/commande/supprimer/<string:id>', methods=['GET', 'POST'])
@login_required
def commande_supprimer(id):
    con = open_connection()
    cur = con.cursor()

    query = ' SELECT * FROM commande WHERE id=%s '
    cur.execute(query, [id])

    commande = cur.fetchone()
    if commande:
        query = ' DELETE FROM commande WHERE id=%s '
        cur.execute(query, [id])
        con.commit()

        flash('Commande supprimée', 'success')
        return redirect(url_for('commande_index'))

    flash(' commande introuvable', 'danger')
    return redirect(url_for('commande_index'))      

@app.route('/commande/search')
@login_required
def commande_search():
    keyword = request.args.get('keyword')

    str_keyword = '%'+keyword+'%'

    con = open_connection()
    cur = con.cursor()

    query = '''
        SELECT * 
        FROM commande
        LEFT JOIN client ON commande.id_client=client.id
        
        WHERE commande.id LIKE %s 
            OR client.nom  LIKE %s 
            OR client.prenom LIKE %s
            OR date_creation  LIKE %s
            OR total_commande  LIKE %s
            OR commande.etat  LIKE %s
   
        ORDER BY commande.id   
    '''
    cur.execute(query, [str_keyword, str_keyword, str_keyword, str_keyword, str_keyword, str_keyword])

    commandes = cur.fetchall()

    return render_template('commande/result.html', commandes=commandes, keyword=keyword)

#gestion des factures

@app.route('/facture')
@login_required
def facture_index():
    con = open_connection()
    cur = con.cursor()

    query = ''' 
        SELECT * 
        FROM facture
        LEFT JOIN commande ON facture.id_commande=commande.id
        LEFT JOIN client ON commande.id_client=client.id
        
    '''
    cur.execute(query)

    factures = cur.fetchall()

    return render_template('facture/index.html', factures=factures)

@app.route('/facture/modifier/<string:id>', methods=['GET', 'POST'])
@login_required
def facture_modifier(id):
    con = open_connection()
    cur = con.cursor()

   

    if request.method == 'POST':
       
        Total = request.form['Total']
        Date_Reglement = request.form['Date_Reglement']
        moyen_paiement = request.form['moyen_paiement']

        con = open_connection()
        cur = con.cursor()

        query = '''
            UPDATE facture
            SET sous_total=%s,
             date_reglement=%s,
             moyen_paiement=%s
            WHERE id=%s
            '''
        cur.execute(query, [Total,  Date_Reglement, moyen_paiement, id])
        con.commit()

        flash('Facture modifiée', 'success')
        return redirect(url_for('facture_modifier', id=id))
    
    
    else:  # method == 'GET' 
    
     query = '''
            SELECT * FROM commande ORDER BY id
        '''
     cur.execute(query)
     commandes = cur.fetchall()

     query = ' SELECT * FROM facture WHERE id=%s '
     cur.execute(query, [id])

     facture = cur.fetchone()

    if facture:
        return render_template('facture/modifier.html', facture=facture, commandes=commandes)

    flash('Facture introuvable', 'danger')
    return redirect(url_for('facture_index'))

@app.route('/facture/ajouter', methods=['GET', 'POST'])
@login_required
def facture_ajouter():
    con = open_connection()
    cur = con.cursor()

    if request.method == 'POST':
        
        Total = request.form['Total']
        Date_Reglement = request.form['Date_Reglement']
        moyen_paiement = request.form['moyen_paiement']
        Num_Commande = request.form['Num_Commande']

       
        query = '''
            INSERT INTO facture(sous_total, date_reglement, moyen_paiement, id_commande) 
            VALUES(%s, %s, %s, %s)
            '''
        cur.execute(query, [Total, Date_Reglement, moyen_paiement, Num_Commande])
        con.commit()
        

        flash('facture ajoutée', 'success')
        return redirect(url_for('facture_index'))

    else:  # method == 'GET'
        query = '''
            SELECT * FROM commande 
        '''
        cur.execute(query)
        commandes = cur.fetchall()

        return render_template('facture/ajouter.html', commandes=commandes)

@app.route('/facture/supprimer/<string:id>', methods=['GET', 'POST'])
@login_required
def facture_supprimer(id):
    con = open_connection()
    cur = con.cursor()

    query = ' SELECT * FROM facture WHERE id=%s '
    cur.execute(query, [id])

    facture = cur.fetchone()
    if facture:
        query = ' DELETE FROM facture WHERE id=%s '
        cur.execute(query, [id])
        con.commit()

        flash('Facture supprimée', 'success')
        return redirect(url_for('facture_index'))

    flash(' facture introuvable', 'danger')
    return redirect(url_for('facture_index'))      

if __name__ == '__main__':
        app.run()
