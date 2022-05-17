import unittest
from app.models import Comment
from app import db

class CommentModelTest(unittest.TestCase):

    def setUp(self):
        self.new_comment = Comment('impressive')

    def tearDown(self):
        Blog.query.delete()
        User.query.delete()    

    def test_instance(self):
        self.assertTrue(isinstance(self.new_comment, Comment))

    def test_save_comment(self):
        self.new_comment.save_comment()
        self.assertTrue(len(Comment.query.all())>0)