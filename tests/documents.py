import unittest
from webtest import TestApp

from app import app
import seeds.test

test_app = TestApp(app)

class TestAuth(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        seeds.test.run()
        params = dict(email='editor@home.com', password='abc123')
        response = test_app.post_json('/auth/login', params)
        test_app.authorization = ('Bearer', response.json.get('token'))

    def test_get_documents(self):
        response = test_app.get('/documents')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json.get('data'))

if __name__ == '__main__':
    unittest.main()