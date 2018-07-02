import unittest
from webtest import TestApp

from app import app
import seeds.test

test_app = TestApp(app)
user_id = 1

class TestAuth(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        seeds.test.run()
        params = dict(email='editor@home.com', password='abc123')
        response = test_app.post_json('/auth/login', params)
        test_app.authorization = ('Bearer', response.json.get('token'))

    def test_get_documents(self):
        response = test_app.get('/documents')
        documents = response.json.get('data')
        
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(documents)
        
        for document in documents:
            self.assertEqual(document.get('owner'), user_id)

    def test_create_document(self):
        params = dict(name='New Document', width=224, height=224)
        response = test_app.post_json('/documents', params)
        document = response.json
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(document.get('owner'), user_id)

if __name__ == '__main__':
    unittest.main()