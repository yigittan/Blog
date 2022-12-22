from models.Adress import Adress


class User:
    def __init__(self, name: str, surname: str, email: str, password: str, adress: Adress) -> None:
        self.__name = name
        self.__surname = surname
        self.__email = email
        self.__password = password
        self.__adress = adress

    def get_name(self):
        return self.__name

    def set_name(self, name: str) -> None:
        self.__name = name

    def get_surname(self):
        return self.__surname

    def set_surname(self, surname: str) -> None:
        self.__surname = surname

    def get_email(self):
        return self.__email

    def set_email(self, email: str) -> None:
        self.__email = email

    def get_password(self):
        return self.__password

    def set_password(self, password: str) -> None:
        self.__password = password

    def get_adress(self):
        return self.__adress.get_adress()
