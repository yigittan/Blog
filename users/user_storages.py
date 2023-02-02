from models.adress import Adress
from models.user import User


class UserPostgreStorage:
    def __init__(self, connection) -> str:
        self.connection = connection

    def insert_user(self, user: User):
        cursor = self.connection.cursor()

        query = """INSERT INTO "user" (name, surname, email, password) VALUES(%s, %s, %s, %s) RETURNING id"""
        record_data = (user.name, user.surname, user.email, user.password)

        cursor.execute(query, record_data)
        self.connection.commit()
        current_inserted_id = cursor.fetchone()[0]

        return str(current_inserted_id)

    def insert_user_adress(self, adress: Adress) -> None:
        cursor = self.connection.cursor()
        query = """INSERT INTO "adress" (city, street, building, zip_code, user_id) VALUES(%s, %s, %s, %s, %s)"""
        record_data = (adress.city, adress.street,
                       adress.building, adress.zip_code, adress.user_id)
        cursor.execute(query, record_data)
        self.connection.commit()

    def get_user_by_email(self, email):
        cursor = self.connection.cursor()
        query = """SELECT * FROM "user" WHERE email=%(email)s"""
        record_data = {'email': email}
        cursor.execute(query, record_data)
        data = cursor.fetchone()
        try:
            return User(data[1], data[2], data[3], data[4], data[0])
        except:
            return

    def get_user_by_id(self, id):
        cursor = self.connection.cursor()
        query = """SELECT * FROM "user" WHERE id=%(id)s"""
        record_data = {'id': id}
        cursor.execute(query, record_data)
        data = cursor.fetchone()
        try:
            return User(data[1], data[2], data[3], data[4], data[0])
        except:
            return
