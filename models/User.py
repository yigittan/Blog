class User:
    def __init__(self, name, surname, email, password, id=None):
        self.id = id
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password
