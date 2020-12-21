from floa.models.loa import LoA
import random
import unittest
from unittest.mock import Mock, patch
from requests.models import Response
from requests.exceptions import HTTPError


class TestLoA(unittest.TestCase):

    @staticmethod
    def _generate_list(count, start=1, rand=False):
        result = []
        for id in range(start, start + count):
            if rand:
                id = random.randrange(400)
            result.append({'id': id, 'title': f'Title {id}'})
        return result

    @staticmethod
    def _generate_loa_html(count):
        result = ""
        for i in range(count):
            result += f'<li class="content-listing content-listing--book"> \
                        <a href="/books/Link-{i}"> \
                        <i class="book-listing__number">{i}</i> \
                        <b class="content-listing__title">Title-{i}</b> \
                        </a> \
                    </li>'
        return result

    def setUp(self):
        self.catalog = LoA()

    def tearDown(self):
        return super().tearDown()

    @staticmethod
    def _mock_response(
            status=200,
            content="CONTENT",
            json_data=None,
            raise_for_status=None):
        """
        since we typically test a bunch of different
        requests calls for a service, we are going to do
        a lot of mock responses, so its usually a good idea
        to have a helper function that builds these things
        """
        mock_resp = Mock()
        # mock raise_for_status call w/optional error
        mock_resp.raise_for_status = Mock()
        if raise_for_status:
            mock_resp.raise_for_status.side_effect = raise_for_status
        # set status code and content
        mock_resp.status_code = status
        mock_resp.content = content
        # add json data if provided
        if json_data:
            mock_resp.json = Mock(
                return_value=json_data
            )
        return mock_resp

    @patch('floa.models.loa.requests.get')
    def test_loa_request_return_200(self, mock_get): 
        mock_get.return_value = self._mock_response(content="something")
        response = LoA.loa_request()
        self.assertEqual(response, 'something')

    @patch('floa.models.loa.requests.get')
    def test_loa_request_return_404(self, mock_get): 
        mock_get.return_value = self._mock_response(status=404, raise_for_status=HTTPError("page not found"))
        self.assertRaises(HTTPError, LoA.loa_request)

    @patch('floa.models.loa.requests.get')
    def test_loa_request_return_500(self, mock_get): 
        mock_get.return_value = self._mock_response(status=500, raise_for_status=HTTPError("site down"))
        self.assertRaises(HTTPError, LoA.loa_request)       

    def test_scrape_no_results_raises_error(self):
        self.assertRaises(ValueError, LoA.scrape, '<html></html>')

    def test_scrape_success(self):
        number_of_entries = 3
        content = self._generate_loa_html(number_of_entries)
        results = LoA.scrape(content)
        self.assertEqual(len(results), number_of_entries)

    def test_build_catalog(self):
        raise NotImplementedError

    def test_get_latest(self):
        raise NotImplementedError

    def test_sort_catalog(self):
        list1 = self._generate_list(100, rand=True)
        sorted_list = self.catalog.sort(list1)
        for i in range(len(sorted_list) - 1):
            self.assertTrue(sorted_list[i]['id'] <= sorted_list[i+1]['id'])
