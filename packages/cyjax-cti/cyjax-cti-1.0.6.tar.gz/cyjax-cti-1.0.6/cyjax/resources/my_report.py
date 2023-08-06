from cyjax.helpers import DateHelper
from cyjax.resources.resource import Resource


class MyReport(Resource):

    def __init__(self, api_key=None, api_url=None):
        """
        :param api_key: The API key.
        :param api_url: The API URL.
        """
        super(MyReport, self).__init__(api_key=api_key, api_url=api_url)

    def list(self, query=None, since=None, until=None, limit=None):
        """
        Returns my reports.

        :param query: The search query.
        :type query: str, optional

        :param since: The start date time.
        :type since: (datetime, timedelta, str), optional

        :param until: The end date time.
        :type until:  (datetime, timedelta, str), optional

        :param limit: The limit of items to fetch. If limit is None returns all items for a collection.
        :type limit: int

        :return: The list generator for incident reports.
        :rtype Generator[dict]
        """
        params = DateHelper.build_date_params(since=since, until=until)
        if query:
            params.update({'query': query})

        return self.paginate(endpoint='report/my-report', params=params, limit=limit)

    def one(self, report_id):
        """
        Get one record by ID

        :param report_id: The my report ID
        :type report_id: int, str

        :return: The record dictionary, raises exception if record not found
        :rtype: Dict[str, Any]:
        """
        return self.get_one_by_id(endpoint='report/my-report', record_id=report_id)
