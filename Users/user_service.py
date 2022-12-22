class UserService:
    def __init__(self, storage) -> None:
        self.storage = storage

    def service_insert(self, user):
        return self.storage.storage_insert(user)

    def service_get_user_by_email(self, email):
        res = self.storage.storage_get_user_by_email(email)
        return res
