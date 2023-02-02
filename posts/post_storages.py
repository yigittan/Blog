from models.post import Post


class PostPostgreStorage:
    def __init__(self, connection):
        self.connection = connection

    def insert_post(self, post: Post):
        cursor = self.connection.cursor()
        query = """INSERT INTO "post" (title, content, user_id, likes) VALUES(%s, %s, %s, %s) RETURNING id"""
        record_data = (post.title, post.content, post.user_id, post.likes)
        cursor.execute(query, record_data)
        self.connection.commit()
        return str(cursor.fetchone()[0])

    def get_all_posts(self):
        cursor = self.connection.cursor()
        query = """SELECT * FROM "post" """
        cursor.execute(query)
        return cursor.fetchall()

    def get_all_own_post(self, user_id):
        cursor = self.connection.cursor()
        query = """SELECT * FROM "post" WHERE user_id = %(user_id)s"""
        select_data = {'user_id': user_id}
        cursor.execute(query, select_data)
        return cursor.fetchall()

    def get_post_by_id(self, post_id):
        cursor = self.connection.cursor()
        query = """SELECT * FROM "post" WHERE id =%(post_id)s"""
        get_data = {'post_id': post_id}
        cursor.execute(query, get_data)
        post_data = cursor.fetchone()
        if not post_data:
            raise Exception('Post data not found')
        return Post(post_data[1], post_data[2], post_data[3], post_data[4])

    def delete_post_by_id(self, post_id):
        cursor = self.connection.cursor()
        query = """DELETE FROM "post" WHERE id = %(post_id)s"""
        deleted_id = {'post_id': post_id}
        cursor.execute(query, deleted_id)
        self.connection.commit()

    def update_post(self, title, content, post_id):
        cursor = self.connection.cursor()
        query = """UPDATE "post" SET title=%(title)s, content =%(content)s WHERE id=%(post_id)s"""
        update_data = {'title': title, 'content': content, 'post_id': post_id}
        cursor.execute(query, update_data)
        self.connection.commit()

    def update_post_likes(self, post_id, likes):
        cursor = self.connection.cursor()
        query = """UPDATE "post" SET likes=%(likes)s WHERE id =%(post_id)s"""
        update_data = {'likes': likes, 'post_id': post_id}
        cursor.execute(query, update_data)
        self.connection.commit()
