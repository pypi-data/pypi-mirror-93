from cyjax.helpers import DateHelper
from cyjax.resources.resource import Resource


class LeakedEmail(Resource):

    def __init__(self, api_key=None, api_url=None):
        """
        :param api_key: The API key
        :param api_url: The API URL.
        """
        super(LeakedEmail, self).__init__(api_key=api_key, api_url=api_url)

    def list(self, query=None, since=None, until=None):
        """
        Returns leaked emails.
        :param query: The search query.
        :type query: str, optional
        :param since: The start date time. time.
        :type since: (datetime, timedelta, str), optional
        :param until: The end date time.
        :type until:  (datetime, timedelta, str), optional
        :return: The list of leaked emails.
        :rtype list
        """

        params = DateHelper.build_date_params(since=since, until=until)
        if query:
            params.update({'query': query})

        return self.paginate(endpoint='data-leak/credentials', params=params)

    def one(self, record_id):
        """
        Get one record by ID

        :param record_id: The record ID
        :type record_id: int, str

        :return: The record dictionary, raises exception if record not found
        :rtype: Dict[str, Any]:
        """
        return self.get_one_by_id(endpoint='data-leak/credentials', record_id=record_id)
