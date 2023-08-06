import datetime
from datetime import timedelta
from unittest.mock import patch, Mock

import pytest
import pytz

import cyjax
from cyjax import MyReport, InvalidDateFormatException


class TestMyReport:

    fake_date = Mock(wraps=datetime.datetime)
    fake_date.now.return_value.astimezone.return_value = datetime.datetime(2020, 5, 2, 12, 0, 0, tzinfo=pytz.UTC)

    def test_get_my_reports_without_parameters(self, mocker):
        my_report = MyReport()
        spy_method_paginate = mocker.spy(my_report, 'paginate')

        my_report.list()
        spy_method_paginate.assert_called_once_with(endpoint='report/my-report', params={}, limit=None)

    def test_get_incident_reports_with_parameters(self, mocker):
        my_report = MyReport()
        spy_method_paginate = mocker.spy(my_report, 'paginate')

        my_report.list(query='search-query', since='2020-05-02T07:31:11+00:00', until='2020-07-02T00:00:00+00:00')

        expected_params = {
            'query': 'search-query',
            'since': '2020-05-02T07:31:11+00:00',
            'until': '2020-07-02T00:00:00+00:00'
        }
        spy_method_paginate.assert_called_once_with(endpoint='report/my-report', params=expected_params, limit=None)

    @patch('cyjax.helpers.datetime', fake_date)
    def test_get_incident_reports_with_date_as_timedelta(self, mocker):
        my_report = MyReport()
        spy_method_paginate = mocker.spy(my_report, 'paginate')

        my_report.list(since=timedelta(hours=2), until=timedelta(hours=1))

        since = '2020-05-02T10:00:00+00:00'
        until = '2020-05-02T11:00:00+00:00'
        expected_params = {'since': since, 'until': until}

        spy_method_paginate.assert_called_once_with(endpoint='report/my-report', params=expected_params, limit=None)

    def test_get_incident_reports_with_date_as_datetime_without_timezone(self, mocker):
        my_report = MyReport()
        spy_method_paginate = mocker.spy(my_report, 'paginate')

        my_report.list(since=datetime.datetime(2020, 5, 2, 10, 0, 0), until=datetime.datetime(2020, 5, 2, 11, 0, 0))

        since = datetime.datetime(2020, 5, 2, 10, 0, 0).astimezone().isoformat()
        until = datetime.datetime(2020, 5, 2, 11, 0, 0).astimezone().isoformat()
        expected_params = {'since': since, 'until': until}

        spy_method_paginate.assert_called_once_with(endpoint='report/my-report', params=expected_params, limit=None)

    def test_get_incident_reports_with_date_as_datetime_with_timezone(self, mocker):
        my_report = MyReport()
        spy_method_paginate = mocker.spy(my_report, 'paginate')

        my_report.list(since=datetime.datetime(2020, 5, 2, 10, 0, 0, tzinfo=pytz.UTC),
                       until=datetime.datetime(2020, 5, 2, 11, 0, 0, tzinfo=pytz.UTC))

        expected_params = {'since': '2020-05-02T10:00:00+00:00', 'until': '2020-05-02T11:00:00+00:00'}

        spy_method_paginate.assert_called_once_with(endpoint='report/my-report', params=expected_params, limit=None)

    def test_get_incident_reports_with_date_as_string(self, mocker):
        my_report = MyReport()
        spy_method_paginate = mocker.spy(my_report, 'paginate')

        my_report.list(since='2020-05-02T10:00:00+00:00', until='2020-05-02T11:00:00+00:00')

        expected_params = {'since': '2020-05-02T10:00:00+00:00', 'until': '2020-05-02T11:00:00+00:00'}

        spy_method_paginate.assert_called_once_with(endpoint='report/my-report', params=expected_params, limit=None)

    def test_get_incident_reports_with_wrong_date(self):
        my_report = MyReport()
        with pytest.raises(InvalidDateFormatException):
            my_report.list(since='2020-05', until='2020-05-02T11:00:00+00:00')

        with pytest.raises(InvalidDateFormatException):
            my_report.list(since='2020-05-02T11:00:00+00:00', until='2020-05')

    def test_setting_client(self):
        cyjax.api_key = None  # reset to defaults

        my_report = MyReport()
        assert 'https://api.cyberportal.co' == my_report._api_client.get_api_url()
        assert my_report._api_client.get_api_key() is None

        my_report = MyReport('123456', 'https://api.new-address.com')
        assert 'https://api.new-address.com' == my_report._api_client.get_api_url()
        assert '123456' == my_report._api_client.get_api_key()

        cyjax.api_url = None  # Reset to default

    def test_get_one_by_id(self, mocker):
        my_report = MyReport()
        my_report._api_client = Mock()

        spy_method_get_one_by_id = mocker.spy(my_report, 'get_one_by_id')

        assert hasattr(my_report, 'one')
        my_report.one(400)

        spy_method_get_one_by_id.assert_called_once_with(endpoint='report/my-report', record_id=400)

    def test_list_with_limit(self, mocker):
        resource = MyReport()
        spy_method_paginate = mocker.spy(resource, 'paginate')

        resource.list(limit=300)
        spy_method_paginate.assert_called_once_with(endpoint='report/my-report', params={}, limit=300)
