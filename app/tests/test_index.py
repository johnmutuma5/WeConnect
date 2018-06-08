import unittest
from app import app


class TestIndexCase (unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://127.0.0.1:8080/'
        self.app = app.test_client()

    def test_renders_index_page(self):
        url = self.base_url
        response = self.app.get(url)
        html = response.data.decode('utf-8')
        self.assertIn('WeConnect - Homepage', html)


    def test_renders_documentation_page(self):
        url = self.base_url + 'api/documentation'
        response = self.app.get(url)
        html = response.data.decode('utf-8')
        self.assertIn('WeConnect provides a platform that brings', html)



if __name__ == "__main__":
    unittest.main(module=__name__)
