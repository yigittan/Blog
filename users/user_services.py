import jwt
from models.user import User


class UserService:
    def __init__(self, storage):
        self.storage = storage

    def create_user(self, user):
        return self.storage.insert_user(user)

    def create_user_adress(self, adress):
        return self.storage.insert_user_adress(adress)

    def get_user_by_email(self, email):
        return self.storage.get_user_by_email(email)

    def check_password(self, user: User, candidate_password):
        return candidate_password == user.password

    def get_user_by_id(self, id):
        return self.storage.get_user_by_id(id)
