import unittest
from webtest import TestApp

from app import api

USER_ID = 1

test_app = TestApp(api)

class TestAuth(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        params = dict(email='editor@home.com', password='abc123')
        response = test_app.post_json('/auth/login', params)
        test_app.authorization = ('Bearer', response.json.get('token'))
        
    def test_user_me(self):
        response = test_app.get('/users/me')
        user = response.json
        
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(user)
        self.assertEqual(user.get('id'), USER_ID)
        self.assertIsNone(user.get('hash'))