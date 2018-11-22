#!/usr/bin/python

# FUJITSU LIMITED
# Copyright 2018 FUJITSU LIMITED
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division)
__metaclass__ = type

from builtins import str

import mock

from ansible.compat.tests import unittest
from ansible.compat.tests.mock import create_autospec
from ansible.module_utils.basic import AnsibleModule

from module_utils import irmc_utils


class TestIrmcUtils(unittest.TestCase):

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
        mockdata.reason = "mockdata error reason"
        mockdata.content = "<xml><cmd/></xml>"
        mockdata.status_code = 200

        # unittest.TestCase.setUp(self)
        self.mod = mod
        self.mockdata = mockdata
        self.url = "http://{0}/config".format(mod.params['irmc_url'])

    # ending the test
    def tearDown(self):
        self.mockdata.dispose()
        self.mockdata = None

    def test__compare_irmc_profile__same_type_identical(self):
        myprofile1 = {"one": 1, "two": 2, "three": [{"four": 4, "seven": 7}, {"five": 5}, {"six": 6}]}
        myprofile2 = myprofile1
        myclist = []
        cval, clist = irmc_utils.compare_irmc_profile(myprofile1, myprofile2, "", myclist)
        self.assertEqual(True, cval)
        self.assertEqual(myclist, clist)

    def test__compare_irmc_profile__same_type_dict_key_different(self):
        myprofile1 = {"one": 1, "two": 2, "three": [{"four": 4, "seven": 7}, {"five": 5}, {"six": 6}]}
        myprofile2 = {"eins": 1, "two": 2, "three": [{"four": 4, "seven": 7}, {"five": 5}, {"six": 6}]}
        myclist = []
        cval, clist = irmc_utils.compare_irmc_profile(myprofile1, myprofile2, "", myclist)
        self.assertEqual(False, cval)
        self.assertIn("missing keys 'one', found keys 'eins'", " ".join(str(x) for x in clist))

    def test__compare_irmc_profile__same_type_dict_value_different(self):
        myprofile1 = {"one": 1, "two": 2, "three": [{"four": 4, "seven": 7}, {"five": 5}, {"six": 6}]}
        myprofile2 = {"one": 10, "two": 2, "three": [{"four": 4, "seven": 7}, {"five": 5}, {"six": 6}]}
        myclist = []
        cval, clist = irmc_utils.compare_irmc_profile(myprofile1, myprofile2, "", myclist)
        self.assertEqual(False, cval)
        self.assertIn("'1' != '10'", " ".join(str(x) for x in clist))

    def test__compare_irmc_profile_list__same_type_list_value_different(self):
        myprofile1 = {"one": 1, "two": 2, "three": [{"four": 4, "seven": 7}, {"five": 5}, {"six": 6}]}
        myprofile2 = {"one": 1, "two": 2, "three": [{"four": 4, "seven": 7}, {"eight": 8}, {"six": 6}]}
        myclist = []
        cval, clist = irmc_utils.compare_irmc_profile(myprofile1, myprofile2, "", myclist)
        self.assertEqual(False, cval)
        self.assertIn("missing keys 'eight', found keys 'five'", " ".join(str(x) for x in clist))

    def test__compare_irmc_profile__same_type_dict_length_different(self):
        myprofile1 = {"one": 1, "two": 2, "three": [{"four": 4, "seven": 7}, {"five": 5}, {"six": 6}]}
        myprofile2 = {"one": 1, "three": [{"four": 4, "seven": 7}, {"five": 5}, {"six": 6}]}
        myclist = []
        cval, clist = irmc_utils.compare_irmc_profile(myprofile1, myprofile2, "", myclist)
        self.assertEqual(False, cval)
        self.assertIn("dict len '3' != dict len '2' ", " ".join(str(x) for x in clist))

    def test__compare_irmc_profile__same_type_list_length_different(self):
        myprofile1 = {"one": 1, "two": 2, "three": [{"four": 4, "seven": 7}, {"five": 5}, {"six": 6}]}
        myprofile2 = {"one": 1, "two": 2, "three": [{"four": 4, "seven": 7}, {"six": 6}]}
        myclist = []
        cval, clist = irmc_utils.compare_irmc_profile(myprofile1, myprofile2, "", myclist)
        self.assertEqual(False, cval)
        self.assertIn("list len '3' != list len '2' ", " ".join(str(x) for x in clist))

    def test__compare_irmc_profile__list_type_different(self):
        myprofile1 = {"one": 1, "two": 2, "three": [{"four": 4, "seven": 7}, {"five": 5}, {"six": 6}]}
        myprofile2 = {"one": 1, "two": 2, "three": {"four": 4, "seven": 7}}
        myclist = []
        cval, clist = irmc_utils.compare_irmc_profile(myprofile1, myprofile2, "", myclist)
        result = " ".join(str(x) for x in clist).replace("class", "type")
        self.assertEqual(False, cval)
        self.assertIn("type '<type 'list'>' != type '<type 'dict'>'", result)

    def test__compare_irmc_profile__dict_type_different(self):
        myprofile1 = {"one": 1, "two": 2, "three": [{"four": 4, "seven": 7}, {"five": 5}, {"six": 6}]}
        myprofile2 = [{"one": 1, "two": 2, "three": [{"four": 4}, {"seven": 7}, {"five": 5}, {"six": 6}]}]
        myclist = []
        cval, clist = irmc_utils.compare_irmc_profile(myprofile1, myprofile2, "", myclist)
        result = " ".join(str(x) for x in clist).replace("class", "type")
        self.assertEqual(False, cval)
        self.assertIn("type '<type 'dict'>' != type '<type 'list'>'", result)

    def test__compare_irmc_profile_dict__same_type_identical(self):
        mydict1 = {"one": 1, "two": 2, "three": 3}
        mydict2 = mydict1
        myclist = []
        cval, clist = irmc_utils.compare_irmc_profile_dict(mydict1, mydict2, "", myclist)
        self.assertEqual(True, cval)
        self.assertEqual(myclist, clist)

    def test__compare_irmc_profile_dict__same_type_key_different(self):
        mydict1 = {"one": 1, "two": 2, "three": 3}
        mydict2 = {"four": 1, "two": 2, "three": 3}
        myclist = []
        cval, clist = irmc_utils.compare_irmc_profile_dict(mydict1, mydict2, "", myclist)
        self.assertEqual(False, cval)
        self.assertIn("missing keys 'one', found keys 'four'", " ".join(str(x) for x in clist))

    def test__compare_irmc_profile_dict__same_type_value_different(self):
        mydict1 = {"one": 1, "two": 2, "three": 3}
        mydict2 = {"one": 4, "two": 2, "three": 3}
        myclist = []
        cval, clist = irmc_utils.compare_irmc_profile_dict(mydict1, mydict2, "", myclist)
        self.assertEqual(False, cval)
        self.assertIn("'1' != '4'", " ".join(str(x) for x in clist))

    def test__compare_irmc_profile_dict__same_type_length_different(self):
        mydict1 = {"one": 1, "two": 2, "three": 3}
        mydict2 = {"one": 1, "two": 2, "three": 3, "four": 4}
        myclist = []
        cval, clist = irmc_utils.compare_irmc_profile_dict(mydict1, mydict2, "", myclist)
        self.assertEqual(False, cval)
        self.assertIn("dict len '3' != dict len '4' ", " ".join(str(x) for x in clist))

    def test__compare_irmc_profile_dict__type_different(self):
        mydict1 = {"one": 1, "two": 2, "three": 3}
        mydict2 = ["one", "two", "three"]
        myclist = []
        cval, clist = irmc_utils.compare_irmc_profile_dict(mydict1, mydict2, "", myclist)
        result = " ".join(str(x) for x in clist).replace("class", "type")
        self.assertEqual(False, cval)
        self.assertIn("type '<type 'dict'>' != type '<type 'list'>'", result)

    def test__compare_irmc_profile_list__same_type_identical(self):
        mylist1 = ["one", "two", "three"]
        mylist2 = mylist1
        myclist = []
        cval, clist = irmc_utils.compare_irmc_profile_list(mylist1, mylist2, "", myclist)
        self.assertEqual(True, cval)
        self.assertEqual(myclist, clist)

    def test__compare_irmc_profile_list__same_type_value_different(self):
        mylist1 = ["one", "two", "three"]
        mylist2 = ["four", "two", "three"]
        myclist = []
        cval, clist = irmc_utils.compare_irmc_profile_list(mylist1, mylist2, "", myclist)
        self.assertEqual(False, cval)
        self.assertIn("'four' != 'one'", " ".join(str(x) for x in clist))

    def test__compare_irmc_profile_list__same_type_length_different(self):
        mylist1 = ["one", "two", "three"]
        mylist2 = ["one", "two", "three", "four"]
        myclist = []
        cval, clist = irmc_utils.compare_irmc_profile_list(mylist1, mylist2, "", myclist)
        self.assertEqual(False, cval)
        self.assertIn("list len '3' != list len '4' ", " ".join(str(x) for x in clist))

    def test__compare_irmc_profile_list__type_different(self):
        mylist1 = ["one", "two", "three"]
        mylist2 = {"one": 1, "two": 2, "three": 3}
        myclist = []
        cval, clist = irmc_utils.compare_irmc_profile_list(mylist1, mylist2, "", myclist)
        result = " ".join(str(x) for x in clist).replace("class", "type")
        self.assertEqual(False, cval)
        self.assertIn("type '<type 'list'>' != type '<type 'dict'>'", result)

    def test__is_final_type__list(self):
        mylist = ["one", "two", "three"]
        myval = irmc_utils.is_final_type(mylist)
        self.assertEqual(False, myval)

    def test__is_final_type__dict(self):
        mydict = {"one": 1, "two": 2, "three": 3}
        myval = irmc_utils.is_final_type(mydict)
        self.assertEqual(False, myval)

    def test__is_final_type__string(self):
        mystring = "one, two, three"
        myval = irmc_utils.is_final_type(mystring)
        self.assertEqual(True, myval)

    def test__is_final_type__int(self):
        myint = 123
        myval = irmc_utils.is_final_type(myint)
        self.assertEqual(True, myval)

    def test__is_final_type__bool(self):
        mybool = False
        myval = irmc_utils.is_final_type(mybool)
        self.assertEqual(True, myval)


if __name__ == '__main__':
    unittest.main()
