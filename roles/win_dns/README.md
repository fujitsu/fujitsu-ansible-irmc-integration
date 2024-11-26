win_dns
=========

Set DNS IPv4 address on adapters.

Requirements
------------

This role depends on the following Ansible collections:

- `ansible.windows` >= 2.5.0

Role Variables
--------------

| Name | Required | Default Value | Choices | Type | Description |
|------|----------|---------------|---------|------|-------------|
| `adapter_names` | true | | | str | Adapter name or list of adapter names for which to manage DNS settings ("*" is supported as a wildcard value).<br>The adapter name used is the connection caption in the Network Control Panel or via `Get-NetAdapter` |
| `ipv4_addresses` | true | | | str | Single or ordered list of DNS server IPv4 addresses to configure for lookup. An empty list will configure the adapter to use the DHCP-assigned values on connections where DHCP is enabled, or disable DNS lookup on statically-configured connections. |

Dependencies
------------

None

Example Playbook
----------------

playbook.yml:

    ---
    - name: Set DNS
      hosts: windows
      roles:
        - role: fujitsu.primergy.win_dns
          vars:
            adapter_names: Enthernet
            ipv4_addresses:
              - 192.0.2.1
              - 192.0.2.2

License
-------

GPL-3.0-or-later

Author Information
------------------

- Jiajun Guo <guo.jiajun@fujitsu.com>
