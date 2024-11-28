win_dsnap
=========

Set up DSNAP.

Note:  
DSNAP is software for collecting information of failure analisys in a batch.

Note:  
You must download ServerView Management and Serviceability DVD to use this role.

1. Access <https://support.ts.fujitsu.com/>.
2. Press "Select a new Product" button.
3. Select "Serial-ident number", enter the serial number of your PRIMERGY and press the "Continue" button.
4. Select your Windows Server OS in "Selected operating system".
5. Display "Applications tab > Server Management Software > ServerView - ServerView Suite CDs/DVDs/ISO-Images".
6. Download the zip file of "ServerView Management and Serviceability DVD" containing the ISO file.

Please unzip the downloaded zip file and place `SVSxx.xx.xx.xx.iso` on your Ansible control node.  
You can also extract `dsnap.exe` from `SVSxx.xx.xx.xx.iso` in advance and place it on your Ansible control node to reduce execution time.  
The path to `dsnap.exe` is `SVSxx.xx.xx.xx.iso\SVSLocalTools\<your language>\DSNAP\<your cpu_arch>\dsnap.exe`.

Requirements
------------

This role depends on the following Ansible collections:

- `ansible.windows` >= 1.14.0
- `community.windows` >= 1.13.0

Role Variables
--------------

| Name | Required | Default Value | Choices | Type | Description |
|------|----------|---------------|---------|------|-------------|
| `cpu_arch` | false | `x64` | `x64`, <br> `x86` | str | Architecture of your Windows Server. <br> This parameter is used when the ISO file is selected for `filename`. |
| `language` | false | `English` | `English`, <br> `Japanese` | str | Language of DSNAP. <br> This parameter is used when the ISO file is selected for `filename`. |
| `path` | true | | | str | Path to the EXE or ISO file placed on the Ansible control node. <br> Example: <ul> <li>/path/to/dsnapfile/dsnap.exe</li> <li>/path/to/dsnapfile/SVS15.24.06.03.iso</li> </ul>  |

Dependencies
------------

None

Example Playbook
----------------

    ---
    - name: Set up DSNAP
      hosts: windows
      roles:
        - role: fujitsu.primergy.win_dsnap
          vars:
            language: Japanese
            path: /path/to/dsnapfile/SVS15.24.06.03.iso

License
-------

GPL-3.0-or-later

Author Information
------------------

- Tomohisa Nakai <nakai.tomohisa@fujitsu.com>
