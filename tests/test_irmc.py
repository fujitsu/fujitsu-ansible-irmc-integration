#!/usr/bin/python

# see https://www.relaxdiego.com/2016/09/writing-ansible-modules-002.html


# FUJITSU Limited
# Copyright (C) FUJITSU Limited 2018
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division)
__metaclass__ = type


import json
import mock
import requests
from requests.exceptions import Timeout

from ansible.compat.tests import unittest
from ansible.compat.tests.mock import create_autospec, patch
from ansible.module_utils.basic import AnsibleModule

from module_utils import irmc


# pylint: disable=too-many-public-methods
# pylint: disable=unused-argument
class TestIrmc(unittest.TestCase):

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

    @patch.object(requests.Session, 'get')
    def test__irmc_redfish_get__all_is_well(self, get):
        requests.Session.get.return_value = self.mockdata
        status, data, msg = irmc.irmc_redfish_get(self.mod, "redfish_path")
        self.assertEqual(self.mockdata.status_code, status)
        self.assertEqual(self.mockdata.json.return_value, data.json.return_value)
        self.assertEqual("OK", msg)

    @patch.object(requests.Session, 'get')
    def test__irmc_redfish_get__bad_status_without_reason(self, get):
        requests.Session.get.return_value = self.mockdata
        self.mockdata.status_code = 100
        status, data, msg = irmc.irmc_redfish_get(self.mod, "redfish_path")
        self.assertEqual(self.mockdata.status_code, status)
        self.assertEqual(self.mockdata.json.return_value, data.json.return_value)
        self.assertEqual("GET request was not successful (" + self.url + ").", msg)

    @patch.object(requests.Session, 'get')
    def test__irmc_redfish_get__bad_status_with_reason(self, get):
        requests.Session.get.return_value = self.mockdata
        self.mockdata.json.return_value = self.mockdata.bad_return
        self.mockdata.status_code = 100
        status, data, msg = irmc.irmc_redfish_get(self.mod, "redfish_path")
        self.assertEqual(self.mockdata.status_code, status)
        self.assertEqual(self.mockdata.json.return_value, data.json.return_value)
        self.assertEqual("GET request was not successful (" + self.url + "): " + self.mockdata.reason, msg)

    @patch.object(requests.Session, 'get')
    def test__irmc_redfish_get__exception(self, get):
        requests.Session.get.side_effect = Timeout()
        status, data, msg = irmc.irmc_redfish_get(self.mod, "redfish_path")
        self.assertEqual(status, 99)
        self.assertIn("Traceback", str(data))
        self.assertIn("GET request encountered exception (" + self.url + ")", msg)

    @patch.object(requests.Session, 'patch')
    def test__irmc_redfish_patch__all_is_well(self, patch):    # pylint: disable=redefined-outer-name
        requests.Session.patch.return_value = self.mockdata
        status, data, msg = irmc.irmc_redfish_patch(self.mod, "redfish_path", json.dumps({'Patch': 'mockpatch'}), 12345)
        self.assertEqual(self.mockdata.status_code, status)
        self.assertEqual(self.mockdata.json.return_value, data.json.return_value)
        self.assertEqual("OK", msg)

    @patch.object(requests.Session, 'patch')
    def test__irmc_redfish_patch__etag_is_good_string(self, patch):    # pylint: disable=redefined-outer-name
        requests.Session.patch.return_value = self.mockdata
        status, data, msg = irmc.irmc_redfish_patch(self.mod, "redfish_path", json.dumps({'Patch': 'mockpatch'}),
                                                    "12345")
        self.assertEqual(self.mockdata.status_code, status)
        self.assertEqual(self.mockdata.json.return_value, data.json.return_value)
        self.assertEqual("OK", msg)

    @patch.object(requests.Session, 'patch')
    def test__irmc_redfish_patch__etag_is_extra_large(self, patch):    # pylint: disable=redefined-outer-name
        requests.Session.patch.return_value = self.mockdata
        status, data, msg = irmc.irmc_redfish_patch(self.mod, "redfish_path", json.dumps({'Patch': 'mockpatch'}),
                                                    1234567890123456789)
        self.assertEqual(self.mockdata.status_code, status)
        self.assertEqual(self.mockdata.json.return_value, data.json.return_value)
        self.assertEqual("OK", msg)

    @patch.object(requests.Session, 'patch')
    def test__irmc_redfish_patch__bad_etag(self, patch):    # pylint: disable=redefined-outer-name
        requests.Session.patch.return_value = self.mockdata
        etag = "abcde"
        status, data, msg = irmc.irmc_redfish_patch(self.mod, "redfish_path", json.dumps({'Patch': 'mockpatch'}), etag)
        self.assertEqual(97, status)
        self.assertEqual("etag is no number: " + etag, data)
        self.assertEqual("etag is no number: " + etag, msg)

    @patch.object(requests.Session, 'patch')
    def test__irmc_redfish_patch__bad_status_without_reason(self, patch):    # pylint: disable=redefined-outer-name
        requests.Session.patch.return_value = self.mockdata
        self.mockdata.status_code = 100
        status, data, msg = irmc.irmc_redfish_patch(self.mod, "redfish_path", json.dumps({'Patch': 'mockpatch'}), 12345)
        self.assertEqual(self.mockdata.status_code, status)
        self.assertEqual(self.mockdata.json.return_value, data.json.return_value)
        self.assertEqual("PATCH request was not successful (" + self.url + ").", msg)

    @patch.object(requests.Session, 'patch')
    def test__irmc_redfish_patch__bad_status_with_reason(self, patch):    # pylint: disable=redefined-outer-name
        requests.Session.patch.return_value = self.mockdata
        self.mockdata.json.return_value = self.mockdata.bad_return
        self.mockdata.status_code = 100
        status, data, msg = irmc.irmc_redfish_patch(self.mod, "redfish_path", json.dumps({'Patch': 'mockpatch'}), 12345)
        self.assertEqual(self.mockdata.status_code, status)
        self.assertEqual(self.mockdata.json.return_value, data.json.return_value)
        self.assertEqual("PATCH request was not successful (" + self.url + "): " + self.mockdata.reason, msg)

    @patch.object(requests.Session, 'patch')
    def test__irmc_redfish_patch__bad_body(self, patch):    # pylint: disable=redefined-outer-name
        requests.Session.patch.return_value = self.mockdata
        status, data, msg = irmc.irmc_redfish_patch(self.mod, "redfish_path", "{ 'Patch': 'mockpatch' }", 12345)
        self.assertEqual(98, status)
        self.assertIn("Traceback", str(data))
        self.assertIn("PATCH request got invalid JSON body", msg)

    @patch.object(requests.Session, 'patch')
    def test__irmc_redfish_patch__exception(self, patch):    # pylint: disable=redefined-outer-name
        requests.Session.patch.side_effect = Timeout()
        status, data, msg = irmc.irmc_redfish_patch(self.mod, "redfish_path", json.dumps({'Patch': 'mockpatch'}), 12345)
        self.assertEqual(99, status)
        self.assertIn("Traceback", str(data))
        self.assertIn("PATCH request encountered exception (" + self.url + ")", msg)

    @patch.object(requests.Session, 'post')
    def test__irmc_redfish_post__all_is_well(self, post):
        requests.Session.post.return_value = self.mockdata
        status, data, msg = irmc.irmc_redfish_post(self.mod, "redfish_path", json.dumps({'Patch': 'mockpatch'}))
        self.assertEqual(self.mockdata.status_code, status)
        self.assertEqual(self.mockdata.json.return_value, data.json.return_value)
        self.assertEqual("OK", msg)

    @patch.object(requests.Session, 'post')
    def test__irmc_redfish_post__bad_status_without_reason(self, post):
        requests.Session.post.return_value = self.mockdata
        self.mockdata.status_code = 100
        status, data, msg = irmc.irmc_redfish_post(self.mod, "redfish_path", json.dumps({'Patch': 'mockpatch'}))
        self.assertEqual(self.mockdata.status_code, status)
        self.assertEqual(self.mockdata.json.return_value, data.json.return_value)
        self.assertEqual("POST request was not successful (" + self.url + ").", msg)

    @patch.object(requests.Session, 'post')
    def test__irmc_redfish_post__bad_status_with_reason(self, post):
        requests.Session.post.return_value = self.mockdata
        self.mockdata.json.return_value = self.mockdata.bad_return
        self.mockdata.status_code = 100
        status, data, msg = irmc.irmc_redfish_post(self.mod, "redfish_path", json.dumps({'Patch': 'mockpatch'}))
        self.assertEqual(self.mockdata.status_code, status)
        self.assertEqual(self.mockdata.json.return_value, data.json.return_value)
        self.assertEqual("POST request was not successful (" + self.url + "): " + self.mockdata.reason, msg)

    @patch.object(requests.Session, 'post')
    def test__irmc_redfish_post__bad_body(self, post):
        requests.Session.post.return_value = self.mockdata
        status, data, msg = irmc.irmc_redfish_post(self.mod, "redfish_path", "{ 'Patch': 'mockpatch' }")
        self.assertEqual(98, status)
        self.assertIn("Traceback", str(data))
        self.assertIn("POST request got invalid JSON body", msg)

    @patch.object(requests.Session, 'post')
    def test__irmc_redfish_post__exception(self, post):
        requests.Session.post.side_effect = Timeout()
        status, data, msg = irmc.irmc_redfish_post(self.mod, "redfish_path", json.dumps({'Patch': 'mockpatch'}))
        self.assertEqual(99, status)
        self.assertIn("Traceback", str(data))
        self.assertIn("POST request encountered exception (" + self.url + ")", msg)

    def test__get_irmc_json__all_is_well(self):
        result0 = irmc.get_irmc_json(self.mockjson, "Level0Key")
        result1 = irmc.get_irmc_json(self.mockjson, ["Level1", "Level1Key"])
        result2 = irmc.get_irmc_json(self.mockjson, ["Level1", "Level2", "Level2Key"])
        result3 = irmc.get_irmc_json(self.mockjson, ["Level1", "Level2", "Level3", "Level3Key"])
        result4 = irmc.get_irmc_json(self.mockjson, ["Level1", "Level2", "Level3", "Level4", "Level4Key"])
        result5 = irmc.get_irmc_json(self.mockjson, ["Level1", "Level2", "Level3", "Level4", "Level5", "Level5Key"])
        self.assertEqual("MockLevel0Data", result0)
        self.assertEqual("MockLevel1Data", result1)
        self.assertEqual("MockLevel2Data", result2)
        self.assertEqual("MockLevel3Data", result3)
        self.assertEqual("MockLevel4Data", result4)
        self.assertEqual("MockLevel5Data", result5)

    def test__get_irmc_json__key_too_long(self):
        key = ["Level1", "Level2", "Level3", "Level4", "Level5", "Level6", "Level6Key"]
        jsonkey = " ".join(key)
        result = irmc.get_irmc_json(self.mockjson, key)
        self.assertEqual("Key too long (7 levels): '" + jsonkey + "'", result)

    def test__get_irmc_json__key_does_not_exist(self):
        key = "InvalidKey"
        result = irmc.get_irmc_json(self.mockjson, key)
        self.assertEqual("Key does not exist: '" + key + "'", result)


if __name__ == '__main__':
    unittest.main()
