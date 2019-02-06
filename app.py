import re
from flask import Flask, session, request, redirect, render_template, flash, url_for
import json, pprint, requests
import db.data_layer as db
from db.data_layer import create_user, check_login, download_data, search_film_by_name, like_film, get_liked_film, dislike_film, check_like



EMAIL_REGEX = re.compile(r'^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$')

app = Flask(__name__)
app.secret_key = '0d599f0ec05c3bda8c3b8a68c32a1b47'

@app.route('/')
def index():
    if 'user_id' in session: #check if user not yet login
        likes = get_liked_film(session['user_id'])
        return render_template('index.html', likes = likes)
    return render_template('index.html')

@app.route('/search')
def search():
    return redirect(url_for('search_films', query=request.args['html_query']))
    
@app.route('/results/<query>')
def search_films(query):
    
    liked = []
    download_data(query)
    films = search_film_by_name(query)
    if 'user_id' in session:
        likeds = get_liked_film(session['user_id'])
        for like in likeds:
            liked.append(like.film_id)

    print(liked)
    return render_template('index.html', films = films, liked = liked)

@app.route('/like/<film_id>')
def like(film_id):
    user_id = session['user_id']
    check_like(user_id, film_id)


    return redirect('/') 

@app.route('/like/<film_id>/<user_id>')
def checklike(film_id, user_id):
    check = check_like(film_id, user_id)

    return check

@app.route('/dislike/<user_id>/<film_id>')
def dislike(user_id, film_id):
    dislike_film(user_id, film_id)

    return redirect('/') 

@app.route('/authenticate')
def authenticate():
    pass

@app.route('/register', methods=["GET", "POST"])
def register():
    if 'user_id' not in session: #check if user not yet login
        if request.method == 'POST':
            username = request.form.get("username")
            email = request.form.get("email")
            password = request.form.get("password")
            confirm = request.form.get("confirm")
            if password == confirm:
                if len(password)>7:
                    if EMAIL_REGEX.match(email):
                            user = create_user(email, username, password)
                            session['user_id'] = user.id
                            session['username'] = user.email
                            return redirect('/')
                    else:
                        flash("Please input correct email")
                        return redirect('/register') 
                else:
                    flash("password minimum 8 char")
                    return redirect('/register') 
            else:
                flash("password must be same with confirm")
                return redirect('/register') 

        else:
            return render_template('page_register.html')


    return redirect('/') #redirect if already login


@app.route('/login', methods=["GET", "POST"])
def login():
    if 'user_id' not in session: #check if user not yet login
        if request.method == 'POST':
            email = request.form.get("email")
            password = request.form.get("password")
            try:
                user = check_login(email, password)
                session['user_id'] = user.id
                session['username'] = user.username
                return redirect('/')
            except:
                flash("email or password not found")
                return redirect('/login') 
                
        else:
            return render_template('page_login.html')

    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('index'))

def setup_web_session(user):
    pass


app.run(debug=True)