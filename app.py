from datetime import datetime, timedelta
from flask import Flask, request, jsonify
import psycopg2
import jwt
from functools import wraps


from users.user_services import UserService
from users.user_storages import UserPostgreStorage
from posts.post_services import PostService
from posts.post_storages import PostPostgreStorage
from comments.comment_services import CommentService
from comments.comment_storages import CommentPostgreStorage
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
# Comment service and comment postgre storage created
comment_storage = CommentPostgreStorage(connection)
comment_service = CommentService(comment_storage)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'Authorization' not in request.headers:
            raise Exception('There is no any Authorization')
        token = request.headers['Authorization'].split(' ')[1]
        try:
            decode_token = jwt.decode(token, key=app.secret_key)
            current_user = user_service.get_user_by_id(decode_token['id'])
        except:
            Exception('token could not decode')
        return f(current_user, *args, **kwargs)
    return decorated


@app.route('/')
def index():
    return post_service.get_all_posts()


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
    user: User = user_service.get_user_by_email(email)
    if user is not None:
        if user_service.check_password(user, candidate_password):
            return create_token(user.id, user.name, user.email)
        raise Exception('Check your password')
    raise Exception('User not found check your email')


@app.route('/user/post', methods=['GET', 'POST'])
@token_required
def post(current_user: User):
    if request.method == 'GET':
        all_post = post_service.get_all_own_post(current_user.id)
        return jsonify({'posts': all_post})

    if request.method == 'POST':
        response = request.get_json()
        title = response['title']
        text = response['content']
        post = Post(title, text, current_user.id)
        return post_service.create_post(post)


@app.route('/user/post/<int:post_id>', methods=['DELETE', 'PUT'])
@token_required
def delete_or_update_post(current_user: User, post_id: int):
    if request.method == 'DELETE':
        try:
            post_service.get_post_by_id(post_id)
            try:
                post_service.delete_post_by_id(post_id)
                return ''
            except:
                raise Exception('Delete failed')
        except:
            raise Exception('Post not found for delete')


@app.route('/user/<int:post_id>/comments', methods=['GET', 'POST'])
@token_required
def comment(current_user: User, post_id: int):
    if request.method == 'GET':
        return comment_service.get_all_comments(post_id)

    if request.method == 'POST':
        response = request.get_json()
        content = response['content']
        return comment_service.create_comment(content, post_id, current_user.id)


@app.route('/user/<int:post_id>/like', methods=['POST'])
@token_required
def like(current_user: User, post_id: int):
    if request.method == 'POST':
        try:
            post_service.post_like(post_id)
            return ''
        except:
            Exception('Delet post failed')


@app.route('/user')
@token_required
def user(current_user: User):
    return jsonify({'id': current_user.id, 'name': current_user.name, 'surname': current_user.surname, 'email': current_user.email})


def create_token(user_id, user_name, user_email):
    token = jwt.encode({
        'id': user_id,
        'user_email': user_email,
        'user_name': user_name,
        'exp': (datetime.now() + timedelta(seconds=300)).timestamp()
    }, key=app.secret_key).decode('UTF-8')
    return token


if __name__ == '__main__':
    app.secret_key = 'secret_key'
    app.run(debug=True, host='127.0.0.1', port=3000)
