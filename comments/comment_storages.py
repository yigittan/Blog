class CommentPostgreStorage:
    def __init__(self, connection):
        self.connection = connection

    def insert_comment(self, content, post_id, current_id):
        cursor = self.connection.cursor()
        query = """INSERT INTO "comment" (content, post_id, comment_owner_id) VALUES(%s, %s, %s) RETURNING id"""
        record_data = (content, post_id, current_id)
        cursor.execute(query, record_data)
        self.connection.commit()
        inserted_id = str(cursor.fetchone()[0])
        return inserted_id

    def get_all_comments(self, post_id):
        cursor = self.connection.cursor()
        query = """SELECT * FROM "comment" WHERE post_id = %(post_id)s"""
        select_data = {'post_id': post_id}
        cursor.execute(query, select_data)
        all_comment = cursor.fetchall()
        return all_comment
