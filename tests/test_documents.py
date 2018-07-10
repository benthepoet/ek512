import unittest
from webtest import TestApp

from app import api

DOCUMENT_ID = 2
ELEMENT_ID = 2
USER_ID = 1

test_app = TestApp(api)

class TestAuth(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        params = dict(email='editor@home.com', password='abc123')
        response = test_app.post_json('/auth/login', params)
        test_app.authorization = ('Bearer', response.json.get('token'))

    def test_create_document(self):
        params = dict(name='New Document', width=224, height=224)
        response = test_app.post_json('/documents', params)
        document = response.json
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(document.get('owner'), USER_ID)
    
    def test_get_documents(self):
        response = test_app.get('/documents')
        documents = response.json.get('data')
        
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(documents)
        
        for document in documents:
            self.assertEqual(document.get('owner'), USER_ID)

    def test_get_document(self):
        response = test_app.get('/documents/%s' % DOCUMENT_ID)
        document = response.json
        
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(document)
        self.assertEqual(document.get('id'), DOCUMENT_ID)
        self.assertEqual(document.get('owner'), USER_ID)
        
    def test_get_document_user_scoping(self):
        response = test_app.get('/documents/%s' % (DOCUMENT_ID + 1), status=404)
        
        self.assertEqual(response.status_code, 404)

    def test_get_elements(self):
        response = test_app.get('/documents/%s/elements' % DOCUMENT_ID)
        elements = response.json.get('data')
        
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(elements)
        
        for element in elements:
            self.assertEqual(element.get('document'), DOCUMENT_ID)
            
    def test_get_elements_user_scoping(self):
        response = test_app.get('/documents/%s/elements' % (DOCUMENT_ID + 1), status=404)
        
        self.assertEqual(response.status_code, 404)
        
    def test_update_document(self):
        params = dict(name='Revised Document', width=640, height=480)
        response = test_app.put_json('/documents/%s' % DOCUMENT_ID, params)
        
        self.assertEqual(response.status_code, 200)
        
    def test_update_document_user_scoping(self):
        params = dict(name='Revised Document', width=640, height=480)
        response = test_app.put_json('/documents/%s' % (DOCUMENT_ID + 1), params, status=404)
        
        self.assertEqual(response.status_code, 404)
        
    def test_update_element(self):
        params = dict(x=64, y=64)
        response = test_app.put_json('/documents/%s/elements/%s' % (DOCUMENT_ID, ELEMENT_ID), params)
        
        self.assertEqual(response.status_code, 200)
        
    def test_update_element_user_scoping(self):
        params = dict(x=64, y=64)
        response = test_app.put_json('/documents/%s/elements/%s' % (DOCUMENT_ID, ELEMENT_ID + 1), params, status=404)
        
        self.assertEqual(response.status_code, 404)
        
        response = test_app.put_json('/documents/%s/elements/%s' % (DOCUMENT_ID + 1, ELEMENT_ID), params, status=404)
        
        self.assertEqual(response.status_code, 404)