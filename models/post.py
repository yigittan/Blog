class Post:
    def __init__(self, title, content, user_id, likes=0):
        self.title = title
        self.content = content
        self.user_id = user_id
        self.likes = likes
