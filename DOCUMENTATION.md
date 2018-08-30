# Fujitsu PRIMERGY iRMC modules

## Modules

  * [irmc_certificate - manage iRMC certificates](#irmc_certificate)
  * [irmc_connectvm - connect iRMC Virtual Media Data](#irmc_connectvm)
  * [irmc_facts - get or set PRIMERGY server and iRMC facts](#irmc_facts)
  * [irmc_getvm - get iRMC Virtual Media Data](#irmc_getvm)
  * [irmc_idled - get or set server ID LED](#irmc_idled)
  * [irmc_ldap - manage iRMC LDAP settings](#irmc_ldap)
  * [irmc_license - manage iRMC user accounts](#irmc_license)
  * [irmc_powerstate - get or set server power state](#irmc_powerstate)
  * [irmc_scci - execute iRMC remote SCCI commands](#irmc_scci)
  * [irmc_setnextboot - configure iRMC to force next boot to specified option](#irmc_setnextboot)
  * [irmc_setvm - set iRMC Virtual Media Data](#irmc_setvm)
  * [irmc_user - manage iRMC user accounts](#irmc_user)

---
### irmc_certificate


#### Description
* Ansible module to manage iRMC certificates via iRMC remote scripting interface.
* Module Version V1.0.1.

#### Requirements
  * The module needs to run locally.
  * python >= 2.6

#### Options

| Parameter | Required | Default | Choices | Description |
|:----------|:---------|:--------|:--------|:----------- |
| command  |  No  |  get  | <ul><li>get</li><li>set</li></ul>  | get or set iRMC certificate(s) |
| irmc_password  |  Yes  |  | | password for iRMC user for basic authentication |
| irmc_url  |  Yes  |  | | IP address of the iRMC to be requested for data |
| irmc_username  |  Yes  |  | | iRMC user for basic authentication |
| private_key_path  |  No  |  | | path to file containing SSL private key; this option also requires the SSL certificate |
| ssl_ca_cert_path  |  No  |  | | path to file containing SSL CA certificate |
| ssl_cert_path  |  No  |  | | path to file containing SSL certificate; this option also requires the SSL private key |
| validate_certs  |  No  |  True  | | evaluate SSL certificate (set to false for self-signed certificate) |

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

| Name | Description | Returned | Type |
|:-----|:------------|:---------|:-----|
| certificates   | SSL certificates |  always |  dict |

#### Notes

- See http://manuals.ts.fujitsu.com/file/12563/wp-svs-irmc-remote-scripting-en.pdf
- See https://sp.ts.fujitsu.com/dmsp/Publications/public/dp-svs-configuration-space-values-en.pdf

---
### irmc_connectvm


#### Description
* Ansible module to connect iRMC Virtual Media Data via the iRMC RedFish interface.
* Module Version V1.0.1.

#### Requirements
  * The module needs to run locally.
  * iRMC S4 needs FW >= 9.04, iRMC S5 needs FW >= 1.25.
  * python >= 2.6

#### Options

| Parameter | Required | Default | Choices | Description |
|:----------|:---------|:--------|:--------|:----------- |
| command  |  No  |  ConnectCD  | <ul><li>ConnectCD</li><li>ConnectFD</li><li>ConnectHD</li><li>DisconnectCD</li><li>DisconnectFD</li><li>DisconnectHD</li></ul>  | the virtual media connect command to be executed |
| irmc_password  |  Yes  |  | | password for iRMC user for basic authentication |
| irmc_url  |  Yes  |  | | IP address of the iRMC to be requested for data |
| irmc_username  |  Yes  |  | | iRMC user for basic authentication |
| validate_certs  |  No  |  True  | | evaluate SSL certificate (set to false for self-signed certificate) |

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

# Connect Virtual CD
- name: Connect Virtual CD
  irmc_connectvm:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "ConnectCD"
  delegate_to: localhost
```

#### Return Values

| Name | Description | Returned | Type |
|:-----|:------------|:---------|:-----|
| result   | connection action result |  always |  dict |

#### Notes

- See http://manuals.ts.fujitsu.com/file/13371/irmc-restful-spec-en.pdf
- See http://manuals.ts.fujitsu.com/file/13372/irmc-redfish-wp-en.pdf

---
### irmc_facts


#### Description
* Ansible module to get or set basic iRMC and PRIMERGY server data via iRMC RedFish interface.
* Module Version V1.0.1.

#### Requirements
  * The module needs to run locally.
  * iRMC S4 needs FW >= 9.04, iRMC S5 needs FW >= 1.25.
  * python >= 2.6

#### Options

| Parameter | Required | Default | Choices | Description |
|:----------|:---------|:--------|:--------|:----------- |
| asset_tag  |  No  |  | | server asset tag |
| command  |  No  |  get  | <ul><li>get</li><li>set</li></ul>  | get or set server facts |
| description  |  No  |  | | server description |
| helpdesk_message  |  No  |  | | help desk message |
| irmc_password  |  Yes  |  | | password for iRMC user for basic authentication |
| irmc_url  |  Yes  |  | | IP address of the iRMC to be requested for data |
| irmc_username  |  Yes  |  | | iRMC user for basic authentication |
| location  |  No  |  | | server location |
| validate_certs  |  No  |  True  | | evaluate SSL certificate (set to false for self-signed certificate) |

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

| Name | Description | Returned | Type |
|:-----|:------------|:---------|:-----|
| facts   | basic server and iRMC facts |  always |  dict |

#### Notes

- See http://manuals.ts.fujitsu.com/file/13371/irmc-restful-spec-en.pdf
- See http://manuals.ts.fujitsu.com/file/13372/irmc-redfish-wp-en.pdf

---
### irmc_getvm


#### Description
* Ansible module to get iRMC Virtual Media Data via iRMC RedFish interface.
* Module Version V1.0.1.

#### Requirements
  * The module needs to run locally.
  * iRMC S4 needs FW >= 9.04, iRMC S5 needs FW >= 1.25.
  * python >= 2.6

#### Options

| Parameter | Required | Default | Choices | Description |
|:----------|:---------|:--------|:--------|:----------- |
| irmc_password  |  Yes  |  | | password for iRMC user for basic authentication |
| irmc_url  |  Yes  |  | | IP address of the iRMC to be requested for data |
| irmc_username  |  Yes  |  | | iRMC user for basic authentication |
| validate_certs  |  No  |  True  | | evaluate SSL certificate (set to false for self-signed certificate) |
| vm_type  |  No  |  CDImage  | <ul><li>CDImage</li><li>FDImage</li><li>HDImage</li></ul>  | the virtual media type whose data are to be read |

#### Examples
```yaml
# Get Virtual Media data
- name: Get Virtual Media data
  irmc_getvm:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    vm_type: CDImage
  register: vmdata
  delegate_to: localhost
- name: Show Virtual Media data
  debug:
    msg: "{{ vmdata.virtual_media_data }}"
```

#### Return Values

| Name | Description | Returned | Type |
|:-----|:------------|:---------|:-----|
| virtual_media_data   | iRMC Virtual Media data |  always |  dict |

#### Notes

- See http://manuals.ts.fujitsu.com/file/13371/irmc-restful-spec-en.pdf
- See http://manuals.ts.fujitsu.com/file/13372/irmc-redfish-wp-en.pdf

---
### irmc_idled


#### Description
* Ansible module to get or set server ID LED via iRMC RedFish interface.
* Module Version V1.0.1.

#### Requirements
  * The module needs to run locally.
  * iRMC S4 needs FW >= 9.04, iRMC S5 needs FW >= 1.25.
  * python >= 2.6

#### Options

| Parameter | Required | Default | Choices | Description |
|:----------|:---------|:--------|:--------|:----------- |
| command  |  No  |  get  | <ul><li>get</li><li>set</li></ul>  | get or set server ID LED state |
| irmc_password  |  Yes  |  | | password for iRMC user for basic authentication |
| irmc_url  |  Yes  |  | | IP address of the iRMC to be requested for data |
| irmc_username  |  Yes  |  | | iRMC user for basic authentication |
| state  |  No  |  | <ul><li>Off</li><li>Lit</li><li>Blinking</li></ul>  | desired server ID LED state for command 'set', ignored otherwise |
| validate_certs  |  No  |  True  | | evaluate SSL certificate (set to false for self-signed certificate) |

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

| Name | Description | Returned | Type |
|:-----|:------------|:---------|:-----|
| idled_state   | server ID LED state |  always |  str |

#### Notes

- See http://manuals.ts.fujitsu.com/file/13371/irmc-restful-spec-en.pdf
- See http://manuals.ts.fujitsu.com/file/13372/irmc-redfish-wp-en.pdf

---
### irmc_ldap


#### Description
* Ansible module to manage iRMC LDAP settings via iRMC remote scripting interface.
* Module Version V1.0.1.

#### Requirements
  * The module needs to run locally.
  * python >= 2.6

#### Options

| Parameter | Required | Default | Choices | Description |
|:----------|:---------|:--------|:--------|:----------- |
| alert_email_enabled  |  No  |  | | LDAP email alert enabled |
| alert_table_refresh  |  No  |  | | LDAP alert table refresh in hours (0 = never) |
| always_use_ssl  |  No  |  | | always use SSL login |
| append_base_to_user_dn  |  No  |  | | append base DN to principal user DN |
| auth_type  |  No  |  | <ul><li>Automatic</li><li>Settings stored on iRMC</li><li>Settings stored on LDAP</li></ul>  | authorization type |
| backup_port  |  No  |  | | non-SL port of backup LDAP server |
| backup_server  |  No  |  | | backup LDAP server |
| backup_ssl_port  |  No  |  | | SSL port of backup LDAP server |
| base_dn  |  No  |  | | base DN |
| command  |  No  |  get  | <ul><li>get</li><li>set</li></ul>  | get or set iRMC LDAP data |
| department_name  |  No  |  | | department name |
| directory_type  |  No  |  | <ul><li>MS Active Directory</li><li>Novell eDirector</li><li>Sun ePlanet</li><li>OpenLDAP</li><li>OpenDS / OpenDJ</li></ul>  | directory server type |
| domain_name  |  No  |  | | domain name |
| enabled  |  No  |  | | LDAP enabled |
| enhanced_user_login  |  No  |  | | enhanced user login |
| group_dn  |  No  |  | | groups directory as sub-tree from base DN |
| irmc_password  |  Yes  |  | | password for iRMC user for basic authentication |
| irmc_url  |  Yes  |  | | IP address of the iRMC to be requested for data |
| irmc_username  |  Yes  |  | | iRMC user for basic authentication |
| ldap_password  |  No  |  | | LDAP user password |
| ldap_user  |  No  |  | | LDAP user name |
| local_login_disabled  |  No  |  | | local login disabled |
| primary_port  |  No  |  | | non-SL port of primary LDAP server |
| primary_server  |  No  |  | | primary LDAP server |
| primary_ssl_port  |  No  |  | | SSL port of primary LDAP server |
| ssl_enabled  |  No  |  | | LDAP SSL enabled |
| user_dn  |  No  |  | | principal user DN |
| user_login_filter  |  No  |  | | user login search filter |
| user_search_context  |  No  |  | | user search context |
| validate_certs  |  No  |  True  | | evaluate SSL certificate (set to false for self-signed certificate) |

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

| Name | Description | Returned | Type |
|:-----|:------------|:---------|:-----|
| ldap   | LDAP information |  always |  dict |

#### Notes

- See http://manuals.ts.fujitsu.com/file/12563/wp-svs-irmc-remote-scripting-en.pdf
- See https://sp.ts.fujitsu.com/dmsp/Publications/public/dp-svs-configuration-space-values-en.pdf

---
### irmc_license


#### Description
* Ansible module to manage iRMC user accounts via iRMC remote scripting interface.
* Module Version V1.0.1.

#### Requirements
  * The module needs to run locally.
  * python >= 2.6

#### Options

| Parameter | Required | Default | Choices | Description |
|:----------|:---------|:--------|:--------|:----------- |
| command  |  No  |  get  | <ul><li>get</li><li>set</li></ul>  | license key management to be executed |
| irmc_password  |  Yes  |  | | password for iRMC user for basic authentication |
| irmc_url  |  Yes  |  | | IP address of the iRMC to be requested for data |
| irmc_username  |  Yes  |  | | iRMC user for basic authentication |
| license_key  |  No  |  | | iRMC license key to be set |
| validate_certs  |  No  |  True  | | evaluate SSL certificate (set to false for self-signed certificate) |

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

| Name | Description | Returned | Type |
|:-----|:------------|:---------|:-----|
| license_key   | iRMC license key |  always |  string |

#### Notes

- A license key which was read from an iRMC is 'system-locked'. It can imported to the same iRMC, but not to another iRMC.
- See http://manuals.ts.fujitsu.com/file/12563/wp-svs-irmc-remote-scripting-en.pdf
- See https://sp.ts.fujitsu.com/dmsp/Publications/public/dp-svs-configuration-space-values-en.pdf

---
### irmc_powerstate


#### Description
* Ansible module to get or set server power state via iRMC RedFish interface.
* Module Version V1.0.1.

#### Requirements
  * The module needs to run locally.
  * iRMC S4 needs FW >= 9.04, iRMC S5 needs FW >= 1.25.
  * python >= 2.6

#### Options

| Parameter | Required | Default | Choices | Description |
|:----------|:---------|:--------|:--------|:----------- |
| command  |  No  |  get  | <ul><li>get</li><li>set</li></ul>  | get or set server power state |
| irmc_password  |  Yes  |  | | password for iRMC user for basic authentication |
| irmc_url  |  Yes  |  | | IP address of the iRMC to be requested for data |
| irmc_username  |  Yes  |  | | iRMC user for basic authentication |
| state  |  No  |  | <ul><li>PowerOn</li><li>PowerOff</li><li>PowerCycle</li><li>GracefulPowerOff</li><li>ImmediateReset</li><li>GracefulReset</li><li>PulseNmi</li><li>PressPowerButton</li></ul>  | desired server power state for command 'set', ignored otherwise; options 'GracefulPowerOff' and ' GracefulReset' require ServerView Agents running on server |
| validate_certs  |  No  |  True  | | evaluate SSL certificate (set to false for self-signed certificate) |

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

| Name | Description | Returned | Type |
|:-----|:------------|:---------|:-----|
| power_state   | server power state |  always |  str |

#### Notes

- See http://manuals.ts.fujitsu.com/file/13371/irmc-restful-spec-en.pdf
- See http://manuals.ts.fujitsu.com/file/13372/irmc-redfish-wp-en.pdf

---
### irmc_scci


#### Description
* Ansible module to execute iRMC Remote Scripting (SCCI) commands.
* Module Version V1.0.1.

#### Requirements
  * The module needs to run locally.
  * python >= 2.6

#### Options

| Parameter | Required | Default | Choices | Description |
|:----------|:---------|:--------|:--------|:----------- |
| cabid  |  No  |  -1 (main cabinet)  | | SCCI cabinet ID |
| command  |  Yes  |  | <ul><li>get_cs</li><li>set_cs</li><li>power_on</li><li>power_off</li><li>power_cycle</li><li>reset</li><li>nmi</li><li>graceful_shutdown</li><li>graceful_reboot</li><li>cancel_shutdown</li><li>reset_firmware</li><li>connect_fd</li><li>connect_cd</li><li>connect_hd</li></ul>  | SCCI remote scripting command (opcode) |
| data  |  No  |  | | data for commands which require data, ignored otherwise |
| index  |  No  |  | | SCCI index |
| irmc_password  |  Yes  |  | | password for iRMC user for basic authentication |
| irmc_url  |  Yes  |  | | IP address of the iRMC to be requested for data |
| irmc_username  |  Yes  |  | | iRMC user for basic authentication |
| opcodeext  |  No  |  | | SCCI opcode extension |
| validate_certs  |  No  |  True  | | evaluate SSL certificate (set to false for self-signed certificate) |

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

# Read server location
- name: "Read server location"
  irmc_scci:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    command: "get_cs"
    opcodeext: 0x200
  register: scci
  delegate_to: localhost
- name: Show server location
  debug:
    msg: "{{ scci.data }}"
```

#### Return Values

| Name | Description | Returned | Type |
|:-----|:------------|:---------|:-----|
| data   | SCCI command result |  always |  str |

#### Notes

- See http://manuals.ts.fujitsu.com/file/12563/wp-svs-irmc-remote-scripting-en.pdf
- See https://sp.ts.fujitsu.com/dmsp/Publications/public/dp-svs-configuration-space-values-en.pdf

---
### irmc_setnextboot


#### Description
* Ansible module to configure iRMC to force next boot to specified option.
* Module Version V1.0.1.

#### Requirements
  * The module needs to run locally.
  * iRMC S4 needs FW >= 9.04, iRMC S5 needs FW >= 1.25.
  * python >= 2.6

#### Options

| Parameter | Required | Default | Choices | Description |
|:----------|:---------|:--------|:--------|:----------- |
| bootmode  |  No  |  | <ul><li>Legacy</li><li>UEFI</li></ul>  | the mode for the next boot |
| bootoverride  |  No  |  Once  | <ul><li>Once</li><li>Continuous</li></ul>  | boot override type |
| bootsource  |  No  |  BiosSetup  | <ul><li>None</li><li>Pxe</li><li>Floppy</li><li>Cd</li><li>Hdd</li><li>BiosSetup</li></ul>  | the source for the next boot |
| irmc_password  |  Yes  |  | | password for iRMC user for basic authentication |
| irmc_url  |  Yes  |  | | IP address of the iRMC to be requested for data |
| irmc_username  |  Yes  |  | | iRMC user for basic authentication |
| validate_certs  |  No  |  True  | | evaluate SSL certificate (set to false for self-signed certificate) |

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

| Name | Description | Returned | Type |
|:-----|:------------|:---------|:-----|
| result   | nextboot action result |  always |  dict |

#### Notes

- See http://manuals.ts.fujitsu.com/file/13371/irmc-restful-spec-en.pdf
- See http://manuals.ts.fujitsu.com/file/13372/irmc-redfish-wp-en.pdf

---
### irmc_setvm


#### Description
* Ansible module to set iRMC Virtual Media Data via iRMC RedFish interface.
* Module Version V1.0.1.

#### Requirements
  * The module needs to run locally.
  * iRMC S4 needs FW >= 9.04, iRMC S5 needs FW >= 1.25.
  * python >= 2.6

#### Options

| Parameter | Required | Default | Choices | Description |
|:----------|:---------|:--------|:--------|:----------- |
| force_mediatype_active  |  No  |  | | forces iRMC to activate one of the required remote media types |
| force_remotemount_enabled  |  No  |  | | forces iRMC to enable the remote mount feature |
| image  |  Yes  |  | | name of the remote image |
| irmc_password  |  Yes  |  | | password for iRMC user for basic authentication |
| irmc_url  |  Yes  |  | | IP address of the iRMC to be requested for data |
| irmc_username  |  Yes  |  | | iRMC user for basic authentication |
| server  |  Yes  |  | | remote server (IP or DNS name) where the image is located |
| share  |  Yes  |  | | path on the remote server where the image is located |
| share_type  |  No  |  | <ul><li>NFS</li><li>SMB</li></ul>  | share type (NFS share or SMB share) |
| validate_certs  |  No  |  True  | | evaluate SSL certificate (set to false for self-signed certificate) |
| vm_domain  |  No  |  | | user domain in case of SMB share |
| vm_password  |  No  |  | | user password in case of SMB share |
| vm_type  |  No  |  CDImage  | <ul><li>CDImage</li><li>FDImage</li><li>HDImage</li></ul>  | the virtual media type to be set |
| vm_user  |  No  |  | | user account in case of SMB share |

#### Examples
```yaml
# Set Virtual Media Data
- name: Set Virtual Media Data
  irmc_setvm:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    server: "{{ server }}"
    share: "{{ share }}"
    image: "{{ image }}"
    share_type: "{{ share_type }}"
  delegate_to: localhost
```

#### Return Values

| Name | Description | Returned | Type |
|:-----|:------------|:---------|:-----|
| result   | virtual media set action result |  always |  dict |

#### Notes

- See http://manuals.ts.fujitsu.com/file/13371/irmc-restful-spec-en.pdf
- See http://manuals.ts.fujitsu.com/file/13372/irmc-redfish-wp-en.pdf

---
### irmc_user


#### Description
* Ansible module to manage iRMC user accounts via iRMC remote scripting interface.
* Module Version V1.0.1.

#### Requirements
  * The module needs to run locally.
  * python >= 2.6

#### Options

| Parameter | Required | Default | Choices | Description |
|:----------|:---------|:--------|:--------|:----------- |
| alert_fans  |  No  |  | <ul><li>None</li><li>Critical</li><li>Warning</li><li>All</li></ul>  | define alert level for fan sensors |
| alert_hderrors  |  No  |  | <ul><li>None</li><li>Critical</li><li>Warning</li><li>All</li></ul>  | define alert level for disk drivers & controllers |
| alert_hwerrors  |  No  |  | <ul><li>None</li><li>Critical</li><li>Warning</li><li>All</li></ul>  | define alert level for critical hardware errors |
| alert_memory  |  No  |  | <ul><li>None</li><li>Critical</li><li>Warning</li><li>All</li></ul>  | define alert level for memory |
| alert_network  |  No  |  | <ul><li>None</li><li>Critical</li><li>Warning</li><li>All</li></ul>  | define alert level for network interface |
| alert_others  |  No  |  | <ul><li>None</li><li>Critical</li><li>Warning</li><li>All</li></ul>  | define alert level for other |
| alert_posterrors  |  No  |  | <ul><li>None</li><li>Critical</li><li>Warning</li><li>All</li></ul>  | define alert level for POST errors |
| alert_power  |  No  |  | <ul><li>None</li><li>Critical</li><li>Warning</li><li>All</li></ul>  | define alert level for system power |
| alert_remote  |  No  |  | <ul><li>None</li><li>Critical</li><li>Warning</li><li>All</li></ul>  | define alert level for remote management |
| alert_security  |  No  |  | <ul><li>None</li><li>Critical</li><li>Warning</li><li>All</li></ul>  | define alert level for security |
| alert_syshang  |  No  |  | <ul><li>None</li><li>Critical</li><li>Warning</li><li>All</li></ul>  | define alert level for system hang |
| alert_sysstatus  |  No  |  | <ul><li>None</li><li>Critical</li><li>Warning</li><li>All</li></ul>  | define alert level for system status |
| alert_temperatures  |  No  |  | <ul><li>None</li><li>Critical</li><li>Warning</li><li>All</li></ul>  | define alert level for temperature sensors |
| avr_enabled  |  No  |  | | user may use Advanved Video Redirection (AVR) |
| command  |  No  |  get  | <ul><li>get</li><li>create</li><li>change</li><li>delete</li></ul>  | user management to be executed |
| config_bmc_enabled  |  No  |  | | user may configure iRMC settings |
| config_user_enabled  |  No  |  | | user may configure user accounts |
| description  |  No  |  | | user account desciption |
| email_address  |  No  |  | | alert email address |
| email_enabled  |  No  |  | | alert email enabled |
| email_encrypted  |  No  |  | | alert email is encrypted |
| email_server  |  No  |  | <ul><li>Automatic</li><li>Primary</li><li>Secondary</li></ul>  | preferred mail server for alert email |
| email_type  |  No  |  | <ul><li>Standard</li><li>ITS-Format</li><li>REMCS</li><li>Fixed Subject</li><li>SMS</li></ul>  | alert email format |
| enabled  |  No  |  | | user account enabled |
| irmc_password  |  Yes  |  | | password for iRMC user for basic authentication |
| irmc_url  |  Yes  |  | | IP address of the iRMC to be requested for data |
| irmc_username  |  Yes  |  | | iRMC user for basic authentication |
| lan_privilege  |  No  |  | <ul><li>Reserved</li><li>Callback</li><li>User</li><li>Operator</li><li>Administrator</li><li>OEM</li><li>NoAccess</li></ul>  | IPMI LAN channel privilege |
| name  |  Yes  |  | | user account name |
| password  |  No  |  | | user account password |
| redfish_enabled  |  No  |  | | user may use iRMC Redfish interface |
| redfish_role  |  No  |  | <ul><li>NoAccess</li><li>Operator</li><li>Administrator</li><li>ReadOnly</li></ul>  | user account Redfish role |
| serial_privilege  |  No  |  | <ul><li>Reserved</li><li>Callback</li><li>User</li><li>Operator</li><li>Administrator</li><li>OEM</li><li>NoAccess</li></ul>  | IPMI serial channel privilege |
| shell  |  No  |  | <ul><li>SMASH CLP</li><li>CLI</li><li>Remote Manager</li><li>IPMI basic mode</li><li>IPMI terminal mode</li><li>None</li></ul>  | user text access type |
| snmpv3_access  |  No  |  | <ul><li>ReadOnly</li><li>ReadWrite</li><li>Other</li></ul>  | user account SNMPV3 access privilege |
| snmpv3_auth  |  No  |  | <ul><li>Undefined</li><li>SHA</li><li>MD5</li><li>None</li></ul>  | user account SNMPv3 authentication |
| snmpv3_enabled  |  No  |  | | user may use SNMPv3 |
| snmpv3_privacy  |  No  |  | <ul><li>Undefined</li><li>AES</li><li>DES</li><li>None</li></ul>  | user account SNMPv3 privacy type |
| ssh_certificate  |  No  |  | | user account SSH certificate |
| ssh_public_key  |  No  |  | | user account SSH public key |
| storage_enabled  |  No  |  | | user may use Remote Storage |
| validate_certs  |  No  |  True  | | evaluate SSL certificate (set to false for self-signed certificate) |

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

| Name | Description | Returned | Type |
|:-----|:------------|:---------|:-----|
| user   | user account information |  always |  dict |

#### Notes

- See http://manuals.ts.fujitsu.com/file/12563/wp-svs-irmc-remote-scripting-en.pdf
- See https://sp.ts.fujitsu.com/dmsp/Publications/public/dp-svs-configuration-space-values-en.pdf

---


