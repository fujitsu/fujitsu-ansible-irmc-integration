#!/usr/bin/python

# FUJITSU LIMITED
# Copyright 2018 FUJITSU LIMITED
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division)
__metaclass__ = type

from builtins import str

import ntpath
import traceback
import requests
from requests.auth import HTTPBasicAuth
from requests.adapters import HTTPAdapter
import urllib3
from urllib3.util.retry import Retry
from urllib3.exceptions import InsecureRequestWarning
from requests_toolbelt import MultipartEncoder
urllib3.disable_warnings(InsecureRequestWarning)


def irmc_redfish_post_file(module, uri, filename):
    try:
        filedata = open(filename, 'rb')
    except Exception as e:
        status = 89
        fdata = traceback.format_exc()
        msg = "Could not read file at '{0}': {1}".format(filename, str(e))
        return status, fdata, msg

    filebasename = ntpath.basename(filename)
    multipart_data = MultipartEncoder(
        fields={'data': (filebasename, filedata, 'application/octet-stream', {'Content-Disposition': 'form-data'})}
    )
    headers = {
        "Accept": "application/json",
        "Content-Type": multipart_data.content_type
    }
    url = "https://{0}/{1}".format(module.params['irmc_url'], uri)

    session = requests.Session()
    retries = Retry(total=5, backoff_factor=0.1)
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))

    msg = "OK"
    try:
        data = session.post(url, headers=headers, data=multipart_data, verify=module.params['validate_certs'],
                            auth=HTTPBasicAuth(module.params['irmc_username'], module.params['irmc_password']))
        data.connection.close()

        status = data.status_code
        if status not in (200, 202, 204):
            try:
                msg = "POST request was not successful ({0}): {1}".format(url, data.json()['error']['message'])
            except Exception:
                msg = "POST request was not successful ({0}).".format(url)

    except Exception as e:
        status = 99
        data = traceback.format_exc()
        msg = "POST request encountered exception ({0}): {1}".format(url, str(e))

    return status, data, msg
