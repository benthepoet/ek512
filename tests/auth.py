import unittest
from webtest import TestApp

from app import api
import seeds.test

test_app = TestApp(api)

class TestAuth(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        seeds.test.run()

    def test_login(self):
        params = dict(email='editor@home.com', password='abc123')
        response = test_app.post_json('/auth/login', params)
        
        self.assertEqual(response.status_code, 200)
        
    def test_login_not_found(self):
        params = dict(email='user@home.com', password='ghi789')
        response = test_app.post_json('/auth/login', params, status=404)
        
        self.assertEqual(response.status_code, 404)
        
    def test_signup(self):
        params = dict(email='user@home.com', password='ghi789')
        response = test_app.post_json('/auth/signup', params)
        
        self.assertEqual(response.status_code, 204)
        
    def test_signup_existing(self):
        params = dict(email='editor@home.com', password='ghi789')
        response = test_app.post_json('/auth/signup', params, status=409)
        
        self.assertEqual(response.status_code, 409)

if __name__ == '__main__':
    unittest.main()