import unittest
from webtest import TestApp

import app as main

class TestResources(unittest.TestCase):

    def test_login(self):
        app = TestApp(main.app)
        params = dict(email='editor@home.com', password='abc123')
        response = app.post_json('/auth/login', params)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()