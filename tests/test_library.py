import filecmp
from flask import Flask
from floa.models.library import Library, Status
import os.path
import random
import unittest
import json


class TestLibrary(unittest.TestCase):

    @staticmethod
    def _generate_catalog_list(count, start=1):
        result = []
        for i in range(start, start + count):
            result.append({'id': i, 'title': f'Title {i}'})
        return result

    @staticmethod
    def _generate_library_list(count, val=0, rand=False):
        result = [-1]
        for _ in range(1, count):
            if rand:
                val = random.randrange(-1, 3)
            result.append(val)
        return result

    def setUp(self):
        self.library = Library()

    def tearDown(self):
        return super().tearDown()

    def test_set_status(self):
        self.library.library = [-1, -1]
        self.assertEqual(Status(self.library.library[1]), Status['MISSING'])
        self.library.set_status('1', 0)
        self.assertEqual(Status(self.library.library[1]), Status['NOT_HAVE'])
        self.library.set_status(1, 1)
        self.assertEqual(Status(self.library.library[1]), Status['HAVE'])
        self.library.set_status(1, 2)
        self.assertEqual(Status(self.library.library[1]), Status['WISH'])
        self.library.set_status(1, 3)
        self.assertEqual(Status(self.library.library[1]), Status['NEW'])

    def test_add_book_status_value_is_new(self):
        list1 = self._generate_catalog_list(4)
        self.library.catalog = list1
        # add some items
        self.library.update(self.library.catalog)
        # status of all is New
        for i in self.library.library:
            self.assertEqual(Status(self.library.library[i]), Status['NEW'])
        # and we have the whole list, +1
        self.assertEqual(len(self.library.library), 5)
        # add another item
        list2 = self._generate_catalog_list(5)
        # diff = self.library.compare(list1, list2)
        self.library.update(list2)
        self.assertEqual(len(self.library.library), 6)
        self.assertEqual(Status(self.library.library[4]), Status['NEW'])

    def test_add_with_insertion_of_missing_volume(self):
        list1 = self._generate_library_list(10, val=3)
        list1[8] = -1  # missing item
        list1[9] = 2  # not new so it should not change
        self.library.library = list1

        list2 = self._generate_catalog_list(5, start=8)
        list2.pop(3)  # create gap at id=11
        self.library.update(list2)
        self.assertEqual(self.library.library[8], Status.NEW.value)
        self.assertEqual(self.library.library[9], Status.WISH.value)
        self.assertEqual(self.library.library[11], Status.MISSING.value)
        self.assertEqual(self.library.library[12], Status.NEW.value)
        self.assertEqual(len(self.library.library), 13)

    def test_import_export_my_library(self):
        src = './tests/instance/import.txt'
        dst = './tests/instance/export.txt'
        list10 = self._generate_library_list(10, rand=True)
        with open(src, 'w') as f:
            json.dump(list10, f)
        self.library.import_json(fname=src)
        self.library.export_json(fname=dst)
        self.assertTrue(filecmp.cmp(src, dst))
        os.remove(src)
        os.remove(dst)


if __name__ == '__main__':
    unittest.main()
