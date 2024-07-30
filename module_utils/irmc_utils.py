# Copyright 2018-2024 Fsas Technologies INC.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division)
__metaclass__ = type

from builtins import range


def compare_irmc_profile(profile1, profile2, key="", mykey="", complist=None):
    result = True
    if key != "":
        if mykey != "":
            mykey = "{0}.{1}".format(mykey, key)
        else:
            mykey = key
    if complist is None:
        complist = []

    if type(profile1) != type(profile2):
        complist.append("'{0}': type '{1}' != type '{2}'".format(mykey, type(profile1), type(profile2)))
        result = False
    elif is_final_type(profile1) or is_final_type(profile2):
        if profile1 != profile2:
            complist.append("'{0}': '{1}' != '{2}'".format(mykey, profile1, profile2))
            result = False
    elif isinstance(profile1, list) and isinstance(profile2, list):
        new_result, complist = compare_irmc_profile_list(profile1, profile2, mykey, complist)
        result &= new_result
    else:
        new_result, complist = compare_irmc_profile_dict(profile1, profile2, mykey, complist)
        result &= new_result
    return result, complist


def compare_irmc_profile_dict(dict1, dict2, mykey="", complist=None):
    result = True
    if complist is None:
        complist = []

    if type(dict1) != type(dict2):
        complist.append("'{0}': type '{1}' != type '{2}'".format(mykey, type(dict1), type(dict2)))
        return False, complist

    if len(dict1) != len(dict2):
        complist.append("'{0}': dict len '{1}' != dict len '{2}'".format(mykey, len(dict1), len(dict2)))
        result = False

    odiff = set(dict1.keys()) - set(dict2.keys())
    ndiff = set(dict2.keys()) - set(dict1.keys())
    if odiff != ndiff:
        complist.append("'{0}': missing keys '{1}', found keys '{2}'".format(mykey, " ".join(str(x) for x in odiff),
                                                                             " ".join(str(x) for x in ndiff)))
        result = False
    for dko, dvo in sorted(dict1.items()):
        for dkn, dvn in sorted(dict2.items()):
            if dko == dkn:
                new_result, complist = compare_irmc_profile(dvo, dvn, dko, mykey, complist)
                result &= new_result
    return result, complist


def compare_irmc_profile_list(list1, list2, mykey="", complist=None):
    result = True
    if complist is None:
        complist = []

    if type(list1) != type(list2):
        complist.append("'{0}': type '{1}' != type '{2}'".format(mykey, type(list1), type(list2)))
        return False, complist

    longlist = list1
    shortlist = list2
    if len(list1) != len(list2):
        longside = "original"
        complist.append("'{0}': list len '{1}' != list len '{2}'".format(mykey, len(list1), len(list2)))
        if len(list1) < len(list2):
            longside = "compared"
            longlist = list2
            shortlist = list1
        result = False
    # longlist.sort()
    # shortlist.sort()
    for index in range(0, len(shortlist)):
        new_result, complist = compare_irmc_profile(shortlist[index], longlist[index], "",
                                                    "{0}[{1}]".format(mykey, index), complist)
        result &= new_result
    for index in range(len(shortlist) - 1, len(longlist) - 1):
        complist.append("'{0}[{1}]': only on '{2}' side".format(mykey, index, longside))
        result = False
    return result, complist


def is_final_type(this_var):
    try:               # check whether python knows about 'basestring'
        basestring
    except NameError:  # no, so it is python3, use 'str' instead
        basestring = str

    retval = False
    try:               # check whether python knows about 'unicode'
        if isinstance(this_var, unicode):
            retval = True
    except NameError:  # no, so it is python3
        retval = False
    if isinstance(this_var, (basestring, bool, int)) or this_var is None:
        retval = True
    return retval
