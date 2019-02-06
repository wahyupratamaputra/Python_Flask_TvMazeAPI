from sqlalchemy import or_, and_
from db.base import DbManager
from db.models import User, Film, Like
import json, requests



def download_data(query):
    db = DbManager()
    datas = json.loads(requests.get("http://api.tvmaze.com/search/shows?q={}".format(query)).text)
    for data in datas:
        try:
            savingdata = Film()
            savingdata.parse(data['show'])
            db.save(savingdata)
            
            print('-> created Film in db')
        except:
            print('data exist')
        
    db.close()

def search_film_by_name(query):
    db = DbManager()
    films = db.open().query(Film).filter(Film.name.like("%{}%".format(query))).all()

    db.close()
    return films

def like_film(user_id, film_id):
    db = DbManager()
    like = Like()
    like.user_id = user_id
    like.film_id = film_id
    return db.save(like)

def dislike_film(user_id, film_id):
    db = DbManager()
    return db.delete(db.open().query(Like).filter(Like.user_id == user_id, Like.film_id == film_id).one())

def check_like(user_id, film_id):
    db = DbManager()
    try:
        db.open().query(Like).filter(Like.user_id == user_id, Like.film_id == film_id).one()
    except:
        like_film(user_id, film_id)
    return db.close()
    

def get_liked_film(user_id):
    db = DbManager()
    return db.open().query(Like).filter(Like.user_id == user_id).all()

def create_user(email, username, password):
    db = DbManager()
    user = User()
    user.username = username
    user.email = email
    user.password = password
    return db.save(user)
    

def check_login(email, password):
    db = DbManager()
    return db.open().query(User).filter(User.email == email, User.password == password).one()

