win_locale
==========

Change the language, region and timezone of Windows Server.

Requirements
------------

This role depends on the following Ansible collections:

- `ansible.windows` >= 1.0.0
- `community.windows` >= 1.0.0

Role Variables
--------------

| Name | Required | Default Value | Choices | Type | Description |
|------|----------|---------------|---------|------|-------------|
| `download_path` | true | | | str | Download path for language pack ISO file. |
| `download_url` | true | | | str | Download link of Windows Server 2022 language pack. |
| `format` | false | | | str | Language format. This needs to be set if `location` or `unicode_language` is not set. <br> A list of culture names to use is available from https://msdn.microsoft.com/en-us/library/system.globalization.cultureinfo.aspx. |
| `language` | true | | | str | Display language. It must be specified from among the languages for which the language pack is already installed. |
| `language_pack` | true | | | str | Language pack to be installed. This string must be specified in all lowercase. <br> A list of strings to use is available from `\LanguagesAndOptionalFeatures\Microsoft-Windows-Server-Language-Pack_x64_{{ language_pack }}.cab` in the language pack ISO file. |
| `location` | false | | | str | Location. This needs to be set if `format` or `unicode_language` is not set. <br> A list of GeoIDs you can use and what location it relates to is available from https://msdn.microsoft.com/en-us/library/dd374073.aspx. |
| `timezone` | true | | | str | Timezone. <br> A list of possible timezones is available from `tzutil.exe /l` and from https://msdn.microsoft.com/en-us/library/ms912391.aspx. |
| `unicode_language` | false | | | str | Unicode language format. This needs to be set if `location` or `format` is not set. <br> A list of culture names to use is available from https://msdn.microsoft.com/en-us/library/system.globalization.cultureinfo.aspx. |

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
        download_path: "C:\\lang.iso"
        download_url: "https://go.microsoft.com/fwlink/p/?linkid=2195333"
        format: "ja-JP"
        language: "ja-JP"
        language_pack: "ja-jp"
        location: "122"
        timezone: "Tokyo Standard Time"
        unicode_language: "ja-JP"

License
-------

GPL-3.0-or-later

Author Information
------------------

- Tomohisa Nakai <nakai.tomohisa@fujitsu.com>
