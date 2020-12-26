from datetime import datetime as dt
from floa.models.user import User
import unittest
from unittest.mock import patch


class TestUser(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init_missing_required_args_raises(self):
        with self.assertRaises(TypeError):
            user = User()

    def test_init_initializes_members(self):
        user = User('foo', 'foo@bar.com')
        self.assertEqual(user.name, 'foo')
        self.assertEqual(user.email, 'foo@bar.com')
        self.assertEqual(user._key, -1)
        self.assertIsNone(user.id)
        self.assertEqual(user.library.library, [-1])
        self.assertTrue(isinstance(user.created_date, dt))

    def test_repr_returns_dict(self):
        user = User('foo', 'foo@bar.com')
        repr = user.__repr__()
        assert(isinstance(repr, dict))
        for f in User.fields:
            self.assertTrue(f in repr)

    @patch('floa.models.db.Database.commit')
    def test_add_sets_key(self, mock_commit):
        mock_commit.return_value = 23
        user = User('foo', 'foo@bar.com')
        user.add()
        self.assertEqual(user._key, 23)

    @patch('floa.models.db.Database.query')
    def test_get_found(self, mock_query):
        mock_query.return_value = {'key': 1,
                                   'id': '0000',
                                   'name': 'foo',
                                   'email': 'foo@bar.com'
                                   }
        user = User.get('0000')
        self.assertTrue(isinstance(user, User))
        self.assertEqual(user.id, '0000')

    @patch('floa.models.db.Database.query')
    def test_get_not_found(self, mock_query):
        mock_query.return_value = None
        user = User.get_by_email('foo')
        self.assertIsNone(user)


if __name__ == "__main__":
    unittest.main()
