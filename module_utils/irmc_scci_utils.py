#!/usr/bin/python

# FUJITSU LIMITED
# Copyright 2018 FUJITSU LIMITED
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division)
__metaclass__ = type

from builtins import str

import traceback
from xml.etree import cElementTree as ElementTree
import requests
from requests.auth import HTTPBasicAuth
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


scci_body_start = """<?xml version="1.0" encoding="UTF-8" standalone="yes" ?><CMDSEQ>\n"""
scci_body_end = "</CMDSEQ>"


def setup_sccirequest(module, scci_map):
    if module.params['command'] == "get_cs":
        getset = "GET"
        data = ""
    elif module.params['command'] == "set_cs":
        getset = "SET"
        dtype = "integer" if module.params['data'].isdigit() else "string"
        data = """<DATA Type="xsd::{0}">{1}</DATA>\n""".format(dtype, module.params['data'])
    else:
        getset = "SET"
        data = ""
    body = scci_body_start
    body += """<CMD Context="SCCI" OC="{0}" OE="{1}" OI="{2}" CA="{3}" Type="{4}">{5}<STATUS>0</STATUS></CMD>\n""". \
            format(scci_map.get(module.params['command']), format(module.params['opcodeext'], 'x'),
                   format(module.params['index'], 'x'), module.params['cabid'], getset, data)
    body += scci_body_end
    return body


def setup_commandlist(cmdlist, ctype, scci_map):
    body = scci_body_start
    data = ""
    for elem in scci_map:
        if elem[0] not in cmdlist:
            continue
        if elem[4] is not None and cmdlist[elem[0]] is not None:
            data = get_key_for_value(cmdlist[elem[0]], elem[4])
        else:
            data = cmdlist[elem[0]]
        body += add_scci_command(ctype, scci_map, elem[1], elem[3], data)
    body += scci_body_end
    return body


def add_scci_command(ctype, scci_map, opcodeextcode, index, data):
    if ctype not in ("SET", "GET", "CREATE", "DELETE"):
        return ""
    if ctype in ("CREATE", "DELETE"):
        ctype = "SET"
    if ctype == "SET" and data is None:
        return ""

    scci_code = get_sccicode(opcodeextcode, scci_map)
    if scci_code == 0:
        return ""

    if ctype == "SET":
        opcode = "E002"
        if isinstance(data, bool):
            data = "0" if data is False else "1"
        if isinstance(data, int):
            data = str(data)
        dtype = "integer" if data.isdigit() else "string"
        sensitives = ("&", "<", ">", '"', "'")
        for char in sensitives:
            if char in data:
                data = "<![CDATA[{0}]]>".format(data)
                break
        data = """<DATA Type="xsd::{0}">{1}</DATA>\n""".format(dtype, data)
    else:
        ctype = "GET"
        opcode = "E001"
        data = ""
    body = """<CMD Context="SCCI" OC="{0}" OE="{1}" OI="{2}" CA="{3}" Type="{4}">{5}<STATUS>0</STATUS></CMD>\n""". \
           format(opcode, format(scci_code, 'X'), format(index, 'X'), -1, ctype, data)
    return body


def get_scciresult(data, opcodeextcode):
    # extract XML data
    # things are complicated, as the return string is not necessarily well-formed.
    # We do some extra work here just in case
    sccidata = sccicontext = overallcontext = ""
    scciresult = overallresult = 0
    try:
        root = ElementTree.fromstring(data)
        for item in root:
            if item.tag.upper() == "CMD" or item.tag.upper() == "ERROR" or item.tag.upper() == "WARNING":
                if item.attrib['OE'] != str(format(opcodeextcode, 'X')):
                    continue
                if item.tag.upper() == "VALUE":
                    scciresult = int(item.text)
                if item.tag.upper() == "SEVERITY":
                    if item.text.upper() == "ERROR" and scciresult == 0:
                        scciresult += 1    # something went wrong, make sue we get a hint
                if item.tag.upper() == "ERROR" or item.tag.upper() == "WARNING":
                    sccicontext = item.text
                for iitem in item:
                    if iitem.tag.upper() == "DATA":
                        sccidata = iitem.text
                    if iitem.tag.upper() == "STATUS" or iitem.tag.upper() == "VALUE":
                        scciresult = int(iitem.text)
                    if iitem.tag.upper() == "ERROR" or iitem.tag.upper() == "WARNING":
                        sccicontext = iitem.text
                break
            elif item.tag.upper() == "VALUE":
                overallresult = int(item.text)
            elif item.tag.upper() == "MESSAGE":
                overallcontext = item.text
    except KeyError as e:
        # scciresult = 94
        # sccidata = "Error: no results from command list."
        # sccicontext = sccidata
        pass
    except Exception as e:
        scciresult = 95
        sccidata = "SCCI result was not correct XML: {0}".format(str(e))
        sccicontext = traceback.format_exc()

    # User SSH key is empty
    if scciresult == 1 and opcodeextcode in (0x19A1, 0x19A2, 0x19A3):
        scciresult = 0
        sccidata = sccicontext = ""

    if sccidata is None:
        sccidata = ""

    if scciresult != 0 or overallresult != 0:
        if sccidata == "":
            sccidata = sccicontext
        scciresult += overallresult
        if sccicontext == "":
            sccicontext += overallcontext
        else:
            sccicontext = "OpCodeExt 0x{0}: {1} ({2})".format(format(opcodeextcode, 'X'), sccicontext, scciresult)

    return sccidata, scciresult, sccicontext


