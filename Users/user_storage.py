from models.User import User


class UserStorage:
    def __init__(self, client) -> None:
        self.db = client.db.users

    def storage_insert(self, user):
        res = self.db.insert_one({
            "name": user.get_name(),
            "surname": user.get_surname(),
            "email": user.get_email(),
            "password": user.get_password(),
            "adress": user.get_adress()
        })

        return str(res.inserted_id)

    def storage_get_user_by_email(self, email):
        res = self.db.find_one({'email': email})
        user = User(res['name'], res['surname'], res['email'],
                    res['password'], res['adress'])
        return user
