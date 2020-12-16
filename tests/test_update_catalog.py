import unittest
from floa.routes import get_latest_catalog

class TestUpdateCatalog(unittest.TestCase):
    def test_get_latest(self):
        result = get_latest_catalog()
        print(result)

if __name__ == '__main__':
    unittest.main()