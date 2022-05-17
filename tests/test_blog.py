import unittest
from app.models import Blog
from app import db

class BlogModelTest(unittest.TestCase):

    def setUp(self):
        self.new_blog = Blog(id = 1, title = 'travel', blog = 'i love adventures',author = 'frida')

    def test_instance(self):
        self.assertTrue(isinstance(self.new_blog, Blog))