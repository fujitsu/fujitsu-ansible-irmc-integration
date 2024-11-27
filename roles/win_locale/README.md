win_locale
==========

Change the language setting (language, region, timezone) of the specified account on Windows Server.

Notes:

- For languages for which no language pack is initially installed, a language pack is downloaded.
  This requires setting up an internet connection and takes about 30 minutes to download the language pack.
- Initially installed language pack is following (differences depending on the installation media.):
  - de-DE, en-US, es-ES, fr-FR, it-IT, ja-JP, ko-KR, zh-TW

Requirements
------------

This role depends on the following Ansible collections:

- `ansible.windows` >= 1.14.0
- `community.windows` >= 1.13.0

If a language pack download occurs, internet connection settings are required.

Role Variables
--------------

| Name | Required | Default Value | Choices | Type | Description |
|------|----------|---------------|---------|------|-------------|
| `language` | true | | | str | Language. <br/> A list of culture names to use is available from <https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/available-language-packs-for-windows>. |
| `location` | true | | | str | Location. <br/> A list of GeoIDs you can use and what location it relates to is available from <https://msdn.microsoft.com/en-us/library/dd374073.aspx>. |
| `timezone` | true | | | str | Timezone. <br/> A list of possible timezones is available from `tzutil.exe /l` and from <https://msdn.microsoft.com/en-us/library/ms912391.aspx>. |
| `reuse_iso` | false | false | | bool | If true is specified, the ISO file is not deleted and the existing ISO file is reused. |

Dependencies
------------

None

Example Playbook
----------------

    ---
    - hosts: windows
      roles:
        - role: fujitsu.primergy.win_locale
          vars:
            language: "ja-JP"
            location: "122"
            timezone: "Tokyo Standard Time"

License
-------

GPL-3.0-or-later

Author Information
------------------

- Yutaka Kamioka <yutaka.kamioka@fujitsu.com>
- Tomohisa Nakai <nakai.tomohisa@fujitsu.com>
