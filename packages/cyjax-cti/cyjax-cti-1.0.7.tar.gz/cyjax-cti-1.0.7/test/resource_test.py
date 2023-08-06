#  CYjAX Limited

import pytest
import responses

from unittest.mock import patch, Mock
from cyjax.exceptions import UnauthorizedException, ResponseErrorException

import cyjax
from cyjax.api_client import ApiClient
from cyjax.resources.resource import Resource


class TestResourceService:

    @classmethod
    def setup_class(cls):
        api_client = ApiClient(api_key='foo_api_key')
        cls.api_url = api_client.get_api_url()

    @responses.activate
    def test_paginate(self):

        responses.add(responses.GET, self.api_url + '/test/endpoint?param1=test&param2=foo&page=1&per-page='
                      + str(Resource.DEFAULT_ITEMS_PER_PAGE),
                      json=[{"1": "a"}, {"2": "b"}], status=200,
                      headers={'Link': self.api_url +
                                       '/test/endpoint?param1=test&param2=foo&page=2&per-page=1;rel=next'})

        responses.add(responses.GET, self.api_url + '/test/endpoint?param1=test&param2=foo&page=2&per-page='
                      + str(Resource.DEFAULT_ITEMS_PER_PAGE),
                      json=[{"3": "c"}, {"4": "d"}], status=200)

        resource_service = Resource(api_key='9753b80f76bd4293e8c610b07091a37b')
        for x in resource_service.paginate(endpoint='test/endpoint', params={'param1': 'test', 'param2': 'foo'}):
            continue

        assert len(responses.calls) == 2
        assert responses.calls[0].request.url == self.api_url + \
               '/test/endpoint?param1=test&param2=foo&page=1&per-page=' + str(Resource.DEFAULT_ITEMS_PER_PAGE)
        assert responses.calls[0].response.text == '[{"1": "a"}, {"2": "b"}]'

        assert responses.calls[1].request.url == self.api_url + \
               '/test/endpoint?param1=test&param2=foo&page=2&per-page=' + str(Resource.DEFAULT_ITEMS_PER_PAGE)
        assert responses.calls[1].response.text == '[{"3": "c"}, {"4": "d"}]'

        def test_setting_client():
            resource = Resource()
            assert 'https://api.cyberportal.co' == resource._api_client.get_api_url()
            assert resource._api_client.get_api_key() is None

            resource = Resource('123456', 'https://api.new-address.com')
            assert 'https://api.new-address.com' == resource._api_client.get_api_url()
            assert '123456' == resource._api_client.get_api_key()

    def test_one_not_implement_by_default(self):
        resource = Resource()
        assert hasattr(resource, 'one')

        with pytest.raises(NotImplementedError) as e:
            resource.one(1)

        assert 'This resource does not support get_one_by_id' == str(e.value)

    @responses.activate
    def test_get_one_by_id(self):
        cyjax.api_key = 'module_api_key'

        responses.add(responses.GET, self.api_url + '/test-resource/7003', status=200,
                      json={'id': 7003,
                            'title': 'Test',
                            'description': 'Hello'})

        resource = Resource()
        assert hasattr(resource, 'get_one_by_id')

        entity = resource.get_one_by_id('test-resource', 7003)
        assert isinstance(entity, dict)
        assert 7003 == entity.get('id')
        assert 'Test' == entity.get('title')
        assert 'Hello' == entity.get('description')

        entity = resource.get_one_by_id('test-resource', '7003')
        assert 7003 == entity.get('id')

        entity = resource.get_one_by_id('test-resource/', '7003')
        assert 7003 == entity.get('id')

        entity = resource.get_one_by_id('/test-resource/', '7003')
        assert 7003 == entity.get('id')

        cyjax.api_key = None

    @responses.activate
    def test_get_one_by_id_not_found(self):
        cyjax.api_key = 'module_api_key'

        responses.add(responses.GET, self.api_url + '/test-resource/7004', status=404,
                      json={"message": "Incident report not found",
                            "code": 404,
                            "reason": "Not Found"})

        resource = Resource()

        with pytest.raises(ResponseErrorException) as e:
            resource.get_one_by_id('test-resource', 7004)

        assert "(404, 'Incident report not found')" == str(e.value)
        cyjax.api_key = None

    def test_default_pagination_limit(self):
        page_response_mock = Mock()
        page_response_mock.json.return_value = [{'id': 1}, {'id': 2}, {'id': 3}, {'id': 4}, {'id': 5}, {'id': 6}]
        page_response_mock.links = {}

        with patch.object(Resource, 'get_page', return_value=page_response_mock):
            resource_service = Resource(api_key='test-key')

            models = list(resource_service.paginate(endpoint='test/endpoint'))
            assert 6 == len(models)

    def test_supports_pagination_limit(self):
        page_response_mock = Mock()
        page_response_mock.json.return_value = [{'id': 1}, {'id': 2}, {'id': 3}, {'id': 4}, {'id': 5}, {'id': 6}]
        page_response_mock.links = {'next': {'url': 'https://next-page.com?page=2'}}

        with patch.object(Resource, 'get_page', return_value=page_response_mock):
            resource_service = Resource(api_key='test-key')

            models = list(resource_service.paginate(endpoint='test/endpoint', limit=2))
            assert 2 == len(models)

    @responses.activate
    def test_limit_with_multiple_pages(self):
        models = []
        for i in range(100):
            models.append({'id': i})

        responses.add(responses.GET, self.api_url + '/test/endpoint?page=1&per-page=50',
                      status=200, json=models[:50],
                      headers={'Link': self.api_url + '/test/endpoint?page=2&per-page=50;rel=next'})

        responses.add(responses.GET, self.api_url + '/test/endpoint?page=2&per-page=50',
                      json=models[50:],
                      status=200)

        resource_service = Resource(api_key='test-key')
        found = list(resource_service.paginate(endpoint='test/endpoint', limit=67))
        assert 67 == len(found)
        assert models[0:67] == found

    def test_trim_endpoint(self):
        resource = Resource()
        assert hasattr(resource, '_trim_endpoint')
        assert 'test-testy' == resource._trim_endpoint('test-testy')
        assert 'test-testy' == resource._trim_endpoint('/test-testy')
        assert 'test-testy' == resource._trim_endpoint('test-testy/')
        assert 'test-testy' == resource._trim_endpoint('/test-testy/')
