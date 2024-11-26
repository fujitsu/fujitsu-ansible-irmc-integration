irmc_set_ntp
============

Time synchronizetion for iRMC.

Requirements
------------

None

Role Variables
--------------

| Name | Required | Default Value | Choices | Type | Description |
|------|----------|---------------|---------|------|-------------|
| `ntp_server_primary` | false | | | str | IP address (IPv4 or IPv6) or DNS name of primary NTP server to be set. |
| `ntp_server_secondary` | false | | | str | IP address (IPv4 or IPv6) or DNS name of secondary NTP server to be set. |
| `rtc_mode` | false | | `local time`,<br>`UTC/GMT` | str | Defines how iRMC interprets the system's hardware RTC time. |
| `time_mode` | false | | `System RTC`,<br>`NTP` | str | Defines how iRMC synchronizes its real-time clock (RTC). |
| `time_zone_location` | false | | | str | iRMC time zone (e.g. "Europe/Berlin"; based on Linux "tzdata"). |

Dependencies
------------

None

Example Playbook
----------------

playbook.yml:

    ---
    - name: Set iRMC ntp
      connection: local
      hosts: iRMC_group
      gather_facts: false
      roles:
        - role: fujitsu.primergy.irmc_set_ntp
          vars:
            ntp_server_primary: 192.0.2.1
            ntp_server_secondary: 192.0.2.2
            time_mode: "System RTC"
            time_zone_location: "Asia/Tokyo"
            rtc_mode: "local time"

License
-------

GPL-3.0-or-later

Author Information
------------------

- Jiajun Guo <guo.jiajun@fujitsu.com>
