from flask import Flask, request
from flask_pymongo import PyMongo
from Users.user_service import UserService
from Users.user_storage import UserStorage

from models.Adress import Adress
from models.User import User

app = Flask(__name__)

mongo_client = PyMongo(app, uri="mongodb://localhost:27017/BLOG")

users_storage = UserStorage(mongo_client)
users_service = UserService(users_storage)


@app.route('/')
def index():
    return 'HELLO THİS İS INDEX PAGE'


@app.route('/register', methods=['POST'])
def register():
    response = request.get_json()
    name = response['name']
    surname = response['surname']
    email = response['email']
    password = response['password']
    city = response['city']
    street = response['street']
    building = response['building']
    zip_code = response['zip_code']
    adress = Adress(city, street, building, zip_code)
    user = User(name, surname, email, password, adress)

    res = users_service.service_insert(user)
    return {'id': res}


@app.route('/login', methods=['POST'])
def login():
    response = request.get_json()
    email = response['email']
    password = response['password']

    user = users_service.service_get_user_by_email(email)
    if user:
        print(user.get_name())
    return ''


if __name__ == '__main__':
    app.secret_key = 'secret_key'
    app.run(debug=True, host='127.0.0.1', port=3000)
