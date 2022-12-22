class Adress:
    def __init__(self, city: str, street: str, building: str, zip_code: str) -> None:
        self.__city = city
        self.__street = street
        self.__building = building
        self.__zip_code = zip_code

    def get_adress(self):
        return f'{self.__city}, {self.__street},  {self.__building}, {self.__zip_code}.'

    def set_adress(self, city: str, street: str, building: str, zip_code: str):
        self.__city = city
        self.__street = street
        self.__building = building
        self.__zip_code = zip_code

    def get_city(self):
        return self.__city

    def set_city(self, city: str) -> None:
        self.__city = city

    def get_street(self):
        return self.__street

    def set_street(self, street: str) -> None:
        self.__street = street

    def get_building(self):
        return self.__building

    def set_building(self, building: str) -> None:
        self.__building = building

    def get_zip_code(self):
        return self.__zip_code

    def set_zip_code(self, zip_code: str) -> None:
        self.__zip_code = zip_code