def get_scciresultlist(resultlist, sccidata, scci_map):
    listresult = 0
    listcontext = ""
    result = [0] * len(scci_map)
    context = [""] * len(scci_map)
    index = 0
    for elem in scci_map:
        sccidata[elem[0]], result[index], context[index] = get_scciresult(resultlist, elem[2])
        if result[index] != 0 and sccidata[elem[0]] != "":
            listresult += result[index]
            listcontext += context[index] + "\n"
        index += 1

    return sccidata, listresult, listcontext[:-1]


def irmc_scci_post(module, body):
    ''' Post a SCCI command at iRMC config URI. '''
    try:
        ElementTree.fromstring(body)
    except Exception as e:
        data = traceback.format_exc()
        msg = "POST request got invalid XML body: {0}".format(body)
        return 98, data, msg

    session = requests.Session()
    retries = Retry(total=5, backoff_factor=0.1)
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))

    url = "http://{0}/config".format(module.params['irmc_url'])
    msg = "OK"
    try:
        data = session.post(url, data=body, verify=module.params['validate_certs'],
                            auth=HTTPBasicAuth(module.params['irmc_username'], module.params['irmc_password']))
        data.connection.close()

        status = data.status_code
        if status not in (200, 202, 204):
            try:
                msg = "POST request was not successful ({0}): {1}".format(url, data.json()['error']['message'])
            except Exception:
                msg = "POST request was not successful ({0}).".format(url)

        if "Login required to continue." in str(data.content):
            return 1, "Invalid login data.", "Login required to continue."
    except Exception as e:
        status = 99
        data = traceback.format_exc()
        msg = "POST request encountered exception ({0}): {1}".format(url, str(e))

    return status, data, msg


def irmc_scci_update(module, update_url):
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=0.1)
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))

    url = "http://{0}/{1}".format(module.params['irmc_url'], update_url)
    msg = "OK"
    try:
        data = session.post(url, verify=module.params['validate_certs'],
                            auth=HTTPBasicAuth(module.params['irmc_username'], module.params['irmc_password']))
        data.connection.close()

        status = data.status_code
        if status not in (200, 202, 204):
            try:
                msg = "POST request was not successful ({0}): {1}".format(url, data.json()['error']['message'])
            except Exception:
                msg = "POST request was not successful ({0}).".format(url)

        if "Login required to continue." in data.content:
            return 1, "Invalid login data.", "Login required to continue."
    except Exception as e:
        status = 99
        data = traceback.format_exc()
        msg = "POST request encountered exception ({0}): {1}".format(url, str(e))

    return status, data, msg


def get_key_for_value(value, dictionary):
    if value == "" or value is None:
        return ""
    if dictionary is None or not isinstance(dictionary, dict):
        return ""
    for dictkey, dictvalue in dictionary.items():
        value = str(value)
        if value.lower() == dictvalue.lower():
            return dictkey
    return "no key for value '{0}' in '{1}'".format(value, dictionary)


def get_sccicode(param_or_name, scci_map):
    for elem in scci_map:
        if param_or_name in (elem[0], elem[1]):
            return elem[2]
    return 0


def setup_datadict(module, emptyAllowed=True):
    spcount = 0
    datadict = dict()
    for key, value in module.params.items():
        if key not in ("irmc_url", "irmc_username", "irmc_password", "validate_certs", "command"):
            if value is not None:
                if emptyAllowed is True or value != "":
                    spcount += 1
                else:
                    value = None
            datadict[key] = value

    return datadict, spcount
