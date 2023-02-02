from flask import jsonify

from models.post import Post


class PostService:
    def __init__(self, storage):
        self.storage = storage

    def create_post(self, post):
        return self.storage.insert_post(post)

    def get_all_posts(self):
        all_posts = self.storage.get_all_posts()
        posts = []
        for data in all_posts:
            post = {}
            post['id'] = data[0]
            post['title'] = data[1]
            post['content'] = data[2]
            post['user_id'] = data[3]
            post['likes'] = data[4]
            posts.append(post)
        return jsonify(posts)

    def get_all_own_post(self, user_id):
        all_posts = self.storage.get_all_own_post(user_id)
        posts = []
        for data in all_posts:
            post = {}
            post['id'] = data[0]
            post['title'] = data[1]
            post['content'] = data[2]
            post['user_id'] = data[3]
            post['likes'] = data[4]
            posts.append(post)
        return posts

    def get_post_by_id(self, post_id):
        return self.storage.get_post_by_id(post_id)

    def delete_post_by_id(self, post_id):
        return self.storage.delete_post_by_id(post_id)

    def update_post(self, title, content, post_id):
        if not self.get_post_by_id(post_id):
            raise Exception('Post not found for update')
        return self.storage.update_post(title, content, post_id)

    def post_like(self, post_id):
        post: Post = self.storage.get_post_by_id(post_id)
        if not post:
            raise Exception('Post not found for like')
        likes = post.likes + 1
        return self.storage.update_post_likes(post_id, likes)
