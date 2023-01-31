from models.post import Post


class PostPostgreStorage:
    def __init__(self, connection):
        self.connection = connection

    def insert_post(self, post: Post):
        cursor = self.connection.cursor()
        query = """INSERT INTO "post" (title, content, user_id) VALUES(%s, %s, %s) RETURNING id"""
        record_data = (post.title, post.content, post.user_id)
        cursor.execute(query, record_data)
        self.connection.commit()
        post_id = str(cursor.fetchone()[0])
        return post_id

    def get_all_own_post(self, user_id):
        cursor = self.connection.cursor()
        query = """SELECT * FROM "post" WHERE user_id = %(bar)s"""
        select_data = {'bar': user_id}
        cursor.execute(query, select_data)
        all_post = cursor.fetchall()
        return all_post

    def get_post_by_id(self, post_id):
        print(post_id)
        cursor = self.connection.cursor()
        query = """SELECT * FROM "post" WHERE id =%(bar)s"""
        get_data = {'bar': post_id}
        cursor.execute(query, get_data)
        data = cursor.fetchone()
        print(data)
        if data is None:
            return None
        post = Post(data[1], data[2], data[3])
        return post

    def delete_post_by_id(self, post_id):
        cursor = self.connection.cursor()
        query = """DELETE FROM "post" WHERE id = %(bar)s"""
        deleted_id = {'bar': post_id}
        cursor.execute(query, deleted_id)
        self.connection.commit()
        return str(post_id)

    def update_post(self, title, content, post_id):
        cursor = self.connection.cursor()
        query = """UPDATE "post" SET title=%(title)s, content =%(content)s WHERE id=%(post_id)s"""
        update_data = {'title': title, 'content': content, 'post_id': post_id}
        cursor.execute(query, update_data)
        self.connection.commit()
        return {'message': 'Update success'}
