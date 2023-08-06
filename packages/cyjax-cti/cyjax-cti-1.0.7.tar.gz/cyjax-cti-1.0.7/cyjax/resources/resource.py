import logging
from urllib.parse import urlparse, parse_qs

from cyjax.api_client import ApiClient
from cyjax.exceptions import ResponseErrorException, ApiKeyNotFoundException


class Resource(object):

    DEFAULT_ITEMS_PER_PAGE = 50

    def __init__(self, api_key=None, api_url=None):
        """
        :param api_key: The API key.
        :param api_url: The Cyjax API url.
        """
        self._api_client = ApiClient(api_key=api_key, api_url=api_url)

    def get_page(self, endpoint, params=None, data=None, page=1, per_page=DEFAULT_ITEMS_PER_PAGE):
        """
        Returns all items in a page for the given endpoint.
        :param endpoint: The endpoint.
        :type endpoint: str
        :param params: The list of tuples or bytes to send in the query string for the request.
        :type params: dict, optional
        :param data: The list of tuples, bytes, or file-like object to send in the body of the request.
        :return: :class:`Response <Response>` object
        :param page: The page.
        :type page: int, optional
        :param per_page: The number of items per page.
        :type per_page: int, optional
        :return: The list of items.
        :rtype list
        :raises ResponseErrorException: Whether the response cannot be parsed.
        :raises ApiKeyNotFoundException: Whether the API key is not provider.
        """
        if params is None:
            params = {}
        if data is None:
            data = {}
        params.update({'page': page, 'per-page': per_page})

        return self._api_client.send(method='get', endpoint=endpoint, params=params, data=data)

    def paginate(self, endpoint, params=None, data=None, limit=None):
        """
        Returns (all) items for the given endpoint.

        :param endpoint: The endpoint.
        :type endpoint: str

        :param params: The list of tuples or bytes to send in the query string for the request.
        :type params:  dict, optional

        :param data: The list of tuples, bytes, or file-like object to send in the body of the request.
        :type data: dict

        :param limit: The limit of items to fetch. If limit is None returns all items for a collection.
        :type limit: int

        :return: The list generator.
        :rtype Generator[dict]
        """

        if data is None:
            data = {}
        if params is None:
            params = {}
        if limit is not None:
            limit = int(limit)

        endpoint = self._trim_endpoint(endpoint)

        logging.debug('Sending request to endpoint %s...' % endpoint)
        has_next = True
        page = 1
        found = 0

        while has_next:
            logging.debug('Processing page %d...' % page)
            response = self.get_page(endpoint=endpoint, params=params, data=data, page=page)
            logging.debug('Found %d results...' % len(response.json()))

            for entry in response.json():
                if limit is None or found < limit:
                    found += 1
                    yield entry
                else:
                    has_next = False
                    break

            if has_next and 'next' in response.links:
                parsed = urlparse(response.links['next']['url'])
                page = int(parse_qs(parsed.query)['page'][0])
            else:
                has_next = False

    def one(self, record_id):
        """
        Base method to get one by id, should be implemented in child resource class.
        If a resource does not support getting one record by id, raise NotImplement exception.
        """
        raise NotImplementedError('This resource does not support get_one_by_id')

    def get_one_by_id(self, endpoint, record_id, params=None):
        """
        Returns one record by ID.

        :param endpoint: The resource endpoint.
        :type endpoint: str

        :param record_id: The record ID.
        :type record_id: int, str

        :param params: The list of tuples or bytes to send in the query string for the request.
        :type params: dict, optional

        :return: The record dictionary, raises exception if record not found
        :rtype: Dict[str, Any]:
        """
        if params is None:
            params = {}

        url = self._trim_endpoint(endpoint) + '/' + str(record_id)

        response = self._api_client.send(method='get', endpoint=url, params=params)

        if response:
            return response.json()

    def _trim_endpoint(self, endpoint):
        """Trim slashes from start and end of the given endpoint

        :param endpoint: The endpoint.
        :type endpoint: str

        :return: The endpoint.
        :rtype: str
        """
        if endpoint.startswith('/'):
            endpoint = endpoint[1:]

        if endpoint.endswith('/'):
            endpoint = endpoint[:-1]

        return endpoint
