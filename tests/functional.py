import unittest
from webtest import AppError, TestApp

import app as main

class TestResources(unittest.TestCase):

    def test_login(self):
        app = TestApp(main.app)
        params = dict(email='editor@home.com', password='abc123')
        response = app.post_json('/auth/login', params)
        self.assertEqual(response.status_code, 200)
        
    def test_signup(self):
        app = TestApp(main.app)
        
        params = dict(email='user@home.com', password='ghi789')
        good_response = app.post_json('/auth/signup', params)
        self.assertEqual(good_response.status_code, 204)

if __name__ == '__main__':
    unittest.main()