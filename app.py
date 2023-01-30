from datetime import datetime, timedelta
from flask import Flask, request, jsonify
import psycopg2
import jwt
from functools import wraps


from users.user_services import UserService
from users.user_storages import UserPostgreStorage
from posts.post_services import PostService
from posts.post_storages import PostPostgreStorage
from models.adress import Adress
from models.user import User
from models.post import Post

app = Flask(__name__)

connection = psycopg2.connect(
    database="blog",
    user="postgres",
    password="Busem1220",
    host="localhost",
    port='5432'
)

# User service and user postgre storage created
user_storage = UserPostgreStorage(connection)
user_service = UserService(user_storage)
# Post service and post postgre storage created
post_storage = PostPostgreStorage(connection)
post_service = PostService(post_storage)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]
        if not token:
            return jsonify({'message': 'Token is missing !'}), 401
        try:
            data = jwt.decode(token, key=app.secret_key)
            current_user, current_id = user_service.get_user_by_id(data['id'])
        except:
            return jsonify({'message': 'Token is invalid !'}), 401

        return f(current_user, current_id, *args, **kwargs)
    return decorated


@app.route('/')
def index():
    return 'This is Index Page'


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

    user = User(name, surname, email, password)
    user_id = user_service.create_user(user)
    adress = Adress(city, street, building, zip_code, int(user_id))
    user_service.create_user_adress(adress)
    return user_id


@app.route('/login', methods=['POST'])
def login():
    response = request.get_json()
    email = response['email']
    candidate_password = response['password']
    user, user_id = user_service.get_user_by_email(email)
    if user:
        if user_service.check_password(user, candidate_password):
            return create_token(user_id, user.name, user.email)
        else:
            return jsonify({'message': 'Please check your password'})
    else:
        return jsonify({'message': 'User not found'})


@app.route('/user/post', methods=['GET', 'POST'])
@token_required
def post(current_user, current_id):
    if request.method == 'GET':
        output = post_service.get_all_own_post(current_id)
        return jsonify({'posts': output})

    if request.method == 'POST':
        response = request.get_json()
        title = response['title']
        text = response['content']
        post = Post(title, text, current_id)
        post_id = post_service.create_post(post)
        return post_id


@app.route('/user/post/<post_id>', methods=['DELETE', 'PUT'])
@token_required
def delete_or_update_post(current_user, current_id, post_id):
    if request.method == 'DELETE':
        if post_service.get_post_by_id(post_id):
            return str(post_id)
        return jsonify({'message': 'Post not found for delete'})

    if request.method == 'PUT':
        response = request.get_json()
        title = response['title']
        content = response['content']
        if post_service.update_post(title, content, post_id):
            return jsonify({'message': 'success'})
        else:
            return jsonify({'message': 'Post not found for update'})


@app.route('/user')
@token_required
def user(current_user, current_id):
    return jsonify({'id': current_id, 'name': current_user.name, 'surname': current_user.surname, 'email': current_user.email})


def create_token(user_id, user_name, user_email):
    token = jwt.encode({
        'id': user_id,
        'user_email': user_email,
        'user_name': user_name
    }, key=app.secret_key).decode('UTF-8')
    return token


if __name__ == '__main__':
    app.secret_key = 'secret_key'
    app.run(debug=True, host='127.0.0.1', port=3000)
