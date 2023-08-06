import datetime
import logging
from datetime import timedelta
from unittest.mock import patch, Mock

import pytest
import pytz

import cyjax
from cyjax import IncidentReport, IndicatorOfCompromise, InvalidDateFormatException


class TestIncidentReport:

    fake_date = Mock(wraps=datetime.datetime)
    fake_date.now.return_value.astimezone.return_value = datetime.datetime(2020, 5, 2, 12, 0, 0, tzinfo=pytz.UTC)

    def test_get_incident_reports_without_parameters(self, mocker):
        incident_report = IncidentReport()
        spy_method_paginate = mocker.spy(incident_report, 'paginate')

        incident_report.list()
        spy_method_paginate.assert_called_once_with(endpoint='report/incident', params={'excludeIndicators': True},
                                                    limit=None)

    def test_get_incident_reports_with_parameters(self, mocker):
        incident_report = IncidentReport()
        spy_method_paginate = mocker.spy(incident_report, 'paginate')

        incident_report.list(query='search-query', since='2020-05-02T07:31:11+00:00', until='2020-07-02T00:00:00+00:00')

        expected_params = {
            'query': 'search-query',
            'since': '2020-05-02T07:31:11+00:00',
            'until': '2020-07-02T00:00:00+00:00',
            'excludeIndicators': True
        }
        spy_method_paginate.assert_called_once_with(endpoint='report/incident', params=expected_params, limit=None)

    @patch('cyjax.helpers.datetime', fake_date)
    def test_get_incident_reports_with_date_as_timedelta(self, mocker):
        incident_report = IncidentReport()
        spy_method_paginate = mocker.spy(incident_report, 'paginate')

        incident_report.list(since=timedelta(hours=2), until=timedelta(hours=1))

        since = '2020-05-02T10:00:00+00:00'
        until = '2020-05-02T11:00:00+00:00'
        expected_params = {'since': since, 'until': until, 'excludeIndicators': True}

        spy_method_paginate.assert_called_once_with(endpoint='report/incident', params=expected_params, limit=None)

    def test_get_incident_reports_with_date_as_datetime_without_timezone(self, mocker):
        incident_report = IncidentReport()
        spy_method_paginate = mocker.spy(incident_report, 'paginate')

        incident_report.list(since=datetime.datetime(2020, 5, 2, 10, 0, 0), until=datetime.datetime(2020, 5, 2, 11, 0, 0))

        since = datetime.datetime(2020, 5, 2, 10, 0, 0).astimezone().isoformat()
        until = datetime.datetime(2020, 5, 2, 11, 0, 0).astimezone().isoformat()
        expected_params = {'since': since, 'until': until, 'excludeIndicators': True}

        spy_method_paginate.assert_called_once_with(endpoint='report/incident', params=expected_params, limit=None)

    def test_get_incident_reports_with_date_as_datetime_with_timezone(self, mocker):
        incident_report = IncidentReport()
        spy_method_paginate = mocker.spy(incident_report, 'paginate')

        incident_report.list(since=datetime.datetime(2020, 5, 2, 10, 0, 0, tzinfo=pytz.UTC),
                             until=datetime.datetime(2020, 5, 2, 11, 0, 0, tzinfo=pytz.UTC))

        expected_params = {'since': '2020-05-02T10:00:00+00:00',
                           'until': '2020-05-02T11:00:00+00:00',
                           'excludeIndicators': True}

        spy_method_paginate.assert_called_once_with(endpoint='report/incident', params=expected_params, limit=None)

    def test_get_incident_reports_with_date_as_string(self, mocker):
        incident_report = IncidentReport()
        spy_method_paginate = mocker.spy(incident_report, 'paginate')

        incident_report.list(since='2020-05-02T10:00:00+00:00', until='2020-05-02T11:00:00+00:00')

        expected_params = {'since': '2020-05-02T10:00:00+00:00',
                           'until': '2020-05-02T11:00:00+00:00',
                           'excludeIndicators': True}

        spy_method_paginate.assert_called_once_with(endpoint='report/incident', params=expected_params, limit=None)

    def test_get_incident_reports_with_wrong_date(self):
        incident_report = IncidentReport()
        with pytest.raises(InvalidDateFormatException):
            incident_report.list(since='2020-05', until='2020-05-02T11:00:00+00:00')

        with pytest.raises(InvalidDateFormatException):
            incident_report.list(since='2020-05-02T11:00:00+00:00', until='2020-05')

    def test_setting_client(self):
        cyjax.api_key = None  # reset to defaults

        resource = IncidentReport()
        assert 'https://api.cyberportal.co' == resource._api_client.get_api_url()
        assert resource._api_client.get_api_key() is None

        resource = IncidentReport('123456', 'https://api.new-address.com')
        assert 'https://api.new-address.com' == resource._api_client.get_api_url()
        assert '123456' == resource._api_client.get_api_key()

        cyjax.api_url = None  # Reset to default

    def test_get_one_by_id(self, mocker):
        incident_report = IncidentReport()
        incident_report._api_client = Mock()

        spy_method_get_one_by_id = mocker.spy(incident_report, 'get_one_by_id')

        assert hasattr(incident_report, 'one')
        incident_report.one(400)

        spy_method_get_one_by_id.assert_called_once_with(endpoint='report/incident', record_id=400,
                                                         params={'excludeIndicators': True})

    @patch.object(IndicatorOfCompromise, 'paginate', return_value=[])
    def test_get_report_indicators_no_indicators(self, ioc_class_mock):
        indicators = IncidentReport().indicators(1234)
        assert isinstance(indicators, list)
        assert len(indicators) == 0

    @patch.object(IndicatorOfCompromise, 'paginate', return_value=[
        {
            "type": "IPv6",
            "industry_type": [
                "maritime",
                "Law Enforcement"
            ],
            "value": "2001:4b8:2:101::602",
            "handling_condition": "GREEN",
            "discovered_at": "2020-12-23T10:01:12+0000",
            "description": "Report with IP iocs",
            "source": "http://test-domain.com/view?id=100"
        },
        {
            "type": "IPv6",
            "industry_type": [
                "maritime",
                "Law Enforcement"
            ],
            "value": "2606:4700:4700::1111",
            "handling_condition": "GREEN",
            "discovered_at": "2020-12-23T10:01:12+0000",
            "description": "Report with IP iocs",
            "source": "http://test-domain.com/view?id=101"
        }
    ])

    def test_get_report_indicators_two_indicators_found(self, ioc_class_mock):
        indicators = IncidentReport().indicators(1234)
        assert isinstance(indicators, list)
        assert len(indicators) == 2

        assert 'IPv6' == indicators[0].get('type')
        assert 'IPv6' == indicators[1].get('type')

        assert '2001:4b8:2:101::602' == indicators[0].get('value')
        assert '2606:4700:4700::1111' == indicators[1].get('value')

    def test_get_list_exclude_indicators_filter_default(self, mocker):
        incident_report = IncidentReport()
        spy_method_paginate = mocker.spy(incident_report, 'paginate')

        # default
        incident_report.list(since=datetime.datetime(2020, 5, 2, 10, 0, 0, tzinfo=pytz.UTC),
                             until=datetime.datetime(2020, 5, 2, 11, 0, 0, tzinfo=pytz.UTC))

        expected_params = {'since': '2020-05-02T10:00:00+00:00',
                           'until': '2020-05-02T11:00:00+00:00',
                           'excludeIndicators': True}
        spy_method_paginate.assert_called_once_with(endpoint='report/incident', params=expected_params, limit=None)


    def test_get_list_without_excluding_indicators_filter(self, mocker):
        incident_report = IncidentReport()
        spy_method_paginate = mocker.spy(incident_report, 'paginate')

        # False
        incident_report.list(since=datetime.datetime(2020, 5, 2, 10, 0, 0, tzinfo=pytz.UTC),
                             until=datetime.datetime(2020, 5, 2, 11, 0, 0, tzinfo=pytz.UTC, ),
                             exclude_indicators=False)

        expected_params = {'since': '2020-05-02T10:00:00+00:00',
                           'until': '2020-05-02T11:00:00+00:00',
                           'excludeIndicators': False}

        spy_method_paginate.assert_called_once_with(endpoint='report/incident', params=expected_params, limit=None)

    def test_get_list_excluding_indicators_filter(self, mocker):
        incident_report = IncidentReport()
        spy_method_paginate = mocker.spy(incident_report, 'paginate')

        # True
        incident_report.list(since=datetime.datetime(2020, 5, 2, 10, 0, 0, tzinfo=pytz.UTC),
                             until=datetime.datetime(2020, 5, 2, 11, 0, 0, tzinfo=pytz.UTC, ),
                             exclude_indicators=True)

        expected_params = {'since': '2020-05-02T10:00:00+00:00',
                           'until': '2020-05-02T11:00:00+00:00',
                           'excludeIndicators': True}

        spy_method_paginate.assert_called_once_with(endpoint='report/incident', params=expected_params, limit=None)

    def test_get_one_exclude_indicators_filter(self, mocker):
        incident_report = IncidentReport()
        incident_report._api_client = Mock()

        spy_method_get_one_by_id = mocker.spy(incident_report, 'get_one_by_id')

        assert hasattr(incident_report, 'one')
        incident_report.one(400)

        # default
        spy_method_get_one_by_id.assert_called_once_with(endpoint='report/incident', record_id=400,
                                                         params={'excludeIndicators': True})

        # False
        incident_report.one(400, exclude_indicators=False)
        spy_method_get_one_by_id.assert_called_with(endpoint='report/incident', record_id=400,
                                                    params={'excludeIndicators': False})

        # True
        incident_report.one(400, exclude_indicators=True)
        spy_method_get_one_by_id.assert_called_with(endpoint='report/incident', record_id=400,
                                                    params={'excludeIndicators': True})

    def test_list_with_limit(self, mocker):
        resource = IncidentReport()
        spy_method_paginate = mocker.spy(resource, 'paginate')

        resource.list(limit=300)
        spy_method_paginate.assert_called_once_with(endpoint='report/incident',
                                                    params={'excludeIndicators': True}, limit=300)
