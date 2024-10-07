win_serverview_raidmanager
==========================

Set up ServerView RAID Manager to Windows Server.

1. Create group `raid-adm` for managing ServerView RAID Manager
2. Create account `raidroot`
3. Install Adoptium OpenJDK
   - The installer log is output to `C:\Temp\OpenJDK_install.log`
4. Detect the installation path of OpenJDK and set the environment variable `SVRM_JAVA_PATH`
5. Install ServerView Agents
   - The installer log is output to `C:\Temp\ServerviewRAIDManager_install.log`

Notes:
After downloading ServerView Agents, specify the path to the installer file.
Download ServerView Agents from <https://support.ts.fujitsu.com/>.

Notes:
This roll only supports AdoptOpenJDK with HotSpot.
After downloading the OpenJDK installer, specify the path to the installer file.
Please download the MSI format JRE installer from <https://adoptium.net/temurin/releases/?os=windows&version=8&arch=x64&package=jre>.

Requirements
------------

This role depends on the following Ansible collections:

- `ansible.windows` >= 2.5.0

Role Variables
--------------

| Name | Required | Default Value | Choices | Type | Description |
|------|----------|---------------|---------|------|-------------|
| `username` | false | `raidroot` | | str | Account for login to "RAID Manager".<br/> The account name is `raidroot` by default, but can be customized as needed. |
| `password` | true | | | str | Password for the account specified in `username` |
| `installer` | true | | | str | Path to ServerView RAID Manager installer.<br/> Specify the absolute path or relative path from Playbook.|
| `openjdk_installer` | true | | | str | Path to AdoptOpenJDK installer.<br/> Specify the absolute path or relative path from Playbook.|

Dependencies
------------

None

Example Playbook
----------------

    ---
    - hosts: windows
      roles:
        - role: win_serverview_raidmanager
          vars:
            password: P@ssw0rd
            installer: "/path/to/installer/ServerView_RAID_x64.exe"
            openjdk_installer: "/path/to/installer/OpenJDK8U-jdk_x64_windows_hotspot.msi"

License
-------

GPL-3.0-or-later

Author Information
------------------

- Yutaka Kamioka <yutaka.kamioka@jp.fujitsu.com>
