# Fujitsu PRIMERGY iRMC modules

## Modules

  * [irmc_biosbootorder - configure iRMC to force next boot to specified option](#irmc_biosbootorder)
  * [irmc_cas - manage iRMC CAS settings](#irmc_cas)
  * [irmc_certificate - manage iRMC certificates](#irmc_certificate)
  * [irmc_compare_profiles - compare two iRMC profiles](#irmc_compare_profiles)
  * [irmc_connectvm - connect iRMC Virtual Media Data](#irmc_connectvm)
  * [irmc_elcm_offline_update - offline update a server via iRMC](#irmc_elcm_offline_update)
  * [irmc_elcm_online_update - online update a server via iRMC](#irmc_elcm_online_update)
  * [irmc_elcm_repository - configure the eLCM repostory in iRMC](#irmc_elcm_repository)
  * [irmc_eventlog - handle iRMC eventlogs](#irmc_eventlog)
  * [irmc_facts - get or set PRIMERGY server and iRMC facts](#irmc_facts)
  * [irmc_fwbios_update - update iRMC Firmware or server BIOS](#irmc_fwbios_update)
  * [irmc_getvm - get iRMC Virtual Media Data](#irmc_getvm)
  * [irmc_idled - get or set server ID LED](#irmc_idled)
  * [irmc_ldap - manage iRMC LDAP settings](#irmc_ldap)
  * [irmc_license - manage iRMC user accounts](#irmc_license)
  * [irmc_ntp - manage iRMC time options](#irmc_ntp)
  * [irmc_powerstate - get or set server power state](#irmc_powerstate)
  * [irmc_profiles - handle iRMC profiles](#irmc_profiles)
  * [irmc_raid - handle iRMC RAID](#irmc_raid)
  * [irmc_scci - execute iRMC remote SCCI commands](#irmc_scci)
  * [irmc_session - handle iRMC sessions](#irmc_session)
  * [irmc_setnextboot - configure iRMC to force next boot to specified option](#irmc_setnextboot)
  * [irmc_setvm - set iRMC Virtual Media Data](#irmc_setvm)
  * [irmc_task - handle iRMC tasks](#irmc_task)
  * [irmc_user - manage iRMC user accounts](#irmc_user)

---
### irmc_biosbootorder

#### Description
* Ansible module to configure the BIOS boot oder via iRMC.
* Using this module will force server into several reboots.
* The module will abort by default if the PRIMERGY server is powered on.
* Module Version V1.2.

#### Requirements
  * The module needs to run locally.
  * The PRIMERGY server needs to be at least a M2 model.
  * iRMC S4 needs FW >= 9.04, iRMC S5 needs FW >= 1.25.
  * Python >= 2.6
  * Python modules 'future', 'requests', 'urllib3'

#### Options

| Parameter | Required | Default | Choices | Description |
|:----------|:---------|:--------|:--------|:----------- |
| boot_device  |  No  |  | | String to match with specified key for existing boot devices. Needs to be provided for 'set' command. |
| boot_key  |  No  |  StructuredBootString  | DeviceName<br/> StructuredBootString<br/>  | Which key to check for in bios boot order devices. |
| command  |  No  |  get  | get<br/> set<br/> default<br/>  | Get or set BIOS Boot Order. |
| force_new  |  No  |  False  | | Force generation of new BiosBootOrder configuration in iRMC before getting or setting boot order. |
| ignore_power_on  |  No  |  False  | | Ignore that server is powered on. |
| irmc_password  |  Yes  |  | | Password for iRMC user for basic authentication. |
| irmc_url  |  Yes  |  | | IP address of the iRMC to be requested for data. |
| irmc_username  |  Yes  |  | | iRMC user for basic authentication. |
| next_boot_device  |  No  |  | | Set next boot to specified device. |
| validate_certs  |  No  |  True  | | Evaluate SSL certificate (set to false for self-signed certificate). |

#### Examples
```yaml
# Get Bios Boot Order
- name: Get Bios Boot Order
  irmc_biosbootorder:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "get"
    force_new: false
  delegate_to: localhost

# Set Bios Boot Order to default
- name: Get Bios Boot Order to default
  irmc_biosbootorder:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "default"
    ignore_power_on: false
  delegate_to: localhost
```

#### Return Values

**boot_order returned for command "get":**

| Name | Description | Returned | Type | Example |
|:-----|:------------|:---------|:-----|:--------|
| DeviceIdx | device index | always | int | 1 |
| DeviceName | device name | always | string | (Bus 01 Dev 00)PCI RAID Adapter |
| StructuredBootString | structured boot string | always | string | RAID.Slot.1.Legacy |

**For all other commands:**

Default return values

#### Notes

- See http://manuals.ts.fujitsu.com/file/13371/irmc-restful-spec-en.pdf
- See http://manuals.ts.fujitsu.com/file/13372/irmc-redfish-wp-en.pdf

---
### irmc_cas

#### Description
* Ansible module to manage iRMC CAS settings via iRMC remote scripting interface.
* Module Version V1.2.

#### Requirements
  * The module needs to run locally.
  * Python >= 2.6
  * Python modules 'future', 'requests', 'urllib3'

#### Options

| Parameter | Required | Default | Choices | Description |
|:----------|:---------|:--------|:--------|:----------- |
| command  |  No  |  get  | get<br/> set<br/>  | How to handle iRMC CAS data. |
| enabled  |  No  |  | | CAS enabled. |
| irmc_password  |  Yes  |  | | Password for iRMC user for basic authentication. |
| irmc_url  |  Yes  |  | | IP address of the iRMC to be requested for data. |
| irmc_username  |  Yes  |  | | iRMC user for basic authentication. |
| login_always  |  No  |  | | Always Display Login Page. |
| login_uri  |  No  |  | | CAS Login URL. |
| logout_uri  |  No  |  | | CAS Logout URL. |
| port  |  No  |  | | CAS Port. |
| privilege_avr  |  No  |  | | Video Redirection Enabled. |
| privilege_bmc  |  No  |  | | Configure iRMC Settings. |
| privilege_level  |  No  |  | Reserved<br/> Callback<br/> User<br/> Operator<br/> Administrator<br/> OEM<br/> NoAccess<br/>  | Privilege Level. |
| privilege_source  |  No  |  | Local<br/> LDAP<br/>  | Assign CAS permissions from. |
| privilege_storage  |  No  |  | | Remote Storage Enable. |
| privilege_user  |  No  |  | | Configure User Accounts. |
| server  |  No  |  | | CAS Server. |
| ssl_verify  |  No  |  | | Verify SSL Certificate. |
| validate_certs  |  No  |  True  | | Evaluate SSL certificate (set to false for self-signed certificate). |
| validate_uri  |  No  |  | | CAS Validate URL. |

#### Examples
```yaml
# Get CAS data
- name: Get CAS data
  irmc_cas:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "get"
  register: cas
  delegate_to: localhost
- name: Show iRMC CAS data
  debug:
    msg: "{{ cas.cas }}"

# Set CAS data
- name: Set CAS data
  irmc_cas:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "set"
    cas_user: "username"
    cas_password: "password"
  delegate_to: localhost
```

#### Return Values

**CAS data returned by command "get":**

| Name | Description | Returned | Type | Example |
|:-----|:------------|:---------|:-----|:--------|
| enabled | CAS enabled | always | bool | False |
| login_always | always Display Login Page | always | bool | True |
| login_uri | CAS Login URL | always | string | /cas/login |
| logout_uri | CAS Logout URL | always | string | /cas/logout |
| port | CAS port | always | int | 3170 |
| privilege_avr | Video Redirection Enabled | always | bool | False |
| privilege_bmc | configure iRMC Settings | always | bool | False |
| privilege_level | privilege Level | always | string | Operator |
| privilege_source | assign CAS permissions from | always | string | Local |
| privilege_storage | Remote Storage Enable | always | bool | False |
| privilege_user | configure User Accounts | always | bool | False |
| server | CAS server | always | string | cas_server.local |
| ssl_verify | verify SSL Certificate | always | bool | True |
| validate_uri | CAS Validate URL | always | string | /cas/validate |

**For command "set":**

Default return values

#### Notes

- See http://manuals.ts.fujitsu.com/file/12563/wp-svs-irmc-remote-scripting-en.pdf
- See https://sp.ts.fujitsu.com/dmsp/Publications/public/dp-svs-configuration-space-values-en.pdf

---
### irmc_certificate

#### Description
* Ansible module to manage iRMC certificates via iRMC remote scripting interface.
* Module Version V1.2.

#### Requirements
  * The module needs to run locally.
  * Python >= 2.6
  * Python modules 'future', 'requests', 'urllib3'

#### Options

| Parameter | Required | Default | Choices | Description |
|:----------|:---------|:--------|:--------|:----------- |
| command  |  No  |  get  | get<br/> set<br/>  | Get or set iRMC certificate(s). |
| irmc_password  |  Yes  |  | | Password for iRMC user for basic authentication. |
| irmc_url  |  Yes  |  | | IP address of the iRMC to be requested for data. |
| irmc_username  |  Yes  |  | | iRMC user for basic authentication. |
| private_key_path  |  No  |  | | Path to file containing SSL private key. This option also requires the SSL certificate. |
| ssl_ca_cert_path  |  No  |  | | Path to file containing SSL CA certificate. |
| ssl_cert_path  |  No  |  | | Path to file containing SSL certificate. This option also requires the SSL private key. |
| validate_certs  |  No  |  True  | | Evaluate SSL certificate (set to false for self-signed certificate). |

#### Examples
```yaml
# Get SSL certificates
- name: Get SSL certificates
  irmc_certificate:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "get"
  register: certificates
  delegate_to: localhost
- name: show certificates
  debug:
    msg: "{{ certificates.certificates }}"

# Set SSL certificates
- name: Set SSL certificates
  irmc_certificate:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "set"
    private_key_path: "{{ private_key_path }}"
    ssl_cert_path: "{{ ssl_cert_path }}"
    ssl_ca_cert_path: "{{ ssl_ca_cert_path }}"
  delegate_to: localhost
```

#### Return Values

**Certificates returned by command "get":**

| Name | Description | Returned | Type | Example |
|:-----|:------------|:---------|:-----|:--------|
| ssl_ca_certificate | SSL CA certificate | always | string |  |
| ssl_certificate | SSL certificate | always | string |  |

**For command "set":**

Default return values

#### Notes

- See http://manuals.ts.fujitsu.com/file/12563/wp-svs-irmc-remote-scripting-en.pdf
- See https://sp.ts.fujitsu.com/dmsp/Publications/public/dp-svs-configuration-space-values-en.pdf

---
### irmc_compare_profiles

#### Description
* Ansible module to compare two iRMC profiles.
* Module Version V1.2.

#### Requirements
  * The module needs to run locally.
  * iRMC S4 needs FW >= 9.04, iRMC S5 needs FW >= 1.25.
  * Python >= 2.6
  * Python module 'future'

#### Options

| Parameter | Required | Default | Choices | Description |
|:----------|:---------|:--------|:--------|:----------- |
| profile_json1  |  No  |  | | iRMC profile to be compared against another. Takes precedence over profile_path1 when set. |
| profile_json2  |  No  |  | | iRMC profile to be compared against another. Takes precedence over profile_path2 when set. |
| profile_path1  |  No  |  | | Path to file with iRMC profile to be compared against another. Ignored if profile1 is set. |
| profile_path2  |  No  |  | | Path to file with iRMC profile to be compared against another. Ignored if profile2 is set. |

#### Examples
```yaml
# Compare iRMC profiles against each other
- name: Compare iRMC profiles
  irmc_compare_profiles:
    profile_path1: "{{ profile1_path }}"
    profile_path2: "{{ profile2_path }}"
  delegate_to: localhost
```

#### Return Values

| Name | Description | Returned | Type | Example |
|:-----|:------------|:---------|:-----|:--------|
| comparison_list | rudimentary list of probable comparison differences | when comparison_result is False | list |  |
| comparison_result | profile comparison result | always | bool | False |


---
### irmc_connectvm

#### Description
* Ansible module to connect iRMC Virtual Media Data via the iRMC RedFish interface.
* Module Version V1.3.0.

#### Requirements
  * The module needs to run locally.
  * iRMC S6.
  * Python >= 3.10
  * Python modules 'requests', 'urllib3'

#### Options

| Parameter | Required | Default | Choices | Description |
|:----------|:---------|:--------|:--------|:----------- |
| command  |  No  |  ConnectCD  | ConnectCD<br/> ConnectHD<br/> DisconnectCD<br/> DisconnectHD<br/>  | The virtual media connect command to be executed. |
| irmc_password  |  Yes  |  | | Password for iRMC user for basic authentication. |
| irmc_url  |  Yes  |  | | IP address of the iRMC to be requested for data. |
| irmc_username  |  Yes  |  | | iRMC user for basic authentication. |
| validate_certs  |  No  |  True  | | Evaluate SSL certificate (set to false for self-signed certificate). |

#### Examples
```yaml
# Disconnect Virtual CD
- name: Disconnect Virtual CD
  irmc_connectvm:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "DisconnectCD"
  delegate_to: localhost
  tags: 
    - disconnectCD

# Connect Virtual CD
- name: Connect Virtual CD
  irmc_connectvm:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "ConnectCD"
  delegate_to: localhost
  tags: 
    - connectCD

# Disconnect Virtual HD
- name: Disconnect Virtual HD
  irmc_connectvm:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "DisconnectHD"
  delegate_to: localhost
  tags: 
    - disconnectHD

# Connect Virtual HD
- name: Connect Virtual HD
  irmc_connectvm:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "ConnectHD"
  delegate_to: localhost
  tags: 
    - connectHD
```

#### Return Values

Default return values

---
### irmc_elcm_offline_update

#### Description
* Ansible module to offline update a server via iRMC.
* Using this module may force the server into reboot.
* See specification [iRMC RESTful API](http://manuals.ts.fujitsu.com/file/13371/irmc-restful-spec-en.pdf).
* Module Version V1.2.

#### Requirements
  * The module needs to run locally.
  * eLCM needs to be licensed in iRMC.
  * eLCM SD card needs to be mounted.
  * The PRIMERGY server needs to be at least a M2 model.
  * iRMC S4 needs FW >= 9.04, iRMC S5 needs FW >= 1.25.
  * The module assumes that the Update Repository is set correctly in iRMC.
  * Python >= 2.6
  * Python modules 'future', 'requests', 'urllib3'

#### Options

| Parameter | Required | Default | Choices | Description |
|:----------|:---------|:--------|:--------|:----------- |
| command  |  No  |  | prepare<br/> execute<br/>  | How to handle iRMC eLCM Offline Update. |
| ignore_power_on  |  No  |  False  | | Ignore that server is powered on. Server will reboot during update process. Only valid for option 'execute'. |
| irmc_password  |  Yes  |  | | Password for iRMC user for basic authentication. |
| irmc_url  |  Yes  |  | | IP address of the iRMC to be requested for data. |
| irmc_username  |  Yes  |  | | iRMC user for basic authentication. |
| skip_hcl_verify  |  No  |  False  | | For VMware OS the Hardware Compatibility List (HCL) verification will be skipped and updates will be offered regardless of their compatibility with the current VMware OS version. Irrelevant for other OS. |
| validate_certs  |  No  |  True  | | Evaluate SSL certificate (set to false for self-signed certificate). |
| wait_for_finish  |  No  |  True  | | Wait for session to finish. |

#### Examples
```yaml
# Prepare eLCM Offline Update
- name: Prepare eLCM Offline Update
  irmc_elcm_offline_update:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "prepare"
    skip_hcl_verify: "{{ elcm_skip_hcl_verify }}"
    ignore_power_on: false
  delegate_to: localhost

# Execute eLCM Offline Update
- name: Execute eLCM Offline Update
  irmc_elcm_offline_update:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "execute"
    ignore_power_on: false
    wait_for_finish: true
```

#### Return Values

| Name | Description | Returned | Type | Example |
|:-----|:------------|:---------|:-----|:--------|
| For all commands |  |  |  |  |

#### Notes

- See http://manuals.ts.fujitsu.com/file/13371/irmc-restful-spec-en.pdf
- See http://manuals.ts.fujitsu.com/file/13372/irmc-redfish-wp-en.pdf

---
### irmc_elcm_online_update

#### Description
* Ansible module to online update a server via iRMC.
* Using this module may force the server into reboot.
* See specification [iRMC RESTful API](http://manuals.ts.fujitsu.com/file/13371/irmc-restful-spec-en.pdf).
* PRIMERGY servers running ESXi are not capable of eLCM Online Update due to missing agent. Please run eLCM Offline Update on ESXi servers.
* Module Version V1.2.

#### Requirements
  * The module needs to run locally.
  * eLCM needs to be licensed in iRMC.
  * eLCM SD card needs to be mounted.
  * The PRIMERGY server needs to be at least a M2 model.
  * iRMC S4 needs FW >= 9.04, iRMC S5 needs FW >= 1.25.
  * The module assumes that the Update Repository is set correctly in iRMC.
  * Python >= 2.6
  * Python modules 'future', 'requests', 'urllib3'

#### Options

| Parameter | Required | Default | Choices | Description |
|:----------|:---------|:--------|:--------|:----------- |
| command  |  No  |  | get<br/> set<br/> check<br/> execute<br/> delete<br/>  | How to handle iRMC eLCM Online Update. |
| component  |  No  |  | | Component whose execution selection is to be changed. |
| irmc_password  |  Yes  |  | | Password for iRMC user for basic authentication. |
| irmc_url  |  Yes  |  | | IP address of the iRMC to be requested for data. |
| irmc_username  |  Yes  |  | | iRMC user for basic authentication. |
| select  |  No  |  | | Execution selection for specified component/subcomponent. |
| skip_hcl_verify  |  No  |  False  | | For VMware OS the Hardware Compatibility List (HCL) verification will be skipped and updates will be offered regardless of their compatibility with the current VMware OS version. Irrelevant for other OS. |
| subcomponent  |  No  |  | | Subcomponent whose execution selection is to be changed. |
| validate_certs  |  No  |  True  | | Evaluate SSL certificate (set to false for self-signed certificate). |
| wait_for_finish  |  No  |  True  | | Wait for session to finish. |

#### Examples
```yaml
# Generate eLCM Online Update List
- name: Generate eLCM Online Update List
  irmc_elcm_online_update:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "check"
    skip_hcl_verify: "{{ elcm_skip_hcl_verify }}"
    wait_for_finish: true
  delegate_to: localhost

# Read eLCM Online Update List
- name: Read eLCM Online Update List
  irmc_elcm_online_update:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "get"
  delegate_to: localhost

# De-select entry in eLCM Online Update List
- name: De-select entry in eLCM Online Update List
  irmc_elcm_online_update:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "set"
    component: "{{ elcm_component }}"
    subcomponent: "{{ elcm_subcomponent }}"
    select: false
    wait_for_finish: true
  delegate_to: localhost

# Execute eLCM Online Update
- name: Execute eLCM Online Update
  irmc_elcm_online_update:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "execute"
    wait_for_finish: true

# Delete eLCM Online Update List
- name: Delete eLCM Online Update List
  irmc_elcm_online_update:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "delete"
  delegate_to: localhost
```

#### Return Values

**online update collection returned for command "get":**

| Name | Description | Returned | Type | Example |
|:-----|:------------|:---------|:-----|:--------|
| update_collection | list of components which require update with specific data (component, subcomponent, status, severity, selected, reboot, current, new) | always | dict |  |

**For all other commands:**

Default return values

#### Notes

- See http://manuals.ts.fujitsu.com/file/13371/irmc-restful-spec-en.pdf
- See http://manuals.ts.fujitsu.com/file/13372/irmc-redfish-wp-en.pdf

---
### irmc_elcm_repository

#### Description
* Ansible module to configure the eLCM repostory in iRMC.
* iRMC tests access to specified repository and refuses to accept data in case of failure.
* See specification [iRMC RESTful API](http://manuals.ts.fujitsu.com/file/13371/irmc-restful-spec-en.pdf).
* Module Version V1.2.

#### Requirements
  * The module needs to run locally.
  * The PRIMERGY server needs to be at least a M2 model.
  * eLCM needs to be licensed in iRMC.
  * eLCM SD card needs to be mounted.
  * iRMC S4 needs FW >= 9.04, iRMC S5 needs FW >= 1.25.
  * Python >= 2.6
  * Python modules 'future', 'requests', 'urllib3'

#### Options

| Parameter | Required | Default | Choices | Description |
|:----------|:---------|:--------|:--------|:----------- |
| catalog  |  No  |  | | Path to eLCM Update Repository on server. Needs to be set together with 'server'. |
| command  |  No  |  get  | get<br/> set<br/>  | How to handle iRMC eLCM respository data. |
| irmc_password  |  Yes  |  | | Password for iRMC user for basic authentication. |
| irmc_url  |  Yes  |  | | IP address of the iRMC to be requested for data. |
| irmc_username  |  Yes  |  | | iRMC user for basic authentication. |
| proxy_password  |  No  |  | | Proxy password to access eLCM Update Repository. |
| proxy_port  |  No  |  | | Proxy port to access eLCM Update Repository. |
| proxy_url  |  No  |  | | Proxy server to access eLCM Update Repository. |
| proxy_user  |  No  |  | | Proxy user to access eLCM Update Repository. |
| server  |  No  |  | | Server where eLCM Update Repository is located. Needs to be set together with 'catalog'. |
| use_proxy  |  No  |  | | Whether to use proxy to access eLCM Update Repository. |
| validate_certs  |  No  |  True  | | Evaluate SSL certificate (set to false for self-signed certificate). |
| wait_for_finish  |  No  |  True  | | Wait for session to finish. |

#### Examples
```yaml
# Get eLCM repository data
- name: Get eLCM repository data
  irmc_elcm_repository:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "get"
  delegate_to: localhost

# Set eLCM repository data
- name: Set eLCM repository data
  irmc_elcm_repository:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "set"
    server: "{{ elcm_server }}"
    catalog: "{{ elcm_catalog }}"
    use_proxy: "{{ elcm_use_proxy }}"
    proxy_url: "{{ elcm_proxy_url }}"
    proxy_port: "{{ elcm_proxy_port }}"
    proxy_user: "{{ elcm_proxy_user }}"
    proxy_password: "{{ elcm_proxy_password }}"
    wait_for_finish: true
```

#### Return Values

**eLCM data returned for command "get":**

| Name | Description | Returned | Type | Example |
|:-----|:------------|:---------|:-----|:--------|
| repository | eLCM repository data | always | dict |  |

#### Notes

- See http://manuals.ts.fujitsu.com/file/13371/irmc-restful-spec-en.pdf
- See http://manuals.ts.fujitsu.com/file/13372/irmc-redfish-wp-en.pdf

---
### irmc_eventlog

#### Description
* Ansible module to handle iRMC eventlogs via Restful API.
* Module Version V1.2.

#### Requirements
  * The module needs to run locally.
  * iRMC S4 needs FW >= 9.04, iRMC S5 needs FW >= 1.25.
  * Python >= 2.6
  * Python modules 'future', 'requests', 'urllib3'

#### Options

| Parameter | Required | Default | Choices | Description |
|:----------|:---------|:--------|:--------|:----------- |
| command  |  No  |  list  | list<br/> get<br/> clear<br/>  | Handle iRMC eventlogs. |
| eventlog_type  |  No  |  SystemEventLog  | SystemEventLog<br/> InternalEventLog<br/>  | Specific eventlog to handle. |
| id  |  No  |  | | Specific eventlog ID to get. |
| irmc_password  |  Yes  |  | | Password for iRMC user for basic authentication. |
| irmc_url  |  Yes  |  | | IP address of the iRMC to be requested for data. |
| irmc_username  |  Yes  |  | | iRMC user for basic authentication. |
| validate_certs  |  No  |  True  | | Evaluate SSL certificate (set to false for self-signed certificate). |

#### Examples
```yaml
# List iRMC InternalEventLog
- name: List iRMC InternalEventLog
  irmc_eventlog:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "list"
    eventlog_type: "InternalEventLog"
  delegate_to: localhost

# Get specific SystemEventLog entry information
- name: Get specific SystemEventLog entry information
  irmc_eventlog:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "get"
    id: 0
  delegate_to: localhost
```

#### Return Values

**eventlog_entry data returned for command "get":**

| Name | Description | Returned | Type | Example |
|:-----|:------------|:---------|:-----|:--------|
| AlertGroup | group which caused the event | always | string | Memory |
| Cause | reason for the event if available | always | string | The memory module was not approved and released for this system by the system manufacturer |
| Created | dated of the event | always | string | 2018-07-24T15:57:40+02:00 |
| EventSource | where the event originated from | always | string | iRMC S5 |
| Id | event ID | always | int | 20 |
| Message | event entry text | always | string | DIMM-1E Non Fujitsu Memory Module detected - Warranty restricted! |
| Resolutions | list of possible solitions for the problem, if available | always | list |  |
| Severity | serverity of event | always | string | Warning |
| Type | event type | always | string | SEL |

**eventlog data returned for command "list":**

List of individual eventlog_entries (see above)

**For all other commands:**

Default return values

#### Notes

- See http://manuals.ts.fujitsu.com/file/13371/irmc-restful-spec-en.pdf
- See http://manuals.ts.fujitsu.com/file/13372/irmc-redfish-wp-en.pdf

---
### irmc_facts

#### Description
* Ansible module to get or set basic iRMC and PRIMERGY server data via iRMC RedFish interface.
* Module Version V1.2.

#### Requirements
  * The module needs to run locally.
  * iRMC S4 needs FW >= 9.04, iRMC S5 needs FW >= 1.25.
  * Python >= 2.6
  * Python modules 'future', 'requests', 'urllib3'

#### Options

| Parameter | Required | Default | Choices | Description |
|:----------|:---------|:--------|:--------|:----------- |
| asset_tag  |  No  |  | | Server asset tag. |
| command  |  No  |  get  | get<br/> set<br/>  | How to access server facts. |
| contact  |  No  |  | | System contact. |
| description  |  No  |  | | Server description. |
| helpdesk_message  |  No  |  | | Help desk message. |
| irmc_password  |  Yes  |  | | Password for iRMC user for basic authentication. |
| irmc_url  |  Yes  |  | | IP address of the iRMC to be requested for data. |
| irmc_username  |  Yes  |  | | iRMC user for basic authentication. |
| location  |  No  |  | | Server location. |
| validate_certs  |  No  |  True  | | Evaluate SSL certificate (set to false for self-signed certificate). |

#### Examples
```yaml
# Get basic server and iRMC facts
- name: Get basic server and iRMC facts
  irmc_facts:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "get"
  register: facts
  delegate_to: localhost
- name: Show server and iRMC facts
  debug:
    msg: "{{ facts.facts }}"

# Set server asset tag
- name: Set server asset tag
  irmc_facts:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "set"
    asset_tag: "Ansible test server"
  delegate_to: localhost
```

#### Return Values

**facts returned by "get":**

| Name | Description | Returned | Type | Example |
|:-----|:------------|:---------|:-----|:--------|
| hardware.ethernetinterfaces | dict with total number (count) and list of ethernet interfaces (devices) with relevant data (id, macaddress, name) | always | dict | {u'count': 2, u'devices': [{u'macaddress': u'01:02:03:04:05:06', u'id': u'0', u'name': u'eth0'}, {u'macaddress': u'01:02:03:04:05:06', u'id': u'1', u'name': u'eth1'}]} |
| hardware.fans | dict with available fan slots (sockets) and total number (count) and list of existing fans (devices) with relevant data (id, manufacturer, name, size)<br/> <i>note that fan devices are only returned if server is 'On'</i> | always | dict | {u'count': 2, u'sockets': 24, u'devices': [{u'manufacturer': u'Micron Technology', u'id': u'0', u'name': u'DIMM-1A', u'size': 8192}, {u'manufacturer': u'SK Hynix', u'id': u'12', u'name': u'DIMM-1E', u'size': 16384}]} |
| hardware.memory | dict with available memory slots (sockets) and total number (count) and list of existing memories (devices) with relevant data (id, manufacturer, name, size) | always | dict | {u'count': 6, u'sockets': 7, u'devices': [{u'location': u'SystemBoard', u'id': u'0', u'name': u'FAN1 SYS'}, {u'location': u'SystemBoard', u'id': u'1', u'name': u'FAN2 SYS'}, {u'location': u'SystemBoard', u'id': u'2', u'name': u'FAN3 SYS'}, {u'location': u'SystemBoard', u'id': u'3', u'name': u'FAN4 SYS'}, {u'location': u'SystemBoard', u'id': u'4', u'name': u'FAN5 SYS'}, {u'location': u'PowerSupply', u'id': u'5', u'name': u'FAN PSU1'}]} |
| hardware.powersupplies | dict with available power supply slots (sockets) and total number (count) and list of existing power supplies (devices) with relevant data (id, manufacturer, model, name) | always | dict | {u'count': 1, u'sockets': 2, u'devices': [{u'model': u'S13-450P1A', u'manufacturer': u'CHICONY', u'id': u'0', u'name': u'PSU1'}]} |
| hardware.processors | dict with available processor slots (sockets) and total number (count) and list of existing processors (devices) with relevant data (cores, id, name, threads) | always | dict | {u'count': 2, u'sockets': 2, u'devices': [{u'cores': 6, u'threads': 6, u'id': u'0', u'name': u'Genuine Intel(R) CPU @ 2.00GHz'}, {u'cores': 6, u'threads': 6, u'id': u'1', u'name': u'Genuine Intel(R) CPU @ 2.00GHz'}]} |
| hardware.storagecontrollers | dict with total number (count) and list of storage controllers (devices) with relevant data (drives, firmware, id, name, volume)<br/> <i>note that storage controllers are only returned if server is 'On'</i> | always | dict | {u'count': 1, u'devices': [{u'name': u'PRAID EP400i', u'firmware': u'4.270.00-4869', u'id': u'1000', u'volumes': 1, u'drives': 4}]} |
| irmc | dict with relevant iRMC data (fw_builddate, fw_running, fw_version, hostname, macaddress, sdrr_version) | always | dict | {u'macaddress': u'90:1B:0E:01:CA:5C', u'hostname': u'iRMC01CA5C-iRMC', u'fw_version': u'9.08F', u'fw_running': u'LowFWImage', u'fw_builddate': u'2018-03-05T14:02:44', u'sdrr_version': u'3.73'} |
| mainboard | dict with relevant mainboard data (dnumber, manufacturer, part_number, serial_number, version) | always | dict | {u'dnumber': u'D3289', u'serial_number': u'44617895', u'part_number': u'S26361-D3289-D13', u'version': u'WGS04 GS50', u'manufacturer': u'FUJITSU'} |
| system | dict with relevant system data (asset_tag, bios_version, description, health, helpdesk_message, host_name, idled_state, ip, location, manufacturer, memory_size, model, part_number, power_state, serial_number, uuid) | always | dict | {u'uuid': u'11223344-5566-cafe-babe-deadbeef1234', u'helpdesk_message': u'New helpdesk message', u'ip': u'101.102.103.104', u'description': u'server description', u'asset_tag': u'New AssetTag', u'part_number': u'ABN:K1495-VXXX-XX', u'contact': u'Admin (admin@server.room)', u'memory_size': u'24 GB', u'host_name': u'STK-SLES11SP4x64', u'power_state': u'On', u'bios_version': u'V5.0.0.9 R1.36.0 for D3289-A1x', u'serial_number': u'YLVT000098', u'model': u'PRIMERGY RX2540 M1', u'manufacturer': u'FUJITSU', u'health': u'OK', u'idled_state': u'Off', u'location': u'Server Room'} |

**For command "set":**

Default return values

#### Notes

- See http://manuals.ts.fujitsu.com/file/13371/irmc-restful-spec-en.pdf
- See http://manuals.ts.fujitsu.com/file/13372/irmc-redfish-wp-en.pdf

---
### irmc_fwbios_update

#### Description
* Ansible module to get current iRMC update settings or update iRMC Firmware or BIOS via iRMC RedFish interface.
* BIOS or firmware flash can be initiated from TFTP server or local file.
* Module Version V1.2.

#### Requirements
  * The module needs to run locally.
  * iRMC S4 needs FW >= 9.04, iRMC S5 needs FW >= 1.25.
  * Python >= 2.6
  * Python modules 'future', 'requests', 'urllib3', 'requests_toolbelt'

#### Options

| Parameter | Required | Default | Choices | Description |
|:----------|:---------|:--------|:--------|:----------- |
| command  |  No  |  get  | get<br/> update<br/>  | Get settings or run update. |
| file_name  |  No  |  | | Path to file containing correct iRMC FW or server BIOS image. |
| ignore_power_on  |  No  |  False  | | Ignore that server is powered on. |
| irmc_boot_selector  |  No  |  | Auto<br/> LowFWImage<br/> HighFWImage<br/>  | Which iRMC FW image is to be started after iRMC reboot. |
| irmc_flash_selector  |  No  |  | Auto<br/> LowFWImage<br/> HighFWImage<br/>  | Which iRMC image to replace with the new firmware. |
| irmc_password  |  Yes  |  | | Password for iRMC user for basic authentication. |
| irmc_url  |  Yes  |  | | IP address of the iRMC to be requested for data. |
| irmc_username  |  Yes  |  | | iRMC user for basic authentication. |
| server_name  |  No  |  | | TFTP server name or IP. ignored if update_source is set to 'file' |
| timeout  |  No  |  30  | | Timeout for BIOS/iRMC FW flash process in minutes. |
| update_source  |  No  |  | tftp<br/> file<br/>  | Where to get the FW or BIOS update file. |
| update_type  |  No  |  | irmc<br/> bios<br/>  | Whether to update iRMC FW or server BIOS. |
| validate_certs  |  No  |  True  | | Evaluate SSL certificate (set to false for self-signed certificate). |

#### Examples
```yaml
# Get irmc firmware and BIOS update settings
- name: Get irmc firmware and BIOS update settings
  irmc_fwbios_update:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "get"
  register: fw_settings
  delegate_to: localhost
- name: Show irmc firmware and BIOS update settings
  debug:
    msg: "{{ fw_settings.fw_update_configuration }}"

# Update server BIOS from local file
- name: Update server BIOS from local file
  irmc_fwbios_update:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "update"
    update_source: "file"
    update_type: "bios"
    file_name: "{{ bios_filename }}"
  delegate_to: localhost

# Update iRMC FW via TFTP
- name: Update iRMC FW via TFTP
  irmc_fwbios_update:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "update"
    update_source: "tftp"
    update_type: "irmc"
    server_name: "{{ tftp_server }}"
    file_name: "{{ irmc_filename }}"
    irmc_flash_selector: "Auto"
    irmc_boot_selector: "Auto"
  delegate_to: localhost
```

#### Return Values

**For "update" command:**

Default return values

**fw_update_configuration  returned for command "get":**

| Name | Description | Returned | Type | Example |
|:-----|:------------|:---------|:-----|:--------|
| <fw_image>.BooterVersion | booter version | always | string | 8.08 |
| <fw_image>.FirmwareBuildDate | firmware build date | always | string | Dec 1 2017 21:36:17 CEST |
| <fw_image>.FirmwareRunningState | firmware running state | always | string | Inactive |
| <fw_image>.FirmwareVersion | iRMC firmware version | always | string | 9.04F |
| <fw_image>.ImageDescription | firmware image description | always | string | PRODUCTION RELEASE |
| <fw_image>.SDRRId | sensor data record repository id | always | string | 308 |
| <fw_image>.SDRRVersion | sensor data record repository version | always | string | 3.11 |
| bios_file_name | BIOS file name | always | string | D3279-B1x.R1.20.0.UPC |
| bios_version | current BIOS version | always | string | V5.0.0.11 R1.20.0 for D3279-B1x |
| irmc_boot_selector | selector for iRMC FW to boot | always | string | MostRecentProgrammedFW |
| irmc_file_name | iRMC Firmware image name | always | string | D3279_09.09F_sdr03.12.bin |
| irmc_flash_selector | selector for iRMC FW to flash | always | string | Auto |
| power_state | server power state | always | string | False |
| tftp_server_name | TFTP server name | always | string | tftpserver.local |

#### Notes

- See http://manuals.ts.fujitsu.com/file/13371/irmc-restful-spec-en.pdf
- See http://manuals.ts.fujitsu.com/file/13372/irmc-redfish-wp-en.pdf

---
### irmc_getvm

#### Description
* Ansible module to get iRMC Virtual Media Data via iRMC RedFish interface.
* Module Version V1.3.0.

#### Requirements
  * The module needs to run locally.
  * iRMC S6.
  * Python >= 3.10
  * Python modules 'requests', 'urllib3'

#### Options

| Parameter | Required | Default | Choices | Description |
|:----------|:---------|:--------|:--------|:----------- |
| irmc_password  |  Yes  |  | | Password for iRMC user for basic authentication. |
| irmc_url  |  Yes  |  | | IP address of the iRMC to be requested for data. |
| irmc_username  |  Yes  |  | | iRMC user for basic authentication. |
| validate_certs  |  No  |  True  | | Evaluate SSL certificate (set to false for self-signed certificate). |
| vm_type  |  No  |  CDImage  | CDImage<br/> HDImage<br/>  | The virtual media type whose data are to be read. |

#### Examples
```yaml
# Get Virtual CD data
- block:
  - name: Get Virtual CD data
    irmc_getvm:
      irmc_url: "{{ inventory_hostname }}"
      irmc_username: "{{ irmc_user }}"
      irmc_password: "{{ irmc_password }}"
      validate_certs: "{{ validate_certificate }}"
      vm_type: CDImage
    register: cddata
    delegate_to: localhost
  - name: Show Virtual CD data
    debug:
      var: cddata.virtual_media_data
  tags:
    - getcd

# Get Virtual HD data
- block:
  - name: Get Virtual HD data
    irmc_getvm:
      irmc_url: "{{ inventory_hostname }}"
      irmc_username: "{{ irmc_user }}"
      irmc_password: "{{ irmc_password }}"
      validate_certs: "{{ validate_certificate }}"
      vm_type: HDImage
    register: hddata
    delegate_to: localhost
  - name: Show Virtual HD data
    debug:
      var: hddata.virtual_media_data
  tags:
    - gethd
```

#### Return Values

**virtual_media_data returned by requesting data for e.g. 'CDImage':**

| Name | Description | Returned | Type | Example |
|:-----|:------------|:---------|:-----|:--------|
| CDImage | state of image | always | string | Connected |
| bootmode | boot source override mode for the next boot | always | string | UEFI |
| bootoverride | boot override type | always | string | Once |
| bootsource | boot device override for next boot | always | string | BiosSetup |
| image_name | name of the virtual image | always | string | mybootimage.iso |
| server | remote server where the image is located | always | string | 192.168.2.1 |
| share_name | path on the remote server where the image is located | always | string | isoimages |
| share_type | share type (NFS or SMB) | always | string | NFS |
| usb_attach_mode | remote image attach mode | always | string | AutoAttach |
| user_domain | user domain for SMB share | always | string | local.net |
| user_name | user name for SM share | always | string | test |

---
### irmc_idled

#### Description
* Ansible module to get or set server ID LED via iRMC RedFish interface.
* Module Version V1.2.

#### Requirements
  * The module needs to run locally.
  * iRMC S4 needs FW >= 9.04, iRMC S5 needs FW >= 1.25.
  * Python >= 2.6
  * Python modules 'future', 'requests', 'urllib3'

#### Options

| Parameter | Required | Default | Choices | Description |
|:----------|:---------|:--------|:--------|:----------- |
| command  |  No  |  get  | get<br/> set<br/>  | Get or set server ID LED state. |
| irmc_password  |  Yes  |  | | Password for iRMC user for basic authentication. |
| irmc_url  |  Yes  |  | | IP address of the iRMC to be requested for data. |
| irmc_username  |  Yes  |  | | iRMC user for basic authentication. |
| state  |  No  |  | Off<br/> Lit<br/> Blinking<br/>  | Desired server ID LED state for command 'set', ignored otherwise. |
| validate_certs  |  No  |  True  | | Evaluate SSL certificate (set to false for self-signed certificate). |

#### Examples
```yaml
# Get server ID LED state
- name: Get ID LED state
  irmc_idled:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "get"
  register: idled
  delegate_to: localhost
- name: Show iRMC ID LED state
  debug:
    msg: "{{ idled.idled_state }}"

# Set server ID LED state
- name: Set server ID LED state
  irmc_idled:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "set"
    state: "Lit"
  delegate_to: localhost
```

#### Return Values

**For command "get":**

| Name | Description | Returned | Type | Example |
|:-----|:------------|:---------|:-----|:--------|
| idled_state | server ID LED state | always | string | Blinking |

**For command "set":**

Default return values

#### Notes

- See http://manuals.ts.fujitsu.com/file/13371/irmc-restful-spec-en.pdf
- See http://manuals.ts.fujitsu.com/file/13372/irmc-redfish-wp-en.pdf

---
### irmc_ldap

#### Description
* Ansible module to manage iRMC LDAP settings via iRMC remote scripting interface.
* Module Version V1.2.

#### Requirements
  * The module needs to run locally.
  * Python >= 2.6
  * Python modules 'future', 'requests', 'urllib3'

#### Options

| Parameter | Required | Default | Choices | Description |
|:----------|:---------|:--------|:--------|:----------- |
| alert_email_enabled  |  No  |  | | LDAP email alert enabled. |
| alert_table_refresh  |  No  |  | | LDAP alert table refresh in hours (0 = never). |
| always_use_ssl  |  No  |  | | Always use SSL login. |
| append_base_to_user_dn  |  No  |  | | Append base DN to principal user DN. |
| auth_type  |  No  |  | ServerView LDAP<br/> Standard LDAP<br/>  | Authorization type. |
| backup_port  |  No  |  | | Non-SL port of backup LDAP server. |
| backup_server  |  No  |  | | Backup LDAP server. |
| backup_ssl_port  |  No  |  | | SSL port of backup LDAP server. |
| base_dn  |  No  |  | | Base DN. |
| command  |  No  |  get  | get<br/> set<br/>  | Get or set iRMC LDAP data. |
| department_name  |  No  |  | | Department name. |
| directory_type  |  No  |  | MS Active Directory<br/> Novell eDirector<br/> Sun ePlanet<br/> OpenLDAP<br/> OpenDS / OpenDJ<br/>  | Directory server type. |
| domain_name  |  No  |  | | Domain name. |
| enabled  |  No  |  | | LDAP enabled. |
| enhanced_user_login  |  No  |  | | Enhanced user login. |
| group_dn  |  No  |  | | Groups directory as sub-tree from base DN. |
| irmc_password  |  Yes  |  | | Password for iRMC user for basic authentication. |
| irmc_url  |  Yes  |  | | IP address of the iRMC to be requested for data. |
| irmc_username  |  Yes  |  | | iRMC user for basic authentication. |
| ldap_password  |  No  |  | | LDAP user password. |
| ldap_user  |  No  |  | | LDAP user name. |
| local_login_disabled  |  No  |  | | Local login disabled. |
| primary_port  |  No  |  | | Non-SL port of primary LDAP server. |
| primary_server  |  No  |  | | Primary LDAP server. |
| primary_ssl_port  |  No  |  | | SSL port of primary LDAP server. |
| ssl_enabled  |  No  |  | | LDAP SSL enabled. |
| user_dn  |  No  |  | | Principal user DN. |
| user_login_filter  |  No  |  | | User login search filter. |
| user_search_context  |  No  |  | | User search context. |
| validate_certs  |  No  |  True  | | Evaluate SSL certificate (set to false for self-signed certificate). |

#### Examples
```yaml
# Get LDAP data
- name: Get LDAP data
  irmc_ldap:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "get"
  register: ldap
  delegate_to: localhost
- name: Show iRMC LDAP data
  debug:
    msg: "{{ ldap.ldap }}"

# Set LDAP data
- name: Set LDAP data
  irmc_ldap:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "set"
    ldap_user: "username"
    ldap_password: "password"
  delegate_to: localhost
```

#### Return Values

**ldap data returned by command "get":**

| Name | Description | Returned | Type | Example |
|:-----|:------------|:---------|:-----|:--------|
| alert_email_enabled | LDAP email alert enabled | always | bool | False |
| alert_table_refresh | LDAP alert table refresh in hours | always | string | 0 |
| always_use_ssl | always use SSL login | always | bool | False |
| append_base_to_user_dn | append base DN to principal user DN | always | bool | False |
| auth_type | authorization type | always | string | ServerView LDAP |
| backup_port | non-SL port of backup LDAP server | always | string | 389 |
| backup_server | backup LDAP server | always | string | ldap_backup.local |
| backup_ssl_port | SSL port of backup LDAP server | always | string | 636 |
| base_dn | base DN | always | string |  |
| department_name | department name | always | string | department |
| directory_type | directory server type | always | string | MS Active Directory |
| domain_name | domain name | always | string | domain.local |
| enabled | LDAP enabled | always | bool | True |
| enhanced_user_login | enhanced user login | always | string | False |
| group_dn | groups directory as sub-tree from base DN | always | string | ou=ldaptest |
| ldap_user | LDAP user name | always | string | Administrator |
| local_login_disabled | local login disabled | always | bool | False |
| primary_port | non-SL port of primary LDAP server | always | string | 389 |
| primary_server | primary LDAP server | always | string | ldap_primary.local |
| primary_ssl_port | SSL port of primary LDAP server | always | string | 636 |
| ssl_enabled | LDAP SSL enabled | always | bool | False |
| user_dn | principal user DN | always | string |  |
| user_login_filter | user login search filter | always | string | (&(objectclass=person)(cn=%s)) |
| user_search_context | user search context | always | string |  |

**For command "set":**

Default return values

#### Notes

- See http://manuals.ts.fujitsu.com/file/12563/wp-svs-irmc-remote-scripting-en.pdf
- See https://sp.ts.fujitsu.com/dmsp/Publications/public/dp-svs-configuration-space-values-en.pdf

---
### irmc_license

#### Description
* Ansible module to manage iRMC user accounts via iRMC remote scripting interface.
* Module Version V1.2.

#### Requirements
  * The module needs to run locally.
  * Python >= 2.6
  * Python modules 'future', 'requests', 'urllib3'

#### Options

| Parameter | Required | Default | Choices | Description |
|:----------|:---------|:--------|:--------|:----------- |
| command  |  No  |  get  | get<br/> set<br/>  | License key management to be executed. |
| irmc_password  |  Yes  |  | | Password for iRMC user for basic authentication. |
| irmc_url  |  Yes  |  | | IP address of the iRMC to be requested for data. |
| irmc_username  |  Yes  |  | | iRMC user for basic authentication. |
| license_key  |  No  |  | | iRMC license key to be set. |
| validate_certs  |  No  |  True  | | Evaluate SSL certificate (set to false for self-signed certificate). |

#### Examples
```yaml
# Get iRMC license key
- name: Get iRMC license key
  irmc_license:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "get"
  register: license
  delegate_to: localhost
- name: show certificates
  debug:
    msg: "{{ license.license_key }}"

# Set iRMC license key
- name: Set iRMC license key
  irmc_license:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "set"
    license_key: "{{ license_key }}"
  delegate_to: localhost
```

#### Return Values

**For command "get":**

| Name | Description | Returned | Type | Example |
|:-----|:------------|:---------|:-----|:--------|
| license_key | system-locked iRMC license key | always | string |  |

**For command "set":**

Default return values

#### Notes

- A license key which was read from an iRMC is 'system-locked'. It can imported to the same iRMC, but not to another iRMC.
- See http://manuals.ts.fujitsu.com/file/12563/wp-svs-irmc-remote-scripting-en.pdf
- See https://sp.ts.fujitsu.com/dmsp/Publications/public/dp-svs-configuration-space-values-en.pdf

---

### irmc_ntp

#### Description

* Ansible module to manage iRMC time options via iRMC remote scripting interface.
* Module Version V1.3.0.

#### Requirements

* The module needs to run locally.
* Python >= 3.10
* Python modules 'requests', 'urllib3'

#### Options

| Parameter | Required | Default | Choices | Description |
|:----------|:---------|:--------|:--------|:----------- |
| command  |  No  |  get  | get<br/> set<br/>  | NTP management to be executed. |
| irmc_password  |  Yes  |  | | Password for iRMC user for basic authentication. |
| irmc_url  |  Yes  |  | | IP address of the iRMC to be requested for data. |
| irmc_username  |  Yes  |  | | iRMC user for basic authentication. |
| ntp_server_primary  |  No  |  | | IP address (IPv4 or IPv6) or DNS name of primary NTP server. |
| ntp_server_secondary  |  No  |  | | IP address (IPv4 or IPv6) or DNS name of secondary NTP server. |
| rtc_mode  |  No  |  | local time<br/> UTC/GMT<br/>  | Defines how iRMC interprets the system's hardware RTC time. |
| time_mode  |  No  |  | System RTC<br/> NTP<br/> MMB NTP<br/>  | Defines how iRMC synchronizes its real-time clock (RTC). |
| time_zone_location  |  No  |  | | iRMC time zone (e.g. 'Europe/Berlin'; based on Linux 'tzdata'). |
| validate_certs  |  No  |  True  | | Evaluate SSL certificate (set to false for self-signed certificate). |

#### Examples

```yaml
# Get iRMC time settings
- block:
  - name: Get iRMC time settings
    irmc_ntp:
      irmc_url: "{{ inventory_hostname }}"
      irmc_username: "{{ irmc_user }}"
      irmc_password: "{{ irmc_password }}"
      validate_certs: "{{ validate_certificate }}"
      command: "get"
    register: time
    delegate_to: localhost
  - name: Show iRMC time settings
    debug:
      var: time.time_settings
  tags:
    - get

# Set iRMC time option(s)
- name: Set iRMC time option(s)
  irmc_ntp:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "set"
    time_mode: "System RTC"
    time_zone_location: "Asia/Tokyo"
    rtc_mode: "local time"
  delegate_to: localhost
  tags:
    - set
```

#### Return Values

**time_settings returned for command "get":**

| Name | Description | Returned | Type | Example |
|:-----|:------------|:---------|:-----|:--------|
| ntp_server_primary | primary NTP server | always | string | pool.ntp.org |
| ntp_server_secondary | secondary NTP server | always | string | pool.ntp.org |
| rtc_mode | Defines how iRMC interprets the system's hardware RTC time | always | string | local time |
| time_mode | Defines how iRMC synchronizes its real-time clock (RTC) | always | string | System RTC |
| time_zone_location | iRMC time zone | always | string | Europe/Berlin |

**For command "set":**

Default return values

---
### irmc_powerstate

#### Description
* Ansible module to get or set server power state via iRMC RedFish interface.
* Module Version V1.2.

#### Requirements
  * The module needs to run locally.
  * iRMC S4 needs FW >= 9.04, iRMC S5 needs FW >= 1.25.
  * Python >= 2.6
  * Python modules 'future', 'requests', 'urllib3'

#### Options

| Parameter | Required | Default | Choices | Description |
|:----------|:---------|:--------|:--------|:----------- |
| command  |  No  |  get  | get<br/> set<br/>  | Get or set server power state. |
| irmc_password  |  Yes  |  | | Password for iRMC user for basic authentication. |
| irmc_url  |  Yes  |  | | IP address of the iRMC to be requested for data. |
| irmc_username  |  Yes  |  | | iRMC user for basic authentication. |
| state  |  No  |  | PowerOn<br/> PowerOff<br/> PowerCycle<br/> GracefulPowerOff<br/> ImmediateReset<br/> GracefulReset<br/> PulseNmi<br/> PressPowerButton<br/>  | Desired server power state for command 'set', ignored otherwise. Options 'GracefulPowerOff' and ' GracefulReset' require ServerView Agents running on server. |
| validate_certs  |  No  |  True  | | Evaluate SSL certificate (set to false for self-signed certificate). |

#### Examples
```yaml
# Get server power state
- name: Get server power state
  irmc_powerstate:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "get"
  register: powerstate
  delegate_to: localhost
- name: Show server power state
  debug:
    msg: "{{ powerstate.power_state }}"

# set server power state
- name: set server power state
  irmc_powerstate:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "set"
    state: "PowerOn"
  delegate_to: localhost
```

#### Return Values

**For command "get":**

| Name | Description | Returned | Type | Example |
|:-----|:------------|:---------|:-----|:--------|
| power_state | server power state | always | string | On |

**For command "set":**

Default return values

#### Notes

- See http://manuals.ts.fujitsu.com/file/13371/irmc-restful-spec-en.pdf
- See http://manuals.ts.fujitsu.com/file/13372/irmc-redfish-wp-en.pdf

---
### irmc_profiles

#### Description
* Ansible module to configure the BIOS boot oder via iRMC.
* Using this module may force server into several reboots.
* See specification [iRMC RESTful API](http://manuals.ts.fujitsu.com/file/13371/irmc-restful-spec-en.pdf).
* Module Version V1.2.

#### Requirements
  * The module needs to run locally.
  * The PRIMERGY server needs to be at least a M2 model.
  * iRMC S4 needs FW >= 9.04, iRMC S5 needs FW >= 1.25.
  * Python >= 2.6
  * Python modules 'future', 'requests', 'urllib3'

#### Options

| Parameter | Required | Default | Choices | Description |
|:----------|:---------|:--------|:--------|:----------- |
| command  |  No  |  list  | list<br/> get<br/> create<br/> delete<br/> import<br/>  | How to handle iRMC profiles. |
| irmc_password  |  Yes  |  | | Password for iRMC user for basic authentication. |
| irmc_url  |  Yes  |  | | IP address of the iRMC to be requested for data. |
| irmc_username  |  Yes  |  | | iRMC user for basic authentication. |
| profile  |  No  |  | | Which iRMC profile to handle. Only relevant for 'get', 'create', 'delete'. |
| profile_json  |  No  |  | | Direct input of iRMC profile data. Only evaluated for command='import'. When set, 'profile_path' is ignored. |
| profile_path  |  No  |  | | Path file where to read a profile. Only evaluated for command='import'. Ignored when 'profile_json' is set. |
| validate_certs  |  No  |  True  | | Evaluate SSL certificate (set to false for self-signed certificate). |
| wait_for_finish  |  No  |  True  | | Wait for 'create profile' or 'import profile' session to finish. Ignored otherwise. |

#### Examples
```yaml
# List iRMC profiles
- name: List iRMC profiles
  irmc_profiles:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "list"
  delegate_to: localhost

# Get iRMC HWConfigurationIrmc profile
- name: Get iRMC HWConfigurationIrmc profile
  irmc_profiles:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "get"
    profile: "HWConfigurationIrmc"
  delegate_to: localhost
```

#### Return Values

**profiles returned for command "list":**

| Name | Description | Returned | Type | Example |
|:-----|:------------|:---------|:-----|:--------|
| <profile_name> | name of specific profile | always | dict | BiosBootOrder |
| <profile_name>.Location | RedFish location of profile | always | string | rest/v1/Oem/eLCM/ProfileManagement/BiosBootOrder |
| <profile_name>.Name | name of profile | always | string | BiosBootOrder |

**For all other commands:**

Default return values

**profile data returned for command "get":**

| Name | Description | Returned | Type | Example |
|:-----|:------------|:---------|:-----|:--------|
| profile | data of requested profile | always | dict |  |

#### Notes

- See http://manuals.ts.fujitsu.com/file/13371/irmc-restful-spec-en.pdf
- See http://manuals.ts.fujitsu.com/file/13372/irmc-redfish-wp-en.pdf

---
### irmc_raid

#### Description
* Ansible module to configure a PRIMERGY server's RAID via iRMC.
* Using this module may force the server into several reboots.
* See specification [iRMC RESTful API](http://manuals.ts.fujitsu.com/file/13371/irmc-restful-spec-en.pdf).
* Module Version V1.2.

#### Requirements
  * The module needs to run locally.
  * The PRIMERGY server needs to be at least a M2 model.
  * iRMC S4 needs FW >= 9.04, iRMC S5 needs FW >= 1.25.
  * Python >= 2.6
  * Python modules 'future', 'requests', 'urllib3'

#### Options

| Parameter | Required | Default | Choices | Description |
|:----------|:---------|:--------|:--------|:----------- |
| adapter  |  No  |  | | The logical number of the adapter to create/delete RAID arrays on/from. |
| array  |  No  |  | | The logical number of the RAID array to delete. Use -1 for all arrays. Ignored for 'create'. |
| command  |  No  |  get  | get<br/> create<br/> delete<br/>  | How to handle iRMC RAID. |
| irmc_password  |  Yes  |  | | Password for iRMC user for basic authentication. |
| irmc_url  |  Yes  |  | | IP address of the iRMC to be requested for data. |
| irmc_username  |  Yes  |  | | iRMC user for basic authentication. |
| level  |  No  |  | | Raid level of array to be created. Ignored for 'delete'. |
| name  |  No  |  | | Name of the array to be created. Ignored for 'delete'. |
| validate_certs  |  No  |  True  | | Evaluate SSL certificate (set to false for self-signed certificate). |
| wait_for_finish  |  No  |  True  | | Wait for raid session to finish. |

#### Examples
```yaml
# Get RAID configuration
- name: Get RAID configuration
  irmc_raid:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "get"
  register: raid
  delegate_to: localhost
- name: Show RAID configuration
  debug:
    msg: "{{ raid.configuration }}"

# Create RAID array
- name: Create RAID array
  irmc_raid:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "create"
    adapter: "{{ adapter }}"
    level: "{{ level }}"
    name: "{{ name }}"
  delegate_to: localhost

# Delete RAID array
- name: Delete RAID array
  irmc_raid:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "delete"
    adapter: "{{ adapter }}"
    array: "{{ array }}"
  delegate_to: localhost
```

#### Return Values

**data returned for command "get":**

| Name | Description | Returned | Type | Example |
|:-----|:------------|:---------|:-----|:--------|
| configuration | list of available RAID adapters with attached logical and physical disks | always | dict | [{u'raid_level': u'0,1,5,6,10,50,60', u'logical_drives': [{u'id': 0, u'disks': [{u'slot': 0, u'id': u'0', u'name': u'WDC WD5003ABYX-', u'size': u'465 GB'}, {u'slot': 1, u'id': u'1', u'name': u'WDC WD5003ABYX-', u'size': u'465 GB'}], u'raid_level': u'1', u'name': u'LogicalDrive_0'}, {u'id': 1, u'disks': [{u'slot': 2, u'id': u'2', u'name': u'WDC WD5003ABYX-', u'size': u'465 GB'}], u'raid_level': u'0', u'name': u'LogicalDrive_1'}], u'id': u'RAIDAdapter0', u'name': u'RAIDAdapter0', u'unused_disks': [{u'slot': 3, u'id': u'3', u'name': u'WDC WD5003ABYX-', u'size': u'465 GB'}]}] |

**For all commands:**

| Name | Description | Returned | Type | Example |
|:-----|:------------|:---------|:-----|:--------|
| log | detailed log data of RAID session | in case of error | dict | {u'SessionLog': {u'Tag': u'', u'WorkSequence': u'obtainProfileParameters', u'Id': 6, u'Entries': {u'Entry': [{u'@date': u'2018/11/09 09:39:19', u'#text': u"CreateSession: Session 'obtainProfile' created with id 6"}, {u'@date': u'2018/11/09 09:39:19', u'#text': u"AttachWorkSequence: Attached work sequence 'obtainProfileParameters' to session 6"}, {u'@date': u'2018/11/09 09:39:45', u'#text': u"ObtainProfileParameters: Finished processing of profile path 'Server/HWConfigurationIrmc/Adapters/RAIDAdapter' with status 'Error'"}, {u'@date': u'2018/11/09 09:39:45', u'#text': u"TerminateSession: 'obtainProfileParameters' is being terminated"}]}}} |

#### Notes

- See http://manuals.ts.fujitsu.com/file/13371/irmc-restful-spec-en.pdf
- See http://manuals.ts.fujitsu.com/file/13372/irmc-redfish-wp-en.pdf

---
### irmc_scci

#### Description
* Ansible module to execute iRMC Remote Scripting (SCCI) commands.
* Module Version V1.3.0.

#### Requirements
  * The module needs to run locally.
  * iRMC S6.
  * Python >= 3.10
  * Python modules 'requests', 'urllib3'

#### Options

| Parameter | Required | Default | Choices | Description |
|:----------|:---------|:--------|:--------|:----------- |
| cabid  |  No  |  -1 (main cabinet)  | | SCCI cabinet ID. |
| command  |  Yes  |  | get_cs            (ConfigSpace Read)<br/> set_cs            (ConfigSpace Write)<br/> power_on          (Power-On the Server)<br/> power_off         (Power-Off the Server)<br/> power_cycle       (Power Cycle the Server)<br/> reset             (Hard Reset the Server)<br/> nmi               (Pulse the NMI (Non Maskable Interrupt))<br/> graceful_shutdown (Graceful Shutdown, requires running Agent)<br/> graceful_reboot   (Graceful Reboot, requires running Agent)<br/> cancel_shutdown   (Cancel a Shutdown Request)<br/> reset_firmware    (Perform a BMC Reset)<br/>   | SCCI remote scripting command. |
| data  |  No  |  | | Data for commands which require data, ignored otherwise. |
| index  |  No  |  | | SCCI index. |
| irmc_password  |  Yes  |  | | Password for iRMC user for basic authentication. |
| irmc_url  |  Yes  |  | | IP address of the iRMC to be requested for data. |
| irmc_username  |  Yes  |  | | iRMC user for basic authentication. |
| opcodeext  |  No  |  | | SCCI opcode extension. |
| validate_certs  |  No  |  True  | | Evaluate SSL certificate (set to false for self-signed certificate). |

#### Examples
```yaml
# Write server location
- name: Write server location
  irmc_scci:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "set_cs"
    opcodeext: 0x200
    data: "In a galaxy far, far away ..."
  delegate_to: localhost
  tags:
    - write

# Read server location
- block:
  - name: "Read server location"
    irmc_scci:
      irmc_url: "{{ inventory_hostname }}"
      irmc_username: "{{ irmc_user }}"
      irmc_password: "{{ irmc_password }}"
      validate_certs: "{{ validate_certificate }}"
      command: "get_cs"
      opcodeext: 0x200
    register: read_result
    delegate_to: localhost
  - name: Show server location
    debug:
      var: read_result.data
  tags:
    - read

# Power on the server
- name: "Power on the server"
  irmc_scci:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "power_on"
    opcodeext: 0x200
  delegate_to: localhost
  tags:
    - poweron

# Power off the server
- name: "Power off the server"
  irmc_scci:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "power_off"
    opcodeext: 0x200
  delegate_to: localhost
  tags:
    - poweroff

# Cancel shutdown
- name: "Cancel shutdown"
  irmc_scci:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "cancel_shutdown"
    opcodeext: 0x200
  delegate_to: localhost
  tags:
    - cancel_shutdown

# Reset firmware
- name: "Reset firmware"
  irmc_scci:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "reset_firmware"
    opcodeext: 0x200
  delegate_to: localhost
  tags:
    - reset_firm
```

#### Return Values

**For command "get_cs":**

| Name | Description | Returned | Type | Example |
|:-----|:------------|:---------|:-----|:--------|
| data | result of requested SCCI command | always | string | In a galaxy far, far away ... |

**For all other commands:**

Default return values

---
### irmc_session

#### Description

* Ansible module to handle iRMC sessions via Restful API.
* Module Version V1.3.0.

#### Requirements

* The module needs to run locally.
* iRMC S6
* Python >= 3.10
* Python modules 'requests', 'urllib3'

#### Options

| Parameter | Required | Default | Choices | Description |
|:----------|:---------|:--------|:--------|:----------- |
| command  |  No  |  list  | list<br/> get<br/> remove<br/> terminate<br/> clearall<br/>  | Handle iRMC sessions. |
| id  |  No  |  | | Specific session to get, remove or terminate. |
| irmc_password  |  Yes  |  | | Password for iRMC user for basic authentication. |
| irmc_url  |  Yes  |  | | IP address of the iRMC to be requested for data. |
| irmc_username  |  Yes  |  | | iRMC user for basic authentication. |
| validate_certs  |  No  |  True  | | Evaluate SSL certificate (set to false for self-signed certificate). |

#### Examples

```yaml
# List iRMC sessions
- name: Get and show iRMC sessions
  tags:
    - list
  block:
    - name: List iRMC sessions
      irmc_session:
        irmc_url: "{{ inventory_hostname }}"
        irmc_username: "{{ irmc_user }}"
        irmc_password: "{{ irmc_password }}"
        validate_certs: "{{ validate_certificate }}"
        command: "list"
      delegate_to: localhost
      register: result
    - name: Show iRMC sessions details
      ansible.builtin.debug:
        var: result.sessions

# Get specific session information
- name: Get specific session information
  tags:
    - get
  block:
    - name: Get specific session information
      irmc_session:
        irmc_url: "{{ inventory_hostname }}"
        irmc_username: "{{ irmc_user }}"
        irmc_password: "{{ irmc_password }}"
        validate_certs: "{{ validate_certificate }}"
        command: "get"
        id: "{{ session_id | int }}"
      delegate_to: localhost
      register: result
    - name: Show specific session information
      ansible.builtin.debug:
        var: result

# Remove specific session information
- name: Remove specific session information
  tags:
    - remove
  block:
    - name: Remove specific session information
      irmc_session:
        irmc_url: "{{ inventory_hostname }}"
        irmc_username: "{{ irmc_user }}"
        irmc_password: "{{ irmc_password }}"
        validate_certs: "{{ validate_certificate }}"
        command: "remove"
        id: "{{ session_id | int }}"
      delegate_to: localhost
      register: result
    - name: Show result of remove session
      ansible.builtin.debug:
        var: result

# Clear all sessions information
- name: Clear all sessions information
  irmc_session:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "clearall"
  delegate_to: localhost
  register: result
  tags:
    - clearall

# Terminate specific session
- name: Terminate specific session
  irmc_session:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "terminate"
    id: "{{ session_id | int }}"
  delegate_to: localhost
  register: result
  tags:
    - terminate
```

#### Return Values

**data for sessions returned for command "list":**

| Name | Description | Returned | Type | Example |
|:-----|:------------|:---------|:-----|:--------|
| Duration | Session duration in seconds | always | int | 226 |
| Id | session ID | always | int | 4 |
| Start | work sequence | always | string | 2018/07/31 12:09:25 |
| Status | session status | always | string | terminated regularly |
| Tag | session tag | always | string |  |
| Text | work sequence | always | string | offlineUpdatePrepare |

**session_log.SessionLog data returned for command "get":**

| Name | Description | Returned | Type | Example |
|:-----|:------------|:---------|:-----|:--------|
| session_log.SessionLog.Entries.Entry | list of individual session log entries | always | list |  |
| session_log.SessionLog.Id | Session ID | always | int | 4 |
| session_log.SessionLog.Tag | session tag | always | string |  |
| session_log.SessionLog.WorkSequence | work sequence | always | string | prepareOfflineUpdate |
| session_status | session status | always | string | terminated regularly |

**For all other commands:**

Default return values

---
### irmc_setnextboot

#### Description
* Ansible module to configure iRMC to force next boot to specified option.
* Module Version V1.2.

#### Requirements
  * The module needs to run locally.
  * iRMC S4 needs FW >= 9.04, iRMC S5 needs FW >= 1.25.
  * Python >= 2.6
  * Python modules 'future', 'requests', 'urllib3'

#### Options

| Parameter | Required | Default | Choices | Description |
|:----------|:---------|:--------|:--------|:----------- |
| bootmode  |  No  |  | Legacy<br/> UEFI<br/>  | The mode for the next boot. |
| bootoverride  |  No  |  Once  | Once<br/> Continuous<br/>  | Boot override type. |
| bootsource  |  No  |  BiosSetup  | None<br/> Pxe<br/> Floppy<br/> Cd<br/> Hdd<br/> BiosSetup<br/>  | The source for the next boot. |
| irmc_password  |  Yes  |  | | Password for iRMC user for basic authentication. |
| irmc_url  |  Yes  |  | | IP address of the iRMC to be requested for data. |
| irmc_username  |  Yes  |  | | iRMC user for basic authentication. |
| validate_certs  |  No  |  True  | | Evaluate SSL certificate (set to false for self-signed certificate). |

#### Examples
```yaml
# Set Bios to next boot from Virtual CD
# Note: boot from virtual CD might fail, if a 'real' DVD drive exists
- name: Set Bios to next boot from Virtual CD
  irmc_setnextboot:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    bootsource: "Cd"
    bootoverride: "Once"
    bootmode: "Legacy"
  delegate_to: localhost
```

#### Return Values

Default return values

#### Notes

- See http://manuals.ts.fujitsu.com/file/13371/irmc-restful-spec-en.pdf
- See http://manuals.ts.fujitsu.com/file/13372/irmc-redfish-wp-en.pdf

---
### irmc_setvm

#### Description
* Ansible module to set iRMC Virtual Media Data via iRMC RedFish interface.
* Module Version V1.3.0.

#### Requirements
  * The module needs to run locally.
  * iRMC S6.
  * Python >= 3.10
  * Python modules 'requests', 'urllib3'

#### Options

| Parameter | Required | Default | Choices | Description |
|:----------|:---------|:--------|:--------|:----------- |
| force_mediatype_active  |  No  |  | | Forces iRMC to activate one of the required remote media types. |
| force_remotemount_enabled  |  No  |  | | Forces iRMC to enable the remote mount feature. |
| image  |  Yes  |  | | Name of the remote image. |
| irmc_password  |  Yes  |  | | Password for iRMC user for basic authentication. |
| irmc_url  |  Yes  |  | | IP address of the iRMC to be requested for data. |
| irmc_username  |  Yes  |  | | iRMC user for basic authentication. |
| server  |  Yes  |  | | Remote server (IP or DNS name) where the image is located. |
| share  |  Yes  |  | | Path on the remote server where the image is located. |
| share_type  |  No  |  | NFS<br/> SMB<br/>  | Share type (NFS share or SMB share). |
| validate_certs  |  No  |  True  | | Evaluate SSL certificate (set to false for self-signed certificate). |
| vm_domain  |  No  |  | | User domain in case of SMB share. |
| vm_password  |  No  |  | | User password in case of SMB share. |
| vm_type  |  No  |  CDImage  | CDImage<br/> HDImage<br/>  | The virtual media type to be set. |
| vm_user  |  No  |  | | User account in case of SMB share. |

#### Examples
```yaml
# Set Virtual CD
- name: Set Virtual CD
  irmc_setvm:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    share_type: "{{ share_type }}"
    server: "{{ server }}"
    share: "{{ share }}"
    image: "{{ image }}"
    vm_user: "{{ vm_user }}"
    vm_password: "{{ vm_password }}"
    vm_type: "CDImage"
  delegate_to: localhost
  tags:
    - setcd

# Set Virtual HD
- name: Set Virtual HD
  irmc_setvm:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    share_type: "{{ share_type }}"
    server: "{{ server }}"
    share: "{{ share }}"
    image: "{{ image }}"
    vm_user: "{{ vm_user }}"
    vm_password: "{{ vm_password }}"
    vm_type: "HDImage"
  delegate_to: localhost
  tags:
    - sethd
```

#### Return Values

Default return values

---
### irmc_task

#### Description
* Ansible module to handle iRMC tasks via Restful API.
* Module Version V1.2.

#### Requirements
  * The module needs to run locally.
  * iRMC S4 needs FW >= 9.04, iRMC S5 needs FW >= 1.25.
  * Python >= 2.6
  * Python modules 'future', 'requests', 'urllib3'

#### Options

| Parameter | Required | Default | Choices | Description |
|:----------|:---------|:--------|:--------|:----------- |
| command  |  No  |  list  | list<br/> get<br/>  | Handle iRMC tasks. |
| id  |  No  |  | | Specific task to get. |
| irmc_password  |  Yes  |  | | Password for iRMC user for basic authentication. |
| irmc_url  |  Yes  |  | | IP address of the iRMC to be requested for data. |
| irmc_username  |  Yes  |  | | iRMC user for basic authentication. |
| validate_certs  |  No  |  True  | | Evaluate SSL certificate (set to false for self-signed certificate). |

#### Examples
```yaml
# List iRMC tasks
- name: List iRMC tasks
  irmc_task:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "list"
  delegate_to: localhost

# Get specific task information
- name: Get specific task information
  irmc_task:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "get"
    id: 3
  delegate_to: localhost
```

#### Return Values

**task data returned for command "get":**

| Name | Description | Returned | Type | Example |
|:-----|:------------|:---------|:-----|:--------|
| EndTime | end time | always | string | 2018-07-31 12:26:44 |
| Id | task ID | always | int | 3 |
| Name | task name | always | string | ProfileParametersApply |
| StartTime | start time | always | string | 2018-07-31 12:23:02 |
| State | task state | always | string | Completed |
| StateOem | Oem task state | always | string | LcmSessFinished |
| StateProgressPercent | state progress in % | always | string | 100 |
| TotalProgressPercent | overall progress in % | always | string | 100 |

**tasks data returned for command "list":**

List of individual task entries (see above)

#### Notes

- See http://manuals.ts.fujitsu.com/file/13371/irmc-restful-spec-en.pdf
- See http://manuals.ts.fujitsu.com/file/13372/irmc-redfish-wp-en.pdf

---
### irmc_user

#### Description
* Ansible module to manage iRMC user accounts via iRMC remote scripting interface.
* Module Version V1.2.

#### Requirements
  * The module needs to run locally.
  * Python >= 2.6
  * Python modules 'future', 'requests', 'urllib3'

#### Options

| Parameter | Required | Default | Choices | Description |
|:----------|:---------|:--------|:--------|:----------- |
| alert_fans  |  No  |  | None<br/> Critical<br/> Warning<br/> All<br/>  | Define alert level for fan sensors. |
| alert_hderrors  |  No  |  | None<br/> Critical<br/> Warning<br/> All<br/>  | Define alert level for disk drivers & controllers. |
| alert_hwerrors  |  No  |  | None<br/> Critical<br/> Warning<br/> All<br/>  | Define alert level for critical hardware errors. |
| alert_memory  |  No  |  | None<br/> Critical<br/> Warning<br/> All<br/>  | Define alert level for memory. |
| alert_network  |  No  |  | None<br/> Critical<br/> Warning<br/> All<br/>  | Define alert level for network interface. |
| alert_others  |  No  |  | None<br/> Critical<br/> Warning<br/> All<br/>  | Define alert level for other. |
| alert_posterrors  |  No  |  | None<br/> Critical<br/> Warning<br/> All<br/>  | Define alert level for POST errors. |
| alert_power  |  No  |  | None<br/> Critical<br/> Warning<br/> All<br/>  | Define alert level for system power. |
| alert_remote  |  No  |  | None<br/> Critical<br/> Warning<br/> All<br/>  | Define alert level for remote management. |
| alert_security  |  No  |  | None<br/> Critical<br/> Warning<br/> All<br/>  | Define alert level for security. |
| alert_syshang  |  No  |  | None<br/> Critical<br/> Warning<br/> All<br/>  | Define alert level for system hang. |
| alert_sysstatus  |  No  |  | None<br/> Critical<br/> Warning<br/> All<br/>  | Define alert level for system status. |
| alert_temperatures  |  No  |  | None<br/> Critical<br/> Warning<br/> All<br/>  | Define alert level for temperature sensors. |
| avr_enabled  |  No  |  | | User may use Advanved Video Redirection (AVR) |
| command  |  No  |  get  | get<br/> create<br/> change<br/> delete<br/>  | User management to be executed. |
| config_bmc_enabled  |  No  |  | | User may configure iRMC settings. |
| config_user_enabled  |  No  |  | | User may configure user accounts. |
| description  |  No  |  | | User account desciption. |
| email_address  |  No  |  | | Alert email address. |
| email_enabled  |  No  |  | | Alert email enabled. |
| email_encrypted  |  No  |  | | Alert email is encrypted. |
| email_server  |  No  |  | Automatic<br/> Primary<br/> Secondary<br/>  | Preferred mail server for alert email. |
| email_type  |  No  |  | Standard<br/> ITS-Format<br/> REMCS<br/> Fixed Subject<br/> SMS<br/>  | Alert email format. |
| enabled  |  No  |  | | User account enabled. |
| irmc_password  |  Yes  |  | | Password for iRMC user for basic authentication. |
| irmc_url  |  Yes  |  | | IP address of the iRMC to be requested for data. |
| irmc_username  |  Yes  |  | | iRMC user for basic authentication. |
| lan_privilege  |  No  |  | Reserved<br/> Callback<br/> User<br/> Operator<br/> Administrator<br/> OEM<br/> NoAccess<br/>  | IPMI LAN channel privilege. |
| name  |  Yes  |  | | User account name. |
| password  |  No  |  | | User account password. |
| redfish_enabled  |  No  |  | | User may use iRMC Redfish interface. |
| redfish_role  |  No  |  | NoAccess<br/> Operator<br/> Administrator<br/> ReadOnly<br/>  | User account Redfish role. |
| serial_privilege  |  No  |  | Reserved<br/> Callback<br/> User<br/> Operator<br/> Administrator<br/> OEM<br/> NoAccess<br/>  | IPMI serial channel privilege. |
| shell  |  No  |  | SMASH CLP<br/> CLI<br/> Remote Manager<br/> IPMI basic mode<br/> IPMI terminal mode<br/> None<br/>  | User text access type. |
| snmpv3_access  |  No  |  | ReadOnly<br/> ReadWrite<br/> Other<br/>  | User account SNMPV3 access privilege. |
| snmpv3_auth  |  No  |  | Undefined<br/> SHA<br/> MD5<br/> None<br/>  | User account SNMPv3 authentication. |
| snmpv3_enabled  |  No  |  | | User may use SNMPv3. |
| snmpv3_privacy  |  No  |  | Undefined<br/> AES<br/> DES<br/> None<br/>  | User account SNMPv3 privacy type. |
| ssh_certificate  |  No  |  | | User account SSH certificate. |
| ssh_public_key  |  No  |  | | user account SSH public key. |
| storage_enabled  |  No  |  | | User may use Remote Storage. |
| validate_certs  |  No  |  True  | | Evaluate SSL certificate (set to false for self-signed certificate). |

#### Examples
```yaml
# Create new user account
- name: "Create new user account"
  irmc_user:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "create"
    name: "ansibleuser"
    password: "password"
  delegate_to: localhost

# Get user account data
- name: Get user account data
  irmc_user:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "get"
    name: "ansibleuser"
  register: user
  delegate_to: localhost
- name: Show iRMC user details
  debug:
    msg: "{{ user.user }}"

# Change user account data
- name: Change user account data
  irmc_user:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "change"
    name: "ansibleuser"
    description: "ansible user description"
  delegate_to: localhost

# Delete user account
- name: "Delete user account"
  irmc_user:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "delete"
    name: "ansibleuser"
  delegate_to: localhost
```

#### Return Values

**user data returned for command "get":**

| Name | Description | Returned | Type | Example |
|:-----|:------------|:---------|:-----|:--------|
| alert_fans | alert level for fan sensors | always | string | Warning |
| alert_hderrors | alert level for disk drivers & controllers | always | string | Critical |
| alert_hwerrors | alert level for critical hardware errors | always | string | All |
| alert_memory | alert level for memory | always | string | Critical |
| alert_network | alert level for network interface | always | string | Warning |
| alert_others | alert level for other | always | string | None |
| alert_posterrors | alert level for POST errors | always | string | All |
| alert_power | alert level for system power | always | string | Warning |
| alert_remote | alert level for remote management | always | string | Critical |
| alert_security | alert level for security | always | string | Warning |
| alert_syshang | alert level for system hang | always | string | Critical |
| alert_sysstatus | alert level for system status | always | string | None |
| alert_temperatures | alert level for temperature sensors | always | string | Warning |
| avr_enabled | user may use Advanved Video Redirection (AVR) | always | bool | True |
| config_bmc_enabled | user may configure iRMC settings | always | bool | True |
| config_user_enabled | user may configure user accounts | always | bool | True |
| description | user account desciption | always | string | Admin User |
| email_address | alert email address | always | string | admin@irmc.local |
| email_enabled | alert email enabled | always | bool | False |
| email_encrypted | alert email is encrypted | always | bool | False |
| email_server | preferred mail server for alert email | always | string | Automatic |
| email_type | alert email format | always | string | Standard |
| enabled | user account enabled | always | bool | True |
| id | user ID | always | int | 0 |
| lan_privilege | IPMI LAN channel privilege | always | string | Administrator |
| name | user account name | always | string | admin |
| redfish_enabled | user may use iRMC Redfish interface | always | bool | True |
| redfish_role | user account Redfish role | always | string | Administrator |
| serial_privilege | IPMI serial channel privilege | always | string | Administrator |
| shell | user text access type | always | string | Remote Manager |
| snmpv3_access | user account SNMPV3 access privilege | always | string | ReadOnly |
| snmpv3_auth | user account SNMPv3 authentication | always | string | SHA |
| snmpv3_enabled | user may use SNMPv3 | always | bool | False |
| snmpv3_privacy | user account SNMPv3 privacy type | always | string | DES |
| ssh_certificate | user account SSH certificate | always | string |  |
| ssh_public_key | user account SSH public key | always | string |  |
| storage_enabled | user may use Remote Storage | always | bool | True |

**For all other commands:**

Default return values

#### Notes

- See http://manuals.ts.fujitsu.com/file/12563/wp-svs-irmc-remote-scripting-en.pdf
- See https://sp.ts.fujitsu.com/dmsp/Publications/public/dp-svs-configuration-space-values-en.pdf

---
---
Fsas Technologies Inc.  
Copyright 2018-2024 Fsas Technologies Inc.

GNU General Public License v3.0+ (see [LICENSE.md](LICENSE.md) or https://www.gnu.org/licenses/gpl-3.0.txt)


