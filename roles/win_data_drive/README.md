win_data_drive
=========

Create/resize/remove a data partition.

Requirements
------------

None

Role Variables
--------------

| Name | Required | Default Value | Choices | Type | Description |
|------|----------|---------------|---------|------|-------------|
| `op` | true | | `create`<br>`resize`<br>`remove` | str | Select an operation to create, resize or remove a partition. |
| `drive_letter` | true | | `A-Z` | str | Used for accessing partitions. |
| `partition_size` | false | Maximum supported size | | str | Specify size of the partition in B, KB, KiB, MB, MiB, GB, GiB, TB or TiB. |
| `disk_number` | false | | | int | Select a disk to create a new partition.<br>This must be set when op is `create`. |
| `file_system` | false | | `ntfs`<br>`refs`<br>`exfat`<br>`fat32`<br>`fat` | str | Used to specify the file system to be used when formatting the target volume. |
| `new_label` | false | | | str | Used to specify the new file system label of the formatted volume. |

Dependencies
------------

None

Example Playbook
----------------

playbook.yml:

    ---
    - name: Create a new partition
      hosts: windows
      gather_facts: false
      vars:
        drive_letter: D
        disk_number: 0
        op: "create"
      roles:
        - win_data_drive

    ---
    - name: Resize a partition
      hosts: windows
      gather_facts: false
      vars:
        drive_letter: D
        partition_size: 100 GB
        op: "resize"
      roles:
        - win_data_drive

    ---
    - name: Remove a partition
      hosts: windows
      gather_facts: false
      vars:
        drive_letter: D
        op: "remove"
      roles:
        - win_data_drive

License
-------

GPL-3.0-or-later

Author Information
------------------

- Jiajun Guo <guo.jiajun@fujitsu.com>