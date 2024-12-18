irmc_set_certificate
===================

Set iRMC certificates.

Note:  
- Before using this role, SSL Certificate, SSL CA Certificate must be generated or obtained in advance.

Requirements
------------

None

Role Variables
--------------

| Name | Required | Default Value | Choices | Type | Description |
|------|----------|---------------|---------|------|-------------|
| `ssl_private_key_path` | true | | | str | Path to file containing SSL private key. |
| `ssl_cert_path` | true | | | str | Path to file containing SSL CA certificate. |
| `ssl_ca_cert_path` | true | | | str | Path to file containing SSL certificate. |
| `sec_until_timeout` | false | `600` | | int | Seconds before timeout of health check. <br> It is recommended that this parameter not be changed. <br> Please change it only if PRIMERGY takes a long time to reboot and health check fails.  |

Dependencies
------------

None

Example Playbook
----------------

    ---
    - name: Set iRMC certificates
      connection: local
      hosts: iRMC_group
      gather_facts: false
      roles:
        - irmc_set_certificate
      vars:
        ssl_private_key_path: /path/to/sslprivatekey/server.key
        ssl_cert_path: /path/to/sslcert/server.crt
        ssl_ca_cert_path: /path/to/sslcacert/ca.crt

License
-------

GPL-3.0-or-later

Author Information
------------------

- Tomohisa Nakai <nakai.tomohisa@fujitsu.com>
