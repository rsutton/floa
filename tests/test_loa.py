from floa.models.loa import LoA
import unittest
import random

class TestLoA(unittest.TestCase):

    @staticmethod
    def generate_catalog_list(count, start=1, rand=False):
        result = []
        for i in range(start, start + count):
            id = i
            if rand:
                id = random.randrange(400)
            result.append({'id': id, 'title': f'Title {i}'})
        return result
    
    def setUp(self):
        self.catalog = LoA()

    def tearDown(self):
        return super().tearDown()

    # def test_get_latest_catalog(self):
    #     ''' this is expensive and should be an integration test'''
    #     url=self.app.config['LOA_COLLECTION_URL']
    #     result = self.library.get_latest(url)
    #     assert(isinstance(result, list))
    #     id = result[0].get('id')
    #     self.assertTrue(id == 1)

    def test_sort_catalog(self):
        list1 = self.generate_catalog_list(100, rand=True)
        sorted_list = self.catalog.sort(list1)
        for i in range(len(sorted_list) - 1):
            self.assertTrue(sorted_list[i]['id'] <= sorted_list[i+1]['id'])
