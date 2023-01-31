from flask import jsonify


class CommentService:
    def __init__(self, storage):
        self.storage = storage

    def create_comment(self, content, post_id, current_id):
        return self.storage.insert_comment(content, post_id, current_id)

    def get_all_comments(self, post_id):
        all_comments = self.storage.get_all_comments(post_id)
        output = []
        for comments in all_comments:
            comment = {}
            print(comment)
            comment['content'] = comments[1]
            comment['post_id'] = comments[2]
            comment['owner_id'] = comments[3]
            output.append(comment)
        return output
