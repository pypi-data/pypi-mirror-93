from cyjax.helpers import DateHelper
from cyjax.resources.resource import Resource


class MaliciousDomain(Resource):

    def __init__(self, api_key=None, api_url=None):
        """
        :param api_key: The API key.
        :param api_url: The Cyjax API url.
        """
        super(MaliciousDomain, self).__init__(api_key=api_key, api_url=api_url)

    def list(self, since=None, until=None, limit=None):
        """
        Returns potential malicious domains.

        :param since: The start date time.
        :type since: (datetime, timedelta, str), optional

        :param until: The end date time.
        :type until:  (datetime, timedelta, str), optional

        :param limit: The limit of items to fetch. If limit is None returns all items for a collection.
        :type limit: int

        :return: The list generator for potential malicious domains.
        :rtype Generator[dict]
        """

        params = DateHelper.build_date_params(since=since, until=until)
        return self.paginate(endpoint='domain-monitor/potential-malicious-domain', params=params, limit=limit)
