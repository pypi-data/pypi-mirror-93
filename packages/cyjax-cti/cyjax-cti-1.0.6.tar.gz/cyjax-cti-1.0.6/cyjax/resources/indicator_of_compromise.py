from cyjax.helpers import DateHelper
from cyjax.resources.resource import Resource


class IndicatorOfCompromise(Resource):

    SUPPORTED_TYPES = ['IPv4', 'IPv6', 'Domain', 'Hostname', 'Email', 'FileHash-SHA1', 'FileHash-SHA256',
                       'FileHash-MD5', 'FileHash-SSDEEP']

    SUPPORTED_SOURCES = ['incident-report', 'my-report']

    def __init__(self, api_key=None, api_url=None):
        """
        :param api_key: The API key.
        :param api_url: The API URL.
        """
        super(IndicatorOfCompromise, self).__init__(api_key=api_key, api_url=api_url)

    def list(self, since=None, until=None, type=None, source_type=None, source_id=None, limit=None):
        """
        Returns indicators of compromise.

        :param since: The start date time.
        :type since: (datetime, timedelta, str), optional

        :param until: The end date time.
        :type until:  (datetime, timedelta, str), optional

        :param type: The indicator type. If not specified all indicators are returned.
            Allowed values are: IPv4, IPv6, Domain, Hostname, Email, FileHash-SHA1, FileHash-SHA256, FileHash-MD5,
            FileHash-SSDEEP.
        :type type:  (str), optional

        :param source_type: The indicators source type. Allowed values are: incident-report, my-report.
        :type source_type:  (str), optional

        :param source_id: The indicators source ID.
        :type source_id:  (int), optional

        :param limit: The limit of items to fetch. If limit is None returns all items for a collection.
        :type limit: int

        :return: The list generator for indicators of compromise.
        :rtype Generator[dict]
        """

        params = DateHelper.build_date_params(since=since, until=until)

        if type is not None:
            if type in IndicatorOfCompromise.SUPPORTED_TYPES:
                params['type'] = type
            else:
                raise ValueError('Invalid type. Check supported types.')

        if source_type is not None:
            if source_type in IndicatorOfCompromise.SUPPORTED_SOURCES:
                params['sourceType'] = source_type
            else:
                raise ValueError('Invalid source_type. Check supported sources.')

        if source_id is not None:
            if source_id > 0:
                params['sourceId'] = source_id
            else:
                raise ValueError('Invalid source_id')

        return self.paginate(endpoint='indicator-of-compromise', params=params, limit=limit)

    def enrichment(self, value):
        """
        Get the enrichment metadata for the given indicator value

        :param value: The indicator value.
        :type value: str

        :return: The enrichment metadata
        :rtype dict
        """
        if not value or not isinstance(value, str):
            raise ValueError('Indicator value is invalid')

        response = self._api_client.send(method='get', endpoint='indicator-of-compromise/enrichment',
                                         params={'value': value})

        return response.json()
