irmc_install_windows
====================

Install Windows OS via iRMC virtual CD.

NOTE:
After the Windows Server installation is complete, login as Administrator and execute the following command to enable control from Ansible.

```powershell
 New-NetFirewallRule -Name "WinRM HTTP" -DisplayName "Allow WinRM over HTTP" -Enabled True -Direction Inbound -Protocol TCP -LocalPort 5985 -Action Allow
```

Requirements
------------

None

Role Variables
--------------

| Name | Required | Default Value | Choices | Type | Description |
|------|----------|---------------|---------|------|-------------|
| `server` | true | | | str | Remote server (IP or DNS name) where the image is located. |
| `share` | true | | | str | Path on the remote server where the image is located. |
| `image` | true | | | str | Name of the remote image. |
| `share_type` | true | | `NFS`<br>`SMB` | str | Share type (NFS share or SMB share). |
| `vm_user` | false | | | str | User account in case of SMB share. |
| `vm_password` | false | | | str | User password in case of SMB share. |
| `vm_domain` | false | | | str | User domain in case of SMB share. |

Dependencies
------------

None

Example Playbook
----------------

playbook.yml:

    ---
    - name: Install windows
      connection: local
      hosts: iRMC_group
      gather_facts: false
      roles:
        - role: fujitsu.primergy.irmc_install_windows
          vars:
            server: "192.0.2.1"
            share: "/var/share"
            image: "/image.iso"
            share_type: "NFS"

    - name: Waiting for OS installation completed
      hosts: windows
      gather_facts: false
      tasks:
        - name: Waiting for WinRM to be available
          ansible.builtin.wait_for_connection:
            timeout: 5400
        - name: Show completion message
          ansible.builtin.debug:
            msg: "OS installation is completed."

    - name: Disconnect iRMC Virtual CD after installation
      hosts: iRMC_group
      gather_facts: false
      connection: local
      - name: Disconnect Virtual CD
        fujitsu.primergy.irmc_connectvm:
          irmc_url: "{{ inventory_hostname }}"
          irmc_username: "{{ irmc_user }}"
          irmc_password: "{{ irmc_password }}"
          validate_certs: "{{ validate_certificate }}"
          command: "DisconnectCD"
        delegate_to: localhost

License
-------

GPL-3.0-or-later

Author Information
------------------

- Jiajun Guo <guo.jiajun@fujitsu.com>
