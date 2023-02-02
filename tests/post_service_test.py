import pytest

from posts.post_services import PostService
from models.post import Post


class FakeStorage:
    def __init__(self, expected_post):
        self.expected_post = expected_post

    def insert_post(self, post):
        assert self.expected_post == post


def test_post_service_create_post():
    post = Post('Yalancı dünya', 'Test', 3)
    fake_storage = FakeStorage(post)
    service = PostService(fake_storage)
    service.create_post(post)
