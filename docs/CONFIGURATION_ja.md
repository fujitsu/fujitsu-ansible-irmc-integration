# Ansibleコレクション `fujitsu.primergy` 設定ガイド

**ご注意**：
このドキュメントは、<https://galaxy.ansible.com/>上で閲覧する際に、
レイアウトが崩れる場合があります。
そのため[github.com](https://github.com/fujitsu/fujitsu-ansible-irmc-integration)
上で閲覧することを推奨します。

## 1. はじめに

このドキュメントはAnsibleコレクション`fujitsu.primergy`で提供している各ロールの利用方法を、
プレイブックの例を添えて説明します。  
この設定ガイドではAnsibleを使用して、PRIMERGYのiRMCの各種設定、OS（Windowsサーバー）のインストール、
そしてWindowsサーバーの設定を行います。

## 2. PRIMERGY

PRIMERGYのiRMC（遠隔管理機能）の設定を行います。

### 環境設定シート -ハードウェア編-

PRIMERGYの機種ごとに提供されている「環境設定シート -ハードウェア編-」
（以下「環境設定シート(PRIMERGY)」と表記）をあわせて参照してください。  
「環境設定シート(PRIMERGY)」は以下の手順で取得できます：

1. <https://www.fsastech.com/products/pcserver/>
2. 製品ラインアップから該当機種を選択 > マニュアル > 環境設定シート

### iRMCユーザガイド

iRMCの各設定項目の説明は「iRMC S6 Webインターフェイス ユーザガイド」
（以下「iRMCユーザガイド」と表記）も合わせて参照ください。  
「iRMCユーザガイド」は以下の手順で取得できます：

1. <https://support.ts.fujitsu.com/index.asp?ld=jp>
2. 製品を選択する > 製品の検索 > "iRMC"
3. （表示された場合のみ）ダウンロード > 次へ
4. 右記OSに関連した情報を表示する: No Operationg System Dependencies
5. ドキュメント > User Guide > iRMC S6 - Web インターフェース 2.x > ダウンロード

### iRMCファームウェア更新

iRMCのファームウェアをアップデートします。  
[環境設定シート(PRIMERGY)](#環境設定シート--ハードウェア編-)の
「C.1 Toolsの設定項目 / Setting item for Tools」
に相当する項目です。

ファームウェアは事前にダウンロードしてください：

1. <https://support.ts.fujitsu.com/index.asp?ld=jp>
2. 製品を選択する > 識別番号
3. シリアル番号: <シリアル番号>(*1)
4. （表示された場合のみ）ダウンロード > 次へ
5. 右記OSに関連した情報を表示する: OS Independent (BIOS, Firmware, etc.)
6. ドライバ > サーバ管理コントローラ > "*** リモートアップデートツール" > ダウンロード

*1: シリアル番号は`https://<iRMCのIPアドレス>/system`のシステム情報に記載されています。

- パラメタなどの詳細については
  <https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/role/irmc_update_irmc/>
  を参照してください。
- 異なる機種に同時適用するような場合は、それぞれの機種に応じたファームウェアを指定する必要があります。
  パラメタ`irmc_firmware_path_mapping`を参照してください。

**注意**：

- 実行すると、まず最初にiRMC機器の電源をオフにします。
  稼働中のOSは強制的に電源切断となりますので、ご注意下さい。
- （2024-11-14現在では）パラメタ`tftp_server`の指定は必須です。
  tftpサーバーを経由しないアップデートを実施した場合、
  パラメタ`destination`で指定した側にアップデート・再起動されない可能性があるためです。
- ファームウェアアップデート後、自動的にiRMCは再起動されますが、再起動の完了を検知出来ずAnsibleタスクがエラーになる場合があります。
  そのため、他のロールやモジュールと組み合わせて一つのプレイブックで実行することは推奨しません。  

```yaml
---
- hosts: iRMC_group
  connection: local
  gather_facts: false
  roles:
    - role: fujitsu.primergy.irmc_update_irmc
      vars:
        tftp_server: 192.0.2.1
        irmc_firmware_path: "RX1330_M6/irmc/FTS_PRIMERGYRX1330M6iRMC253SSDR227.BIN"
        destination: low
```

### BIOSファームウェア更新

BIOSのファームウェアをアップデートします。  
[環境設定シート(PRIMERGY)](#環境設定シート--ハードウェア編-)の
「C.1 Toolsの設定項目 / Setting item for Tools」
に相当する項目です。

ファームウェアは事前にダウンロードしてください：

1. <https://support.ts.fujitsu.com/index.asp?ld=jp>
2. 製品を選択する > 識別番号
3. シリアル番号: <シリアル番号>(*1)
4. （表示された場合のみ）ダウンロード > 次へ
5. 右記OSに関連した情報を表示する: OS Independent (BIOS, Firmware, etc.)
6. BIOS > "*** オフライン／リモートアップデートツール" > ダウンロード
7. ZIPファイルを展開し`*.upd`ファイル、または`*.upc`ファイルを取り出す

*1: シリアル番号は`https://<iRMCのIPアドレス>/system`のシステム情報に記載されています。

- パラメタなどの詳細については
  <https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/role/irmc_update_bios/>
  を参照してください。
- 異なる機種に同時適用するような場合は、それぞれの機種に応じたファームウェアを指定する必要があります。
  パラメタ`bios_firmware_path_mapping`を参照してください。

**注意**：

- 実行すると、まず最初にiRMC機器の電源をオフにします。
  稼働中のOSは強制的に電源切断となりますので、ご注意下さい。

```yaml
---
- hosts: iRMC_group
  connection: local
  gather_facts: false
  roles:
    - role: fujitsu.primergy.irmc_update_bios
      vars:
        bios_firmware_path: "/any/where/firm/RX1330_M6/bios/D4133-A1x.R1.1.0.UPC"
```

### SSL証明書・CA証明書

iRMCのSSL証明書とCA証明書を設定します。

- SSL証明書とCA証明書は、事前の作成または入手が必要です。
- パラメタなどの詳細については
  <https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/role/irmc_set_certificate/>
  を参照してください。

```yaml
---
- hosts: iRMC_group
  connection: local
  gather_facts: false
  roles:
    - role: fujitsu.primergy.irmc_set_certificate
      vars:
        ssl_private_key_path: "/path/to/certs/server.key"
        ssl_cert_path: "/path/to/certs/server.crt"
        ssl_ca_cert_path: "/path/to/certs/ca.crt"
```

### SNMP

[環境設定シート(PRIMERGY)](#環境設定シート--ハードウェア編-)の
「C.2 Settings の設定項目 / Setting item for Settings」 >
「■Services」 >
「Simple Network Management Protocol (SNMP)」
に相当する項目です。  

- [iRMCユーザガイド](#irmcユーザガイド)
  の「2.4.4 サービス」 > 「SNMP 設定」も合わせて参照してください。
- パラメタなどの詳細については
  <https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/role/irmc_snmp/>
  を参照してください。
- パラメタ`irmc_snmp.trap_destination.servers[].index`は0から6までの値を指定し、
  それぞれ「iRMC Webインターフェイス」のSNMPトラップサーバ1から7までに相当します。
- 変更不要なパラメタは記述しなくて構いません。

```yaml
---
- hosts: iRMC_group
  connection: local
  gather_facts: false
  roles:
    - role: fujitsu.primergy.irmc_snmp
      vars:
        irmc_snmp:
          enabled: true
          protocol: "All"
          community_name: "test-public"

          trap_destination:
            community_name: "test-trap-public"
            servers:
              - index: 0
                name: 192.0.2.1
                protocol: "SnmpV2c"
              - index: 1
                name: 192.0.2.2
                protocol: "SnmpV1"
```

### Eメール警告送信

[環境設定シート(PRIMERGY)](#環境設定シート--ハードウェア編-)の
「C.2 Settings の設定項目 / Setting item for Settings」 >
「■Services」 >
「E-mail Alerting」
に相当する項目です。

- [iRMCユーザガイド](#irmcユーザガイド)
  の「2.4.4 サービス」 > 「Eメール警告送信」も合わせて参照してください。
- パラメタなどの詳細については
  <https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/role/irmc_email_alert/>
  を参照してください。
- 変更不要なパラメタは記述しなくて構いません。

```yaml
---
- hosts: iRMC_group
  connection: local
  gather_facts: false
  roles:
    - role: fujitsu.primergy.irmc_email_alert
      vars:
        irmc_email_alert:
          enabled: true
          smtp:
            primary_server:
              address: 192.0.2.1
              authentication:
                type: "Smtp"
                username: "AuthUserName"
                password: "AuthPassword"
          email_format:
            from: "MailFrom@domain.example.com"
            subject: "FixedMailSubject"
            message: "FixedMailMessage"
```

### ローカルユーザアカウント

#### 1番目のユーザの設定(購入時のユーザー名`admin`)

[環境設定シート(PRIMERGY)](#環境設定シート--ハードウェア編-)の
「C.3 Settings の設定項目 / Setting item for Settings」 >
「■User Management」 >
「iRMC Local User Accounts」
に相当する項目です。

- [iRMCユーザガイド](#irmcユーザガイド)
  の「2.4.5 ユーザ管理」も合わせて参照してください。
- パラメタなどの詳細については
  <https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/role/irmc_account_admin/>
  を参照してください。
- 購入時の初期ユーザ名`admin`から変更している場合、このロールは機能しません。

```yaml
---
- hosts: iRMC_group
  connection: local
  gather_facts: false
  roles:
    - role: fujitsu.primergy.irmc_account_admin
      vars:
        irmc_account_admin:
          password: P@ssw0rd
          description: This is Administrator
```

#### 2～15番目までのユーザの設定

[環境設定シート(PRIMERGY)](#環境設定シート--ハードウェア編-)の
「C.3 Settings の設定項目 / Setting item for Settings」 >
「■User Management」 >
「iRMC Local User Accounts」
に相当する項目です。

- [iRMCユーザガイド](#irmcユーザガイド)
  の「2.4.5 ユーザ管理」も合わせて参照してください。

注意：

- このロールはまだ提供していません。

### 時刻同期

[環境設定シート(PRIMERGY)](#環境設定シート--ハードウェア編-)の
「C.3 Settings の設定項目 / Setting item for Settings」 >
「■Baseboard Management Controller」 >
「Time Synchronization」
に相当する項目です。

- [iRMCユーザガイド](#irmcユーザガイド)
  の「2.4.9 ベースボードマネジメントコントローラ」 > 「時刻同期」も合わせて参照してください。
- パラメタなどの詳細については
  <https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/role/irmc_set_ntp/>
  を参照してください。

```yaml
---
- hosts: iRMC_group
  connection: local
  gather_facts: false
  roles:
    - role: fujitsu.primergy.irmc_set_ntp
      vars:
        ntp_server_primary: 192.0.2.1
        ntp_server_secondary: 192.0.2.2
        time_mode: "System RTC"
        time_zone_location: "Asia/Tokyo"
        rtc_mode: "local time"
```

### ライセンスキー

[環境設定シート(PRIMERGY)](#環境設定シート--ハードウェア編-)の
「C.3 Settings の設定項目 / Setting item for Settings」 >
「■Baseboard Management Controller」 >
「License Keys」
に相当する項目です。

- [iRMCユーザガイド](#irmcユーザガイド)
  の「2.4.9 ベースボードマネジメントコントローラ」 > 「ライセンスキー」も合わせて参照してください。
- パラメタなどの詳細については
  <https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/role/irmc_set_license/>
  を参照してください。

```yaml
---
- hosts: iRMC_group
  connection: local
  gather_facts: false
  roles:
    - role: fujitsu.primergy.irmc_set_license
      vars:
        license_keys:
          - "XXX-XXXX-XXXX-XXXX-XXXX-XX-AA"
          - "XXX-XXXX-XXXX-XXXX-XXXX-XX-BB"
```

---

## 3. OSインストール

- Windows Server 2022のインストールを行います。
- iRMCの「バーチャルメディア」と「AVR」を使用するため、
  「メディア」と「KVM」のライセンスが必要です。
- このロールを実行すると、
  インストールメディアの仮想ドライブへの挿入、
  ブート優先順をCD・DVD-ROMからに変更、
  そして機器の電源オンまでを一連の処理として実行します。
- 自動インストールの仕掛けは組み込まれていないので、
  機器の電源オンの後、iRMCのAVRを開いてインストーラーを操作する必要があります。
- AVR（Advanced Video Redirection）はiRMCが持つリモートコンソール機能です。
  WebブラウザでiRMC（`https://{iRMC機器のIPアドレス}/login`）へログインし、
  画面右上のアイコン（「AVRの起動」のツールチップ）から開くことが出来ます。
- インストール後、WindowsサーバーをターゲットノードとしたAnsibleタスクを実行する場合は、
  WindowsサーバーがAnsibleターゲットノードとして使用できるようになるまで、プレイブックの実行を待機させる必要があります。  
  以下の例の`"ansible.builtin.wait_for_connection"`を参考にして、
  WinRMが有効化されるまでプレイブックの実行が待機されるように制御してください。

```yaml
---
- hosts: iRMC_group
  connection: local
  gather_facts: false
  roles:
    - role: fujitsu.primergy.irmc_install_windows
      vars:
        share_type: NFS
        server: 192.0.2.1
        share: /var/share
        image: iso/windows/ws2022se.iso

# WindowsサーバーがAnsibleで操作可能になるまで待機
- name: Wait for Windows node to become available
  hosts: windows
  tasks:
    - name: Wait for WinRM to become available on the target Windows node
      ansible.builtin.wait_for_connection:
        timeout: 10800  # 最大待機時間（10800秒＝3時間）
```

### 3.1 電源オン（OSインストールをしない場合）

- Windows Server 2022がインストール済みの場合は、
  電源投入を行い、その後Ansibleでの操作が可能になるまで（WinRMが有効になるまで）待機します。
- 「3. OSインストール」とは排他適用です。

```yaml
---
- hosts: iRMC_group
  connection: local
  gather_facts: false
  tasks:
    - name: Turn on the device
      fujitsu.primergy.irmc_powerstate:
        irmc_url: "{{ inventory_hostname }}"
        irmc_username: "{{ irmc_user }}"
        irmc_password: "{{ irmc_password }}"
        validate_certs: "{{ validate_certificate }}"
        command: "set"
        state: "PowerOn"
      delegate_to: localhost
    - name: Show pausing message
      ansible.builtin.debug:
        msg:
          - "Pausing until Windows has booted and is ready for operation by Ansible."
          - "If the pause does not end after Windows finishes booting, follow these steps."
          - ""
          - "1. Login to Windows with Administrator"
          - "2. Run PowerShell and execute the following commands:"
          - ""
          - "New-NetFirewallRule -Name 'WinRM HTTP' -DisplayName 'Allow WinRM over HTTP' -Enabled True -Direction Inbound -Protocol TCP -LocalPort 5985 -Action Allow"

# WindowsサーバーがAnsibleで操作可能になるまで待機
- name: Wait for Windows node to become available
  hosts: windows
  gather_facts: false
  tasks:
    - name: Wait for WinRM to become available on the target Windows node
      ansible.builtin.wait_for_connection:
        timeout: 1800  # 最大待機時間（1800秒＝30分）
```

---

## 4. Windows Server 2022

### 環境設定シート -ServerView Installation Manager編-

「環境設定シート -ServerView Installation Manager編-」
のシート「Win2K**_ガイド」（以下「環境設定シート(Windowsサーバー)」と表記）をあわせて参照してください。  
このプロジェクトで提供している各種ロールはWindows Server 2022でのみ検証していますが、
本ドキュメントは
「環境設定シート -ServerView Installation Manager編-」(CA92344-0149-07)
の"Win2K19"（Windows Server 2019）のガイドをもとに記述しています。

### データドライブ

ストレージの未使用領域を新規ドライブに割り当てます。

- パラメタなどの詳細については
  <https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/role/win_data_drive/>
  を参照してください。

```yaml
---
- hosts: windows
  roles:
    - role: fujitsu.primergy.win_data_drive
      vars:
        op: "create"
        drive_letter: D
        disk_number: 0
```

### 名前と組織名

[環境設定シート（Windowsサーバー）](#環境設定シート--serverview-installation-manager編-)の
シート「Win2K19_ガイド(1)」 > 「基本設定」 > 「名前」・「組織名」
に相当する項目です。

- パラメタなどの詳細については
  <https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/role/win_organization_owner/>
  を参照してください。

```yaml
---
- hosts: windows
  roles:
    - role: fujitsu.primergy.win_organization_owner
      vars:
        organization: Fsas Technologies Inc.
        owner: Fsas Tarou
```

### ホスト名

[環境設定シート（Windowsサーバー）](#環境設定シート--serverview-installation-manager編-)の
シート「Win2K19_ガイド(1)」 > 「基本設定」 > 「コンピュータ名」
に相当する項目です。

- パラメタなどの詳細については
  <https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/role/win_hostname/>
  を参照してください。

```yaml
---
- hosts: windows
  roles:
    - role: fujitus.primergy.win_hostname
      vars:
        hostname: webserver01
```

### 言語・地域設定

[環境設定シート（Windowsサーバー）](#環境設定シート--serverview-installation-manager編-)の
シート「Win2K19_ガイド(1)」 > 「基本設定」 > 「タイムゾーン」・「地域と言語」・「キーボード」
に相当する項目です。

- パラメタなどの詳細については
  <https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/role/win_locale/>
  を参照してください。
- 設定する言語によっては言語パックのダウンロードのために`https://go.microsoft.com/`へアクセスが発生します。
  そのため環境によっては、事前にプロキシの設定（スタート > 設定 > ネットワークとインターネット > プロキシ）などが必要になります。  

```yaml
---
- hosts: windows
  roles:
    - role: fujitsu.primergy.win_locale
      vars:
        language: "en-US"
        location: "244"
        timezone: "Eastern Standard Time"
```

### DNSの設定

[環境設定シート（Windowsサーバー）](#環境設定シート--serverview-installation-manager編-)の
シート「Win2K19_ガイド(2)」 > 「TCP/IP パラメータ 詳細設定」 > 「DNSサーバ」
に相当する項目です。

- パラメタなどの詳細については
  <https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/role/win_dns/>
  を参照してください。
- [ドメインへ参加](#ドメインへの参加)する場合は、
  ドメインコントローラーと連携しているDNSサーバーを指定する必要があります。

```yaml
---
- hosts: windws
  roles:
    - role: fujitsu.primergy.win_dns
      vars:
        adapter_names: Enthernet
        ipv4_addresses:
          - 192.0.2.1
          - 192.0.2.2
```

### ワークグループへの参加

[環境設定シート（Windowsサーバー）](#環境設定シート--serverview-installation-manager編-)の
シート「Win2K19_ガイド(1)」 > 「システムの設定」 > 「参加先」「ワークグループ名」
に相当する項目です。

- パラメタなどの詳細については
  <https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/role/win_set_membership/>
  を参照してください。

```yaml
---
- hosts: windows
  roles:
    - role: fujitsu.primergy.win_set_membership
      vars:
        state: workgroup
        workgroup: WORKGROUP
```

### ドメインへの参加

[環境設定シート（Windowsサーバー）](#環境設定シート--serverview-installation-manager編-)の
シート「Win2K19_ガイド(1)」 > 「システムの設定」 > 「参加先」「ドメイン名」「ドメインユーザ名・パスワード」
に相当する項目です。

- パラメタなどの詳細については
  <https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/role/win_set_membership/>
  を参照してください。
- ドメインに参加する場合は、
  事前にドメインコントローラーと連携している[DNSサーバーを設定](#dnsの設定)しておく必要があります。

```yaml
---
- hosts: windows
  roles:
    - role: fujitsu.primergy.win_set_membership
      vars:
        state: domain
        domain: fti.ansible.local
        username: FTI\Administrator
        password: P@ssw0rd
```

### SNMPの設定

[環境設定シート（Windowsサーバー）](#環境設定シート--serverview-installation-manager編-)の
シート「Win2K19_ガイド(2)」 > 「SNMPサービス」
および
シート「Win2K19_ガイド(3)」 > 「『SNMPサービス』選択時のみ」 > 「SNMPサービス」・「トラップ構成項目」・「セキュリティ」・「エージェント」
に相当する項目です。

- パラメタなどの詳細については
  <https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/role/win_snmp/>
  を参照してください。

```yaml
---
- hosts: windows
  roles:
    - role: fujitsu.primergy.win_snmp
      vars:
        agent:
          contact: MyContact
          location: MyLocation
          service: 76
        security:
          accepted_community: public
          accepted_community_permission: 8
          send_auth_trap: true
        trap:
          community: public
          destination: 192.0.2.1
```

### リモートデスクトップの有効化

[環境設定シート（Windowsサーバー）](#環境設定シート--serverview-installation-manager編-)の
シート「Win2K19_ガイド(3)」 > 「追加のパラメータ」 > 「Remote Desktop」
に相当する項目です。

- パラメタなどの詳細については
  <https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/role/win_set_rdp/>
  を参照してください。

```yaml
---
- hosts: windows
  roles:
    - role: fujitsu.primergy.win_set_rdp
      vars:
        enabled: true
```

### ServerView Agentsのセットアップ

[環境設定シート（Windowsサーバー）](#環境設定シート--serverview-installation-manager編-)の
シート「Win2K19_ガイド(3)」 > 「アプリケーションウィザード」 > 「ServerView Suite」 > 「ServerView Agents」
に相当する項目です。

ServerView Agentsは事前にダウンロードしてください:

1. <https://support.ts.fujitsu.com/index.asp?ld=jp>
2. 製品を選択する > カテゴリから探す > Software > ServerView > Operation > Agents, Agentless Service & Providers
3. （表示された場合のみ）ダウンロード > 次へ
4. 右記OSに関連した情報を表示する: Windows Server 2022
5. アプリケーション > ServerView Agents for Windows > ダウンロード
6. `FTS_ServerViewAgentsforWindows_<version>_*.exe`を実行して展開する
7. `ServerView\Agents\ServerViewAgents_Win_x64.exe`を取り出す

- パラメタなどの詳細については
  <https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/role/win_serverview_agents/>
  を参照してください。
- `installer`にはAnsibleコントロールノードのファイルシステムのパスを指定します。
  絶対パス、もしくはプレイブックからの相対パスで指定します。

```yaml
---
- hosts: windows
  roles:
    - role: fujitsu.primergy.win_serverview_agents
      vars:
        password: P@ssw0rd!
        installer: /any/where/ServerView/Agents/ServerViewAgents_Win_x64.exe
```

### ServerView RAID Managerのセットアップ

[環境設定シート（Windowsサーバー）](#環境設定シート--serverview-installation-manager編-)の
シート「Win2K19_ガイド(3)」 > 「アプリケーションウィザード」 > 「ServerView Suite」 > 「ServerView RAID Manager」
に相当する項目です。

ServerView RAID Managerは事前にダウンロードしてください:

1. <https://support.ts.fujitsu.com/index.asp?ld=jp>
2. 製品を選択する > カテゴリから探す > Software > ServerView > Operation > RAID Management
3. （表示された場合のみ）ダウンロード > 次へ
4. 右記OSに関連した情報を表示する: Windows Server 2022
5. アプリケーション > ServerView RAID Manager (Windows, 64-bit) > ダウンロード
6. `FTS_ServerViewRAIDManagerWindows64bit_<version>_*.zip`を展開する
7. `Windows\x64\ServerView_RAID_<version>_x64.exe`を取り出す

AdoptOpenJDKは事前にダウンロードしてください:

1. <https://adoptium.net/temurin/releases/?os=windows&version=8&arch=x64&package=jre>
2. このロールで適用できるのはAdoptOpenJDKのみです。その他のJDKには対応していません。

- パラメタなどの詳細については
  <https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/role/win_serverview_raidmamanger/>
  を参照してください。
- `installer`および`openjdk_installer`にはAnsibleコントロールノードのファイルシステムのパスを指定します。
  絶対パス、もしくはプレイブックからの相対パスで指定します。

```yaml
- hosts: windows
  roles:
    - role: fujitsu.primergy.win_serverview_raidmanager
      vars:
        password: P@ssw0rd!
        installer: /any/where/ServerViewRAIDManagerWindows64bit/Windows/x64/ServerView_RAID_7.17.5_x64.exe
        openjdk_installer: /any/where/OpenJDK8U-jre_x64_windows_hotspot_8u422b05.msi
```

### 高信頼ツールDSNAPのセットアップ

[環境設定シート（Windowsサーバー）](#環境設定シート--serverview-installation-manager編-)の
シート「Win2K19_ガイド(3)」 > 「アプリケーションウィザード」 > 「Add-on Packages」 > 「DSNAP」
に相当する項目です。

DSNAPはServerView Suiteに格納されています。
ServerView Suite（ServerView Management and Serviceability DVD）は事前にダウンロードしてください:

1. <https://support.ts.fujitsu.com/index.asp?ld=jp>
2. 製品を選択する > 識別番号
3. シリアル番号: <シリアル番号>(*1)
4. （表示された場合のみ）ダウンロード > 次へ
5. 右記OSに関連した情報を表示する: Windows Server 2022
6. アプリケーション > Server Management Software > ServerView - ServerView Suite CDs/DVDs/ISO-Images > ServerView Management and Serviceability DVD > ダウンロード
7. `FTS_ServerViewManagementandServiceabilityDVD_*.zip`ファイルを展開し、isoファイルを取り出す

- パラメタなどの詳細については
  <https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/role/win_dsnap/>
  を参照してください。
- パラメタ`path`にはDSNAP（`*.exe`）を直接指定することが可能です。
  isoファイルからDSNAPを取り出す手間は増えますが
  ターゲットノードへのファイル転送にかかる時間が短くなるので、
  プレイブックの実行時間削減に繋がります。
  isoファイルからDSNAPを取り出す場合は、
  （Windowsでは）isoファイルを右クリック > プログラムから開く > エクスプローラー
  でisoファイルをマウントし、
  `SVSLocalTools\{LANGUAGE}\DSNAP\{ARCH}\dsnap.exe`
  を取り出して下さい。

```yaml
---
- hosts: windows
  roles:
    - role: fujitsu.primergy.win_dsnap
      vars:
        language: Japanese
        path: /path/to/SVS15.24.06.03.iso
```
