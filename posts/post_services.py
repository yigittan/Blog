from flask import jsonify


class PostService:
    def __init__(self, storage):
        self.storage = storage

    def create_post(self, post):
        return self.storage.insert_post(post)

    def get_all_own_post(self, user_id):
        posts = self.storage.get_all_own_post(user_id)
        output = []
        for data in posts:
            post = {}
            post['id'] = data[0]
            post['title'] = data[1]
            post['content'] = data[2]
            post['user_id'] = data[3]
            output.append(post)
        return output

    def get_post_by_id(self, post_id):
        return self.storage.get_post_by_id(post_id)

    def delete_post_by_id(self, post_id):
        return self.storage.delete_post_by_id(post_id)

    def update_post(self, title, content, post_id):
        if self.get_post_by_id(post_id):
            return self.storage.update_post(title, content, post_id)
        else:
            return None
