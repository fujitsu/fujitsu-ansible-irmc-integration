irmc_email_alert
================

Configure E-mail Alert settings for iRMC devices.

NOTE:  
For more information, see P.161 "E-mail Alerting" in "Fujitsu Software ServerView Suite iRMC S6 Web Interface 2.x".
Documents can be downloaded from the link below:

- English version: <https://support.ts.fujitsu.com/IndexDownload.asp?SoftwareGuid=D3410FEF-70F5-4446-B8DC-B4FAD18F48A9>
- Japanese version: <https://support.ts.fujitsu.com/IndexDownload.asp?SoftwareGuid=6B16AC97-2302-47F1-A14D-05DD26BFF27C>

Requirements
------------

None

Role Variables
--------------

| Name | Required | Default Value | Choices | Type | Description |
|------|----------|---------------|---------|------|-------------|
| `email_alert.enabled` | false | | | bool | Enable E-mail Alerting. |
| `email_alert.retries` | false | | 0 to 7 | int | Number of SMTP retries. |
| `email_alert.retry_delay` | false | | | int | Time (up to 255 in seconds) between SMTP retries. |
| `email_alert.response_timeout` | false | | 10 to 300 | int | Timeout (in seconds) for an SMTP response. |
| `smtp.primary_server.address` | false | | | str | IP address, domain name or FQDN of the mail server. |
| `smtp.primary_server.port` | false | | 1 to 65535 | int | SMTP port of the mail server. |
| `smtp.primary_server.authentication.type` | false | | 'None', 'Smtp' | str | Authentication type for connecting the iRMC to the mail server. 'Smtp' is Authentication according to RFC 2554: SMTP Service Extension for Authentication. |
| `smtp.primary_server.authentication.username` | false | | | str | User name for authentication on the mail server. |
| `smtp.primary_server.authentication.password` | false | | | str | Password for authentication on the mail server. |
| `smtp.primary_server.fqdn_with_ehlo_helo` | false | | | bool | Enables sending the FQDN with EHLO/HELO. |
| `smtp.primary_server.use_ssl_tls` | false | | | bool | Depending on the configured network port, the iRMC will either directly establish an SSL connection (SMTPS legacy port 465) or check for the presence of the STARTTLS keyword. |
| `smtp.primary_server.verify_certificate` | false | | | bool | The SSL certificate from the SMTP server is verified against the stored CA certificate in the iRMC. |
| `smtp.secondary_server.*` | | | | | Same as `smtp.primary_server`. |
| `email_format.from` | false | | | str | Sender identification of the iRMC. Active for all mail formats. |
| `email_format.subject` | false | | | str | Fixed subject for the alert mails. Only active for the Fixed Subject mail format. |
| `email_format.message` | false | | | str | Type of message (E-mail). Only active for the Fixed Subject mail format. |
| `email_format.admin_name` | false | | | str | Name of the administrator responsible (optional). Only active for the ITS mail format. |
| `email_format.admin_phone` | false | | | str | Phone number of the administrator responsible (optional). Only active for the ITS mail format. |
| `email_format.country_code` | false | | | str | Two-character country code based on ISO 3166, ISO 3166 alpha 2. |
| `email_format.customer_id` | false | | | str | Identifier for the customer. |
| `email_format.server_url` | false | | | str | A URL under which the server is accessible under certain conditions. This must be entered manually. Only active for the Standard mail format. |
| `email_format.attach_screenshot` | false | | | bool | A screenshot generated automatically by the iRMC in the case of a critical OS stop event is attached to the corresponding 'Critical O/S Stop' event E-mail. |

- The E-mail format for each user is configured in “iRMC Local User Accounts”.
  The following E-mail formats are supported:
  - Standard
  - Fixed Subject
  - ITS Format
  - SMS Format

Dependencies
------------

None

Example Playbook
----------------

playbook.yml:

    ---
    - hosts: iRMC_group
      connection: local
      gather_facts: false

      vars_files:
        - ./vars.yml

      roles:
        - role: irmc_email_alert

vars.yml:

    email_alert:
      enabled: true

    smtp:
      primary_server:
        address: "192.0.2.1"
        authentication:
          type: "Smtp"
          username: "AuthUserName"
          password: "AuthPassword"
      secondary_server:
        address: 192.0.2.2
        authentication:
          type: "None"

    email_format:
      from: "MailFrom@example.com"
      admin_name: "John Doe"
      admin_phone: "+1 555 555 0100"
      server_url: "https://www.server.example.com"
      attach_screenshot: true

inventory.ini:

    [iRMC_group]
    192.0.2.99 irmc_user=admin irmc_password=SECRET

    [iRMC_group:vars]
    validate_certificate=false  # When iRMC deivce is operated without a server certificate

License
-------

GPL-3.0-or-later

Author Information
------------------

- Yutaka Kamioka <yutaka.kamioka@jp.fujitsu.com>
