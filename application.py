#!/usr/bin/env python
# This modules contains all the routes for the functioning
# of the application.

from flask import Flask, render_template, request, redirect, url_for
from flask import flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Categories, TopSelections, User
from flask import session as login_session
from flask import make_response
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
# from oauth2client.client import AccessTokenCredentials
import random
import string
import httplib2
import json
import requests

app = Flask(__name__)

# google client secret
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "PerfumesCatalogApp"

# Connect to the database and create a database session.
engine = create_engine('sqlite:///catalog.db?check_same_thread=False')
Base.metadata.bind = engine

# Bind the above engine to a session.
DBSession = sessionmaker(bind=engine)

# Create a Session object.
session = DBSession()


# Create anti forgery state token and store it in the session for validation
@app.route('/login')
def new_state():
    state = ''.join(random.choice(string.ascii_uppercase + string.
                    digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# google signin function
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validating state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtaining authorization code
    code = request.data
    try:
        # Upgrade the authorization code to the credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the \
        authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
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
            json.dumps("Token's Client ID does not match app's."), 401)
        print "Token's Client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response
    # Check if the user is already logged in
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already \
        connected.'),
                                 200)
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
    login_session['provider'] = 'google'

    # See if a user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += login_session['email']
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: \
    150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    # flash("Welcome %s" % login_session['username'])
    # print "done!"
    return output


