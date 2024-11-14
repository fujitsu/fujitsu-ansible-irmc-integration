win_serverview_agents
=====================

Set up ServerView Agents to Windows Server.

1. Enable SNMP services
2. Create group `FUJITSU SVUSER` for managing ServerView Agents
3. Create account `svroot`
4. Install ServerView Agents
   - The installer log is output to `C:\Temp\ServerviewAgents_install.log`

Notes:
After downloading ServerView Agents, specify the path to the installer file.
Download ServerView Agents from <https://support.ts.fujitsu.com/>.

Requirements
------------

This role depends on the following Ansible collections:

- `ansible.windows` >= 2.5.0

Role Variables
--------------

| Name | Required | Default Value | Choices | Type | Description |
|------|----------|---------------|---------|------|-------------|
| `username` | false | `svroot` | | str | Account for login to "System Monitor".<br/> The account name is `svroot` by default, but can be customized as needed. |
| `password` | true | | | str | Password for the account specified in `username` |
| `installer` | true | | | str | Path to ServerView Agents installer.<br/> Specify the absolute path or relative path from Playbook.|
| `allow_administrator_login` | false | false | | bool | Login to "System Monitor" with Administrator? |

Dependencies
------------

None

Example Playbook
----------------

    ---
    - hosts: windows
      roles:
        - role: fujitsu.primergy.win_serverview_agents
          vars:
            password: P@ssw0rd
            installer: "/path/to/installer/ServerViewAgents_Win_x64.exe"
    
License
-------

GPL-3.0-or-later

Author Information
------------------

- Yutaka Kamioka <yutaka.kamioka@jp.fujitsu.com>
