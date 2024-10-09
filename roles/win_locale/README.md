win_locale
==========

Change the language, region and timezone of Windows Server.

Requirements
------------

This role depends on the following Ansible collections:

- `ansible.windows` >= 2.5.0
- `community.windows` >= 2.3.0

Role Variables
--------------

| Name | Required | Default Value | Choices | Type | Description |
|------|----------|---------------|---------|------|-------------|
| `language` | true | | | str | Language. <br> A list of culture names to use is available from https://msdn.microsoft.com/en-us/library/system.globalization.cultureinfo.aspx. |
| `location` | false | | | str | Location. <br> A list of GeoIDs you can use and what location it relates to is available from https://msdn.microsoft.com/en-us/library/dd374073.aspx. |
| `timezone` | true | | | str | Timezone. <br> A list of possible timezones is available from `tzutil.exe /l` and from https://msdn.microsoft.com/en-us/library/ms912391.aspx. |

Dependencies
------------

None

Example Playbook
----------------

    ---
    - hosts: windows
      roles:
        - role: win_locale
      vars:
        language: "ja-JP"
        location: "122"
        timezone: "Tokyo Standard Time"

License
-------

GPL-3.0-or-later

Author Information
------------------

- Tomohisa Nakai <nakai.tomohisa@fujitsu.com>
