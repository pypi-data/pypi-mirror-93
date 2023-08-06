from cyjax.helpers import DateHelper
from cyjax.resources.resource import Resource
from cyjax.resources.indicator_of_compromise import IndicatorOfCompromise


class IncidentReport(Resource):

    def __init__(self, api_key=None, api_url=None):
        """
        :param api_key: The API key.
        :param api_url: The API URL.
        """
        super(IncidentReport, self).__init__(api_key=api_key, api_url=api_url)

    def list(self, query=None, since=None, until=None, exclude_indicators=True, limit=None):
        """
        Returns incident reports.

        :param query: The search query.
        :type query: str, optional

        :param since: The start date time.
        :type since: (datetime, timedelta, str), optional

        :param until: The end date time.
        :type until:  (datetime, timedelta, str), optional

        :param exclude_indicators: Whether to exclude indicators from Api response. Defaults to True
        :type exclude_indicators:  bool, optional

        :param limit: The limit of items to fetch. If limit is None returns all items for a collection.
        :type limit: int

        :return: The list generator for incident reports.
        :rtype Generator[dict]
        """
        params = DateHelper.build_date_params(since=since, until=until)
        if query:
            params.update({'query': query})

        params['excludeIndicators'] = exclude_indicators

        return self.paginate(endpoint='report/incident', params=params, limit=limit)

    def one(self, report_id, exclude_indicators=True):
        """
        Get one record by ID

        :param report_id: The record ID
        :type report_id: int, str

        :param exclude_indicators: Whether to exclude indicators from Api response. Defaults to True
        :type exclude_indicators:  bool, optional

        :return: The record dictionary, raises exception if record not found
        :rtype: Dict[str, Any]:
        """

        params = {'excludeIndicators': exclude_indicators}

        return self.get_one_by_id(endpoint='report/incident', record_id=report_id, params=params)

    def indicators(self, report_id):
        """
        Return list of IndicatorOfCompromise that are assigned to the IncidentReport

        :param report_id: The IncidentReport ID
        :type report_id: int, str

        :return: The list of IndicatorOfCompromise assigned to the report.
        :rtype: List[Dict[str, Any]]:
        """
        return IndicatorOfCompromise().list(source_type='incident-report', source_id=report_id)
