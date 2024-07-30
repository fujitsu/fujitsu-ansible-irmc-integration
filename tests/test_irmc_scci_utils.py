#!/usr/bin/python

# Copyright 2018-2024 Fsas Technologies INC.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division)
__metaclass__ = type

from builtins import str

import requests
from requests.exceptions import Timeout
from lxml import objectify, etree
import mock

from ansible.compat.tests import unittest
from ansible.compat.tests.mock import create_autospec, patch
from ansible.module_utils.basic import AnsibleModule

from module_utils import irmc_scci_utils


class TestIrmcScciUtils(unittest.TestCase):

    # preparing the tests
    def setUp(self):
        mod_cls = create_autospec(AnsibleModule)
        mod = mod_cls.return_value
        mod.params = dict(
            irmc_url="irmc_dns_or_ip",
            irmc_username="admin",
            irmc_password="admin",
            validate_certs=True,
            index=0,
            cabid=-1
        )

        mockdata = mock.Mock()
        mockdata.reason = "mockdata error reason"
        mockdata.content = "<xml><cmd/></xml>"
        mockdata.status_code = 200

        scci_code_map = {"get_cs": "E001", "set_cs": "E002"}
        userdata = {"description": "", "enabled": ""}
        param_scci_map = [
            ["description", "ConfBMCAcctUserDescription", 0x1455, None],                # iRMC: Desciption
            ["enabled", "ConfBMCAcctUserEnable", 0x1457, {"0": "False", "1": "True"}],  # iRMC: IPMI User Enabled
        ]

        # unittest.TestCase.setUp(self)
        self.mod = mod
        self.mockdata = mockdata
        self.scci_code_map = scci_code_map
        self.userdata = userdata
        self.param_scci_map = param_scci_map
        self.url = "http://{0}/config".format(mod.params['irmc_url'])

    # ending the test
    def tearDown(self):
        self.mockdata.dispose()
        self.mockdata = None

    @patch.object(requests.Session, 'post')
    def test__irmc_scci_post__all_is_well(self, post):
        requests.Session.post.return_value = self.mockdata
        status, data, msg = irmc_scci_utils.irmc_scci_post(self.mod, "<xml><cmd/></xml>")
        self.assertEqual(self.mockdata.status_code, status)
        self.assertEqual(self.mockdata.content, data.content)
        self.assertEqual("OK", msg)

    @patch.object(requests.Session, 'post')
    def test__irmc_scci_post__bad_status_without_reason(self, post):
        self.mockdata.status_code = 100
        self.mockdata.json.return_value = {'Data': 'mockdata'}
        requests.Session.post.return_value = self.mockdata
        status, data, msg = irmc_scci_utils.irmc_scci_post(self.mod, "<xml><cmd/></xml>")
        self.assertEqual(self.mockdata.status_code, status)
        self.assertEqual(self.mockdata.content, data.content)
        self.assertEqual("POST request was not successful (" + self.url + ").", msg)

    @patch.object(requests.Session, 'post')
    def test__irmc_scci_post__bad_status_with_reason(self, post):
        self.mockdata.status_code = 100
        self.mockdata.json.return_value = {'Data': 'mockdata', 'error': {'message': self.mockdata.reason}}
        requests.Session.post.return_value = self.mockdata
        status, data, msg = irmc_scci_utils.irmc_scci_post(self.mod, "<xml><cmd/></xml>")
        self.assertEqual(self.mockdata.status_code, status)
        self.assertEqual(self.mockdata.content, data.content)
        self.assertEqual("POST request was not successful (" + self.url + "): " + str(self.mockdata.reason), msg)

    @patch.object(requests.Session, 'post')
    def test__irmc_scci_post__bad_body(self, post):
        requests.Session.post.return_value = self.mockdata
        requests.Session.post.content = "<xml><cmd></xml>"
        status, data, msg = irmc_scci_utils.irmc_scci_post(self.mod, "<xml><cmd></xml>")
        self.assertEqual(98, status)
        self.assertIn("Traceback", str(data))
        self.assertIn("POST request got invalid XML body", msg)

    @patch.object(requests.Session, 'post')
    def test__irmc_scci_post__exception(self, post):
        requests.Session.post.side_effect = Timeout()
        status, data, msg = irmc_scci_utils.irmc_scci_post(self.mod, "<xml><cmd/></xml>")
        self.assertEqual(99, status)
        self.assertIn("Traceback", str(data))
        self.assertIn("POST request encountered exception (" + self.url + ")", msg)

    def test__setup_sccirequest__all_is_well_get(self):
        self.mod.params['command'] = "get_cs"
        self.mod.params['data'] = ""
        self.mod.params['opcodeext'] = 512
        expectedxml = irmc_scci_utils.scci_body_start
        expectedxml += """<CMD Context="SCCI" OC="{0}" OE="{1}" OI="{2}" CA="{3}" Type="GET">""" \
                       """<STATUS>0</STATUS>""" \
                       """</CMD>""".format("E001", format(self.mod.params['opcodeext'], 'x'),
                                           format(self.mod.params['index'], 'x'), self.mod.params['cabid'])
        expectedxml += irmc_scci_utils.scci_body_end
        expectedxml = expectedxml.replace(irmc_scci_utils.scci_body_start, '<CMDSEQ>\n')
        body = irmc_scci_utils.setup_sccirequest(self.mod, self.scci_code_map)
        body = body.replace(irmc_scci_utils.scci_body_start, '<CMDSEQ>\n')
        expect = etree.tostring(objectify.fromstring(expectedxml))
        result = etree.tostring(objectify.fromstring(body))
        self.assertEqual(expect, result)

    def test__setup_sccirequest__all_is_well_set_string(self):
        self.mod.params['command'] = "set_cs"
        self.mod.params['data'] = "In a galaxy far, far away ..."
        self.mod.params['opcodeext'] = 512
        expectedxml = irmc_scci_utils.scci_body_start
        expectedxml += """<CMD Context="SCCI" OC="{0}" OE="{1}" OI="{2}" CA="{3}" Type="SET">""" \
                       """<DATA Type="xsd::string">{4}</DATA><STATUS>0</STATUS>""" \
                       """</CMD>""".format("E002", format(self.mod.params['opcodeext'], 'x'),
                                           format(self.mod.params['index'], 'x'), self.mod.params['cabid'],
                                           self.mod.params['data'])
        expectedxml += irmc_scci_utils.scci_body_end
        expectedxml = expectedxml.replace(irmc_scci_utils.scci_body_start, '<CMDSEQ>\n')
        body = irmc_scci_utils.setup_sccirequest(self.mod, self.scci_code_map)
        body = body.replace(irmc_scci_utils.scci_body_start, '<CMDSEQ>\n')
        expect = etree.tostring(objectify.fromstring(expectedxml))
        result = etree.tostring(objectify.fromstring(body))
        self.assertEqual(expect, result)

    def test__setup_sccirequest__all_is_well_set_int(self):
        self.mod.params['command'] = "set_cs"
        self.mod.params['data'] = "999"     # param data is always a string
        self.mod.params['opcodeext'] = 512
        expectedxml = irmc_scci_utils.scci_body_start
        expectedxml += """<CMD Context="SCCI" OC="{0}" OE="{1}" OI="{2}" CA="{3}" Type="SET">""" \
                       """<DATA Type="xsd::integer">{4}</DATA><STATUS>0</STATUS>""" \
                       """</CMD>""".format("E002", format(self.mod.params['opcodeext'], 'x'),
                                           format(self.mod.params['index'], 'x'), self.mod.params['cabid'],
                                           self.mod.params['data'])
        expectedxml += irmc_scci_utils.scci_body_end
        expectedxml = expectedxml.replace(irmc_scci_utils.scci_body_start, '<CMDSEQ>\n')
        body = irmc_scci_utils.setup_sccirequest(self.mod, self.scci_code_map)
        body = body.replace(irmc_scci_utils.scci_body_start, '<CMDSEQ>\n')
        expect = etree.tostring(objectify.fromstring(expectedxml))
        result = etree.tostring(objectify.fromstring(body))
        self.assertEqual(expect, result)

    def test__get_scciresult__all_is_well_data_string_1455(self):
        datastr = "TestData"
        status = 0
        sccireturndata = irmc_scci_utils.scci_body_start
        sccireturndata += """<CMD Context="SCCI" OC="ConfigSpace" OE="1455" OI="0" Type="GET">""" \
                          """<DATA Type="xsd::string">{0}</DATA><STATUS>{1}</STATUS>""" \
                          """</CMD>""".format(datastr, status)
        sccireturndata += irmc_scci_utils.scci_body_end
        sccidata, scciresult, sccicontext = irmc_scci_utils.get_scciresult(sccireturndata, 0x1455)
        self.assertEqual(status, scciresult)
        self.assertEqual("", sccicontext)
        self.assertEqual(datastr, sccidata)

    def test__get_scciresult__all_is_well_data_integer_1457(self):
        dataint = "999"     # param data is always a string
        status = 0
        sccireturndata = irmc_scci_utils.scci_body_start
        sccireturndata += """<CMD Context="SCCI" OC="ConfigSpace" OE="1457" OI="0" Type="GET">""" \
                          """<DATA Type="xsd::integer">{0}</DATA><STATUS>{1}</STATUS>""" \
                          """</CMD>""".format(dataint, status)
        sccireturndata += irmc_scci_utils.scci_body_end
        sccidata, scciresult, sccicontext = irmc_scci_utils.get_scciresult(sccireturndata, 0x1457)
        self.assertEqual(status, scciresult)
        self.assertEqual("", sccicontext)
        self.assertEqual(dataint, sccidata)

    def test__get_scciresult__all_is_well_overall(self):
        status = 0
        sccireturndata = """<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>""" \
                         """<Status>""" \
                         """<Value>{0}</Value>""" \
                         """<Severity>Information</Severity>""" \
                         """<Message>No Error</Message>""" \
                         """</Status>""".format(status)
        sccidata, scciresult, sccicontext = irmc_scci_utils.get_scciresult(sccireturndata, 0)
        self.assertEqual(status, scciresult)
        self.assertEqual("", sccicontext)
        self.assertEqual("", sccidata)

    def test__get_scciresult__bad_xml(self):
        sccireturndata = """<?xml version="1.0" encoding="UTF-8" standalone="yes" ?><CMDSEQ><CMD></CMDSEQ>"""
        sccidata, scciresult, sccicontext = irmc_scci_utils.get_scciresult(sccireturndata, 0)
        self.assertEqual(95, scciresult)
        self.assertIn("SCCI result was not correct XML", str(sccidata))
        self.assertIn("Traceback", str(sccicontext))

    def test__get_scciresult__bad_scci_status(self):
        datastr = "TestData"
        opcode = 0x1455
        status = 1
        sccireturndata = """<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>""" \
                         """<Status>""" \
                         """<Value>{0}</Value>""" \
                         """<Severity>Error</Severity>""" \
                         """<Message>Error {0} (Import of settings in WinSCU XML format failed) occurred</Message>""" \
                         """<Error Context="SCCI" OC="ConfigSpace" OE="{1}" OI="3">{2}</Error>""" \
                         """</Status>""".format(status, format(opcode, 'X'), datastr)
        sccidata, scciresult, sccicontext = irmc_scci_utils.get_scciresult(sccireturndata, opcode)
        self.assertEqual(status, scciresult)
        self.assertEqual("OpCodeExt 0x{0}: {1} ({2})".format(format(opcode, 'X'), datastr, status), sccicontext)
        self.assertEqual(datastr, sccidata)

    def test__get_scciresult__bad_overall_status(self):
        datastr = ""
        opcode = 0x1455
        status = 31
        sccireturndata = """<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>""" \
                         """<Status>""" \
                         """<Value>{0}</Value>""" \
                         """<Severity>Error</Severity>""" \
                         """<Message>Error {0}</Message>""" \
                         """</Status>""".format(status)
        sccidata, scciresult, sccicontext = irmc_scci_utils.get_scciresult(sccireturndata, opcode)
        self.assertEqual(status, scciresult)
        self.assertEqual("Error {0}".format(status), sccicontext)
        self.assertEqual(datastr, sccidata)

    def test__get_scciresultlist__all_is_well_results_1455_1457(self):
        datastr = "TestData"
        dataint = "999"     # param data is always a string
        opcode1 = 0x1455
        opcode2 = 0x1457
        status = 0
        sccireturndata = irmc_scci_utils.scci_body_start
        sccireturndata += """<CMD Context="SCCI" OC="ConfigSpace" OE="{3}" OI="0" Type="GET">""" \
                          """<DATA Type="xsd::string">{0}</DATA><STATUS>{2}</STATUS></CMD>""" \
                          """<CMD Context="SCCI" OC="ConfigSpace" OE="{4}" OI="0" Type="GET">""" \
                          """<DATA Type="xsd::integer">{1}</DATA><STATUS>{2}</STATUS></CMD>""". \
                          format(datastr, dataint, status, format(opcode1, 'X'), format(opcode2, 'X'))
        sccireturndata += irmc_scci_utils.scci_body_end
        sccidata, scciresult, sccicontext = \
            irmc_scci_utils.get_scciresultlist(sccireturndata, self.userdata, self.param_scci_map)
        self.assertEqual(status, scciresult)
        self.assertEqual("", sccicontext)
        self.assertEqual(datastr, sccidata['description'])
        self.assertEqual(dataint, sccidata['enabled'])

    def test__get_scciresultlist__bad_scci_status_1455_1457(self):
        datastr = "String setting failed."
        dataint = "Integer setting failed."
        opcode1 = 0x1455
        opcode2 = 0x1457
        status = 1
        sccireturndata = """<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>""" \
                         """<Status>""" \
                         """<Value>{0}</Value>""" \
                         """<Severity>Error</Severity>""" \
                         """<Message>Error {0} (Import of settings in WinSCU XML format failed) occurred</Message>""" \
                         """<Error Context="SCCI" OC="ConfigSpace" OE="{3}" OI="3">{1}</Error>""" \
                         """<Error Context="SCCI" OC="ConfigSpace" OE="{4}" OI="3">{2}</Error>""" \
                         """</Status>""".format(status, datastr, dataint, format(opcode1, 'X'), format(opcode2, 'X'))
        sccidata, scciresult, sccicontext = \
            irmc_scci_utils.get_scciresultlist(sccireturndata, self.userdata, self.param_scci_map)
        self.assertEqual(status * 2, scciresult)
        self.assertIn("OpCodeExt 0x{0}: {1} ({2})\n".format(format(opcode1, 'X'), datastr, status) + \
                      "OpCodeExt 0x{0}: {1} ({2})".format(format(opcode2, 'X'), dataint, status), sccicontext)
        self.assertEqual(datastr, sccidata['description'])
        self.assertEqual(dataint, sccidata['enabled'])

    def test__get_scciresultlist__bad_overall_status(self):
        status = 0
        sccireturndata = """<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>""" \
                         """<Status>""" \
                         """<Value>{0}</Value>""" \
                         """<Severity>Error</Severity>""" \
                         """<Message>Error {0}</Message>""" \
                         """</Status>""".format(status)
        sccidata, scciresult, sccicontext = \
            irmc_scci_utils.get_scciresultlist(sccireturndata, self.userdata, self.param_scci_map)
        self.assertEqual(status, scciresult)
        self.assertEqual("", sccicontext)
        self.assertEqual("", sccidata['description'])
        self.assertEqual("", sccidata['enabled'])

    def test__add_scci_command__all_is_well_get(self):
        scci_type = "GET"
        scci_text = "ConfBMCAcctUserEnable"
        opcode = 0x1457
        data = "TestData"
        expectedxml = """<CMD Context="SCCI" OC="{0}" OE="{1}" OI="{2}" CA="{3}" Type="GET">""" \
                      """<STATUS>0</STATUS></CMD>""".format("E001", format(opcode, 'X'), 0, -1)
        body = irmc_scci_utils.add_scci_command(scci_type, self.param_scci_map, scci_text, 0, data)
        expect = etree.tostring(objectify.fromstring(expectedxml))
        result = etree.tostring(objectify.fromstring(body))
        self.assertEqual(expect, result)

    def test__add_scci_command__all_is_well_set_string(self):
        scci_type = "SET"
        scci_text = "ConfBMCAcctUserDescription"
        opcode = 0x1455
        data = "TestData"
        expectedxml = """<CMD Context="SCCI" OC="{0}" OE="{1}" OI="{2}" CA="{3}" Type="{4}">""" \
                      """<DATA Type="xsd::{5}">{6}</DATA><STATUS>0</STATUS></CMD>""". \
                      format("E002", format(opcode, 'X'), 0, -1, scci_type, "string", data)
        body = irmc_scci_utils.add_scci_command(scci_type, self.param_scci_map, scci_text, 0, data)
        expect = etree.tostring(objectify.fromstring(expectedxml))
        result = etree.tostring(objectify.fromstring(body))
        self.assertEqual(expect, result)

    def test__add_scci_command__all_is_well_set_integer(self):
        scci_type = "SET"
        scci_text = "ConfBMCAcctUserEnable"
        opcode = 0x1457
        data = "12345"              # integer really is a string of numbers
        expectedxml = """<CMD Context="SCCI" OC="{0}" OE="{1}" OI="{2}" CA="{3}" Type="{4}">""" \
                      """<DATA Type="xsd::{5}">{6}</DATA><STATUS>0</STATUS></CMD>""". \
                      format("E002", format(opcode, 'X'), 0, -1, scci_type, "integer", data)
        body = irmc_scci_utils.add_scci_command(scci_type, self.param_scci_map, scci_text, 0, data)
        expect = etree.tostring(objectify.fromstring(expectedxml))
        result = etree.tostring(objectify.fromstring(body))
        self.assertEqual(expect, result)

    def test__add_scci_command__all_is_well_create_integer(self):
        scci_type = "CREATE"
        scci_text = "ConfBMCAcctUserEnable"
        opcode = 0x1457
        data = "12345"              # integer really is a string of numbers
        expectedxml = """<CMD Context="SCCI" OC="{0}" OE="{1}" OI="{2}" CA="{3}" Type="{4}">""" \
                      """<DATA Type="xsd::{5}">{6}</DATA><STATUS>0</STATUS></CMD>""". \
                      format("E002", format(opcode, 'X'), 0, -1, "SET", "integer", data)
        body = irmc_scci_utils.add_scci_command(scci_type, self.param_scci_map, scci_text, 0, data)
        expect = etree.tostring(objectify.fromstring(expectedxml))
        result = etree.tostring(objectify.fromstring(body))
        self.assertEqual(expect, result)

    def test__add_scci_command__all_is_well_delete_integer(self):
        scci_type = "CREATE"
        scci_text = "ConfBMCAcctUserEnable"
        opcode = 0x1457
        data = "12345"              # integer really is a string of numbers
        expectedxml = """<CMD Context="SCCI" OC="{0}" OE="{1}" OI="{2}" CA="{3}" Type="{4}">""" \
                      """<DATA Type="xsd::{5}">{6}</DATA><STATUS>0</STATUS></CMD>""". \
                      format("E002", format(opcode, 'X'), 0, -1, "SET", "integer", data)
        body = irmc_scci_utils.add_scci_command(scci_type, self.param_scci_map, scci_text, 0, data)
        expect = etree.tostring(objectify.fromstring(expectedxml))
        result = etree.tostring(objectify.fromstring(body))
        self.assertEqual(expect, result)

    def test__add_scci_command__all_is_well_set_empty(self):
        scci_type = "SET"
        scci_text = "ConfBMCAcctUserEnable"
        data = None
        expectedxml = ""
        body = irmc_scci_utils.add_scci_command(scci_type, self.param_scci_map, scci_text, 0, data)
        self.assertEqual(expectedxml, body)

    def test__add_scci_command__all_is_well_create_empty(self):
        scci_type = "CREATE"
        scci_text = "ConfBMCAcctUserEnable"
        data = None
        expectedxml = ""
        body = irmc_scci_utils.add_scci_command(scci_type, self.param_scci_map, scci_text, 0, data)
        self.assertEqual(expectedxml, body)

    def test__add_scci_command__bad_opcode(self):
        scci_type = "CREATE"
        scci_text = "NoScciCommand"
        data = ""
        expectedxml = ""
        body = irmc_scci_utils.add_scci_command(scci_type, self.param_scci_map, scci_text, 0, data)
        self.assertEqual(expectedxml, body)

    def test__add_scci_command__bad_opcode_type(self):
        scci_type = "UNKNOWN"
        scci_text = "ConfBMCAcctUserEnable"
        data = ""
        expectedxml = ""
        body = irmc_scci_utils.add_scci_command(scci_type, self.param_scci_map, scci_text, 0, data)
        self.assertEqual(expectedxml, body)

    def test__get_key_for_value__all_is_well(self):
        mydict = {"0": "zero", "1": "one", "2": "two"}
        myvalue = "two"
        mykey = irmc_scci_utils.get_key_for_value(myvalue, mydict)
        self.assertEqual("2", mykey)

    def test__get_key_for_value__no_value(self):
        mydict = {"0": "zero", "1": "one", "2": "two"}
        myvalue = None
        mykey = irmc_scci_utils.get_key_for_value(myvalue, mydict)
        self.assertEqual("", mykey)

    def test__get_key_for_value__bad_value(self):
        mydict = {"0": "zero", "1": "one", "2": "two"}
        myvalue = "three"
        mykey = irmc_scci_utils.get_key_for_value(myvalue, mydict)
        self.assertIn("no key for value", mykey)

    def test__get_key_for_value__bad_dict(self):
        mydict = ("zero", "one", "two")
        myvalue = "two"
        mykey = irmc_scci_utils.get_key_for_value(myvalue, mydict)
        self.assertIn("", mykey)

    def test__get_key_for_value__no_dict(self):
        mydict = None
        myvalue = "three"
        mykey = irmc_scci_utils.get_key_for_value(myvalue, mydict)
        self.assertIn("", mykey)


if __name__ == '__main__':
    unittest.main()