# logout the user
@app.route('/logout', methods=['post'])
def logout():
    # Disconnect based on provider
    if login_session.get('provider') == 'google':
        if gdisconnect():
            flash("You have successfully logged out")
            return redirect(url_for('index'))
    else:
        response = make_response(json.dumps({'state': 'notConnected'}),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not \
        connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
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
        login_session['provider'] = 'null'
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        # response.headers['Content-Type'] = 'application/json'
        # return response
        flash("You have successfully logged out")
        return redirect(url_for('index'))
    else:
        # if the given token was invalid
        print "this is the status " + result['status']
        response = make_response(json.dumps('Failed to revoke token for given \
        user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Adding new user into database
def createUser(login_session):
    name = login_session['name']
    email = login_session['email']
    url = login_session['img']
    provider = login_session['provider']
    newUser = User(name=name, email=email, picture=url, provider=provider)
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


# User Helper Functions
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


# validating current loggedin user
def check_user():
    email = login_session['email']
    return session.query(User).filter_by(email=email).one_or_none()


# retreive admin user details
def check_admin():
    return session.query(User).filter_by(
        email='hebaahmadms@gmail.com').one_or_none()


def queryAllCategories():
    return session.query(TopSelections).all()


# Main page
@app.route('/')
@app.route('/catalog')
def index():
    perfumes = session.query(Categories).all()
    favorite = session.query(TopSelections).order_by(
            TopSelections.id.desc()).limit(7)
    if 'username' not in login_session:
        # flash("Please login")
        return render_template(
            'publichome.html', perfumes=perfumes, favorite=favorite)
    else:
        flash("Welcome %s" % login_session['username'])
        return render_template(
            'home.html', perfumes=perfumes, favorite=favorite)


# Show the top choices in a particular category.
@app.route('/catalog/<int:perfume_id>/favorite/')
def favorite_perfumes(perfume_id):
    """ Show the best perfumes favorites in a particular category."""
    if not check_category(perfume_id):
        flash("We are unable to process your request right now.")
        return redirect(url_for('index'))
    allfragrances = session.query(Categories).all()
    fragrance = session.query(Categories).filter_by(id=perfume_id).first()
    favorite = session.query(TopSelections).filter_by(
            perfume_id=fragrance.id).all()
    total = session.query(TopSelections).filter_by(
            perfume_id=fragrance.id).count()
    owner = session.query(User).filter_by(id=TopSelections.user_id).first()
    if 'username' not in login_session:
        flash("Please login")
        return render_template(
            'publicperfumes.html', allfragrances=allfragrances,
            fragrance=fragrance, favorite=favorite, total=total, owner=owner)
    else:
        return render_template(
            'topperfumes.html', allfragrances=allfragrances,
            fragrance=fragrance, favorite=favorite, total=total, owner=owner)


# Show more info of particular perfume by its ID in a new page
@app.route('/catalog/<int:perfume_id>/favorite/<int:favorite_id>/more_info')
def moreInfo(perfume_id, favorite_id):
    if check_perfume(favorite_id):
        favorite = session.query(TopSelections).filter_by(
                id=favorite_id).first()
        fragrance = session.query(Categories).filter_by(
            id=favorite.perfume_id).first()
        owner = session.query(User).filter_by(id=favorite.user_id).first()
        return render_template(
            'moreInfo.html', fragrance=fragrance,
            favorite=favorite, owner=owner)
    else:
        flash('We are unable to process your request right now.')
        return redirect(url_for('index'))


# Create new Perfumes by Category ID.
@app.route('/catalog/<int:perfume_id>/addperfume', methods=['GET', 'POST'])
def add_Perfume(perfume_id):
    allfragrances = session.query(Categories).all()
    fragrance = session.query(Categories).filter_by(id=perfume_id).first()
    if 'username' not in login_session:
        flash("Please signin to continue!")
        return redirect('/login')
    elif request.method == 'POST':
        # check if the perfume name already exist
        favorite = session.query(TopSelections).filter_by(
                name=request.form['name']).first()
        if favorite:
            if favorite.name == request.form['name']:
                flash('this perfume already exists')
                return redirect(url_for(
                    'add_Perfume', perfume_id=fragrance.id))
            elif request.form['name'] == '':
                flash('The field cannot be empty.')
                return redirect(url_for(
                    'add_Perfume', perfume_id=fragrance.id))
        newPerfume = TopSelections(
            name=request.form['name'], description=request.form['description'],
            perfume_id=request.form['category'], user_id=check_user().id)
        session.add(newPerfume)
        session.commit()
        flash("New Perfume %s Successfully Added" % (newPerfume.name))
        return redirect(url_for('favorite_perfumes', perfume_id=perfume_id))
    else:
        return render_template(
            'addPerfume1.html', perfume_id=perfume_id,
            fragrance=fragrance, allfragrances=allfragrances)


# create function for checking if the perfume's name exists or not
def check_perfume(favorite_id):
    favorite = session.query(TopSelections).filter_by(id=favorite_id).first()
    if favorite is not None:
        return True
    else:
        return False


# create function for checking if the fragrance's category exists or not
def check_category(perfume_id):
    category = session.query(Categories).filter_by(id=perfume_id).first()
    if category is not None:
        return True
    else:
        return False


@app.route(
    '/catalog/<int:perfume_id>/<int:favorite_id>/editfavorite',
    methods=['GET', 'POST'])
def edit_favorite(perfume_id, favorite_id):
    allfragrances = session.query(Categories).all()
    fragrance = session.query(Categories).filter_by(id=perfume_id).first()
    editedPerfume = session.query(TopSelections).filter_by(
            id=favorite_id).one()
    if 'username' not in login_session:
        flash("Please Login to continue!")
        return redirect('/login')
    elif not check_perfume(favorite_id):
        flash("The Required Perfume not exist")
        return redirect('index')
    elif editedPerfume.user_id != (check_user().id or check_admin().id):
        flash("You are not authorise to access this page")
        return redirect('index')
    elif request.method == 'POST':
        if request.form['name']:
            editedPerfume.name = request.form['name']
        if request.form['description']:
            editedPerfume.description = request.form['description']
        if request.form['category']:
            editedPerfume.perfume_id = request.form['category']
        session.add(editedPerfume)
        session.commit()
        flash("%s has been edited" % editedPerfume.name)
        return redirect(url_for('favorite_perfumes', perfume_id=perfume_id))
    else:
        return render_template(
            'editPerfume.html', perfume_id=perfume_id,
            favorite_id=favorite_id, i=editedPerfume, fragrance=fragrance,
            allfragrances=allfragrances)


@app.route(
    '/catalog/<int:perfume_id>/<int:favorite_id>/deletefavorite',
    methods=['GET', 'POST'])
def delete_favorite(perfume_id, favorite_id):
    allfragrances = session.query(Categories).all()
    fragrance = session.query(Categories).filter_by(id=perfume_id).first()
    deletedPerfume = session.query(TopSelections).filter_by(
            id=favorite_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    elif deletedPerfume.user_id != (check_user().id or check_admin().id):
        flash("You are not authorise to access this page")
        return redirect('index')
    if request.method == 'POST':
        session.delete(deletedPerfume)
        session.commit()
        flash("%s has been Deleted" % deletedPerfume.name)
        return redirect(url_for('favorite_perfumes', perfume_id=perfume_id))
    else:
        return render_template(
            'deletePerfume.html', perfume_id=perfume_id,
            favorite_id=favorite_id, i=deletedPerfume,
            fragrance=fragrance, allfragrances=allfragrances)


# Making JSON Endpoint

# Return JSON of all the categories in the catalog.
@app.route('/catalog/JSON')
def catalogJSON():
    categories = session.query(Categories).all()
    return jsonify(Categories=[e.serialize for e in categories])


# Return JSON of all the items in the catalog.
@app.route('/catalog/<int:perfume_id>/favorites/JSON')
def top_favoritesJSON(perfume_id):
    favorites = session.query(TopSelections).order_by(TopSelections.id.desc())
    return jsonify(Favorites=[i.serialize for i in favorites])


@app.route(
    '/catalog/<int:perfume_id>/favorite/<int:favorite_id>/more_info/JSON')
def more_infoJSON(perfume_id, favorite_id):
    if check_category(perfume_id) and check_perfume(favorite_id):
        favorite = session.query(TopSelections).filter_by(
            id=favorite_id, perfume_id=perfume_id).first()
        if favorite is not None:
            return jsonify(favorite=favorite.serialize)
        else:
            return jsonify(error='perfume {} does not belong to \
            category {}'.format(favorite_id, perfume_id))
    else:
        return jsonify(error="the perfume or the category doesn't exist")


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
