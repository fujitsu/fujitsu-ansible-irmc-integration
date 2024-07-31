#!/usr/bin/python

# Copyright 2018-2024 Fsas Technologies Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division)
__metaclass__ = type

import builtins
try:               # check whether python knows about '__builtin__'
    __builtin__.open
except NameError:  # no, so it is python3, use 'builtins' instead
    __builtin__ = builtins

import requests
from requests.exceptions import Timeout
import mock

from ansible.compat.tests import unittest
from ansible.compat.tests.mock import create_autospec, patch
from ansible.module_utils.basic import AnsibleModule

from module_utils import irmc_upload_file


class TestIrmcUploadFile(unittest.TestCase):

    # preparing the tests
    def setUp(self):
        mod_cls = create_autospec(AnsibleModule)
        mod = mod_cls.return_value
        mod.params = dict(
            irmc_url="irmc_dns_or_ip",
            irmc_username="admin",
            irmc_password="admin",
            validate_certs=True
        )

        mockdata = mock.Mock()
        mockdata.reason = "mocked error reason"
        mockdata.bad_return = {'Data': 'mockdata', 'error': {'message': mockdata.reason}}
        mockdata.json.return_value = {'Data': 'mockdata'}
        mockdata.status_code = 200

        # unittest.TestCase.setUp(self)
        self.mod = mod
        self.mockdata = mockdata
        self.url = "https://{0}/redfish_path".format(mod.params['irmc_url'])
        self.mockjson = {"Level0Key": "MockLevel0Data",
                         "Level1": {"Level1Key": "MockLevel1Data",
                                    "Level2": {"Level2Key": "MockLevel2Data",
                                               "Level3": {"Level3Key": "MockLevel3Data",
                                                          "Level4": {"Level4Key": "MockLevel4Data",
                                                                     "Level5": {"Level5Key": "MockLevel5Data"}}}}}}

    # ending the test
    def tearDown(self):
        self.mockdata.dispose()
        self.mockdata = None

    @patch.object(requests.Session, 'post')
    @patch("__builtin__.open", mock.mock_open(read_data="data"))
    def test__irmc_redfish_post_file__all_is_well(self, post):
        requests.Session.post.return_value = self.mockdata
        open.return_value = "some filedata"
        status, data, msg = irmc_upload_file.irmc_redfish_post_file(self.mod, "redfish_path", "filename")
        self.assertEqual(self.mockdata.status_code, status)
        self.assertEqual(self.mockdata.json.return_value, data.json.return_value)
        self.assertEqual("OK", msg)

    @patch.object(requests.Session, 'post')
    @patch("__builtin__.open", mock.mock_open(read_data="data"))
    def test__irmc_redfish_post_file__no_file(self, post):
        requests.Session.post.return_value = self.mockdata
        open.side_effect = Timeout()
        self.mockdata.status_code = 89
        status, data, msg = irmc_upload_file.irmc_redfish_post_file(self.mod, "redfish_path", "nofile")
        self.assertEqual(self.mockdata.status_code, status)
        self.assertIn("Traceback", str(data))
        self.assertIn("Could not read file at", msg)

    @patch.object(requests.Session, 'post')
    @patch("__builtin__.open", mock.mock_open(read_data="data"))
    def test__irmc_redfish_post_file__bad_status_with_reason(self, post):
        requests.Session.post.return_value = self.mockdata
        open.return_value = "some filedata"
        self.mockdata.json.return_value = self.mockdata.bad_return
        self.mockdata.status_code = 100
        status, data, msg = irmc_upload_file.irmc_redfish_post_file(self.mod, "redfish_path", "filename")
        self.assertEqual(self.mockdata.status_code, status)
        self.assertEqual(self.mockdata.json.return_value, data.json.return_value)
        self.assertEqual("POST request was not successful (" + self.url + "): " + self.mockdata.reason, msg)

    @patch.object(requests.Session, 'post')
    @patch("__builtin__.open", mock.mock_open(read_data="data"))
    def test__irmc_redfish_post_file__bad_status_without_reason(self, post):
        requests.Session.post.return_value = self.mockdata
        open.return_value = "some filedata"
        self.mockdata.status_code = 100
        status, data, msg = irmc_upload_file.irmc_redfish_post_file(self.mod, "redfish_path", "filename")
        self.assertEqual(self.mockdata.status_code, status)
        self.assertEqual(self.mockdata.json.return_value, data.json.return_value)
        self.assertEqual("POST request was not successful (" + self.url + ").", msg)

    # POST exception mock does not work here for unknown reason (2 try/except blocks?)
    # @patch.object(requests.Session, 'post')
    # @patch("__builtin__.open", mock.mock_open(read_data="data"))
    # def test__irmc_redfish_post_file__exception(self, post):
        # requests.Session.post.side_effect = Timeout()
        # open.return_value = "some filedata"
        # status, data, msg = irmc_upload_file.irmc_redfish_post_file(self.mod, "redfish_path", "filename")
        # self.assertEqual(99, status)
        # self.assertIn("Traceback", str(data))
        # self.assertIn("POST request encountered exception (" + self.url + ")", msg)


if __name__ == '__main__':
    unittest.main()
