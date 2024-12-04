# サンプルプレイブック説明書

**ご注意**：
このドキュメントは、<https://galaxy.ansible.com/>上で閲覧する際に、
レイアウトが崩れる場合があります。
そのため[github.com](https://github.com/fujitsu/fujitsu-ansible-irmc-integration)
上で閲覧することを推奨します。

## 1. プレイブック

`./example/playbooks/`には以下のプレイブックが用意されています。

- `update_bios_and_irmc_firmware.yml`
- `primergy_setup_with_os_installation.yml`
- `primergy_setup.yml`

---

## 2. 使用方法

### 2.1 共通の準備

#### インベントリファイル

- どのプレイブックを実行する場合においても、インベントリファイルは必要です。
- [ユーザーガイド](./USER_GUIDE_ja.md)
  (link to [galaxy.ansible.com](https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/docs/USER_GUIDE_ja/))
  の
  「[インベントリファイルの設定例](./USER_GUIDE_ja.md#インベントリファイルの設定例)」
  に従って、イベントリファイル`inventory.ini`を作成してください。

#### ファイル共有サーバー

- BIOS・iRMCのファームウェアアップデートを実施する場合はtftpサーバーが必要です。
- OSインストールを実施する場合はNFSまたはSMBサーバーが必要です。

---

### 2.2 プレイブック`update_bios_and_irmc_firmware.yml`

#### 2.2.1 機能

- iRMC機器のBIOS、およびiRMCのファームウェアをアップデートします。

#### 2.2.2 準備

- 機種に応じたファームウェアは事前に入手してください。
  入手方法については
  [設定ガイド](./CONFIGURATION_ja.md)
  (link to [galaxy.ansible.com](https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/docs/CONFIGURATION_ja/))
  の
  「[BIOSファームウェア更新](./CONFIGURATION_ja.md#biosファームウェア更新)」
  と
  「[iRMCファームウェア更新](./CONFIGURATION_ja.md#irmcファームウェア更新)」
  を参照してください。
- tftpサーバーを用意し、入手したファームウェアを配置してください。

#### 2.2.3 プレイブックへの記載

- `vars.tftp_server`にtftpサーバーのIPアドレスを記述してください。
- 各ロールの`bios_firmware_path_mapping`と`irmc_firmware_path_mapping`に該当機種名と、
  その機種に適用するファームウェアのパスをkey-value形式で記述してください。
  パスはtftpサーバーのルートディレクトリからのパスです。
- BIOS、iRMCのどちらかのみアップデートする場合は、
  必要の無い方の`role`ディレクティブをまとめて無効化（削除またはコメントアウト）してください。

#### 2.2.4 実行方法

以下のコマンドを実行してください：

```shell
ansible-playbook -i inventory.ini ./examples/playbooks/update_bios_and_irmc_firmware.yml
```

- ファームウェアのアップデートには、BIOS・iRMCそれぞれ10分以上の時間がかかります。
- BIOS、iRMCの順番でアップデートを行います。
  iRMCのファームウェアアップデート後、iRMCのリブートが行われますが、
  リブート完了の検知に失敗してエラーになるケースがあります。
  その場合であってもiRMCのファームウェアアップデートは完了したか、
  もしくは実行中なのでiRMCにログインして、システム > 動作中のiRMCファームウェアから
  動作中のバージョンを確認してください。

---

### 2.3 プレイブック`primergy_setup_with_os_installation.yml`（`primergy_setup.yml`）

#### 2.3.1 機能

PRIMERGYの初期セットアップを想定したシナリオとして構成されています。
OSインストールが必要ない場合は`primergy_setup.yml`を使用してください。  
このプレイブックでインストールや設定をするOSは、Windows Server 2022を想定しています。

1. iRMCの設定
2. OSインストールのための準備と電源投入
   （OSインストールをしない場合は電源投入のみ）
3. OSインストール（または電源投入）後のWinRMサービス待機処理
4. OS（Windows Server 2022）の設定

#### 2.3.2 準備

以下の情報を入手してください：

- **OSインストールする場合**：
  - インストールするOSに適用するIPアドレス
    （プレイブック実行前に「インベントリファイル」に記載してください）
  - インストールするOSに適用する`Administrator`アカウントのパスワード
    （プレイブック実行前に「インベントリファイル」に記載してください）
  - インストールするOS（Windows Server 2022）のインストールメディアiso形式ファイル
  - （iRMC機器用の） 「メディア」と「KVM」のライセンスキー
  - ファイル共有サーバーを用意し、インストールメディアを配置して下さい。
    ファイル共有はNFSかSMBのいずれかです。
- **必要に応じて**：
  - DNSサーバのIPアドレス
  - SMTPサーバー（メールサーバー）のホスト名またはIPアドレス、
    SMTP認証の場合にはそのアカウントとパスワード
  - SNMPマネージャーのホスト名またはIPアドレス、コミュニティ名など
  - NTPサーバーのホスト名またはIPアドレス
  - （iRMC機器用の）SSL証明書・CA証明書
  - （iRMC機器用の）ライセンスキー
  - ドメインコントローラーのドメイン名と、
    連携しているDNSサーバー（通常はドメインコントローラー自身）のIPアドレス

必要に応じて、以下のファイルを入手してください。
入手方法については[設定ガイド](./CONFIGURATION_ja.md)
(link to [galaxy.ansible.com](https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/docs/CONFIGURATION_ja/))
の各項目を参照してください：

- ServerView Agentsのインストーラー
- ServerView RAID Managerのインストーラー
- AdoptOpenJDKのインストーラー（ServerView RAID Managerをインストールする場合）
- ServerView Suiteのisoファイル

#### 2.3.3 プレイブックへの記載

- 入手した情報をプレイブック
  `primergy_setup_with_os_installation.yml`（`primergy_setup.yml`）
  に記載してください。
- 設定が不要な箇所は`import_role`ディレクティブを含むブロックごとに
  無効化（削除かコメントアウト）してください。
- 特に注意が必要な箇所について補足します：
  - **iRMCのユーザ登録 `fujitsu.primergy.irmc_account_admin`**：
    権限（`role`=`Administrator`や`ipmi.lan_privilege`=`OEM`）を不用意に変更すると、
    それ以降の設定タスクがエラーになる可能性がありますのでご注意ください。
  - **SSL証明書・CA証明書設定 `fujitsu.primergy.irmc_set_certificate`**：
    パラメタ`ssl_private_key_path`で指定したファイルは
    ヘッダとフッタをOpenSSL3.x形式にするため直接書き換えられます。
    オリジナルファイルを書き換えられたく無い場合はご注意ください。
    また、指定したファイルへの書き込み権限が必要です。
  - **ライセンス登録 `fujitsu.primergy.irmc_set_license`**：
    iRMCのライセンスは機器ごとに発行されるため、
    パラメタ`license_keys`はiRMC機器ごとに記述する必要があります。
    カレントディレクトリの下の`host_vars/<iRMC機器のIPアドレス>.yml`というファイルに
    パラメタ`license_keys`を記述してください。

    ```yaml
    # ./host_vars/192.0.2.128.yml
    license_keys:
      - LICENSE-KEY1
      - LICENSE-KEY2
    ```

  - **WindowsサーバーのDNS設定 `fujitsu.primergy.win_dns`**：
    パラメタ`adapter_names`に`"*"`を指定した場合は全てのネットワークアダプタへの設定になります。
    特定のネットワークアダプタに設定したい場合は、そのアダプタ名を指定してください。
    アダプタ名はWindowsインストール後であれば`Get-NetAdapter`で調べることが出来ます。
  - **ドメイン参加 `fujitsu.primergy.win_set_membership`**：
    ドメインに参加する場合は、WindowsサーバーのDNS設定`fujitsu.primergy.win_dns`で、
    １つ目のDNSサーバーにドメインコントローラーと連携しているDNSサーバーを指定してください。
  - **データドライブ設定 `fujitsu.primergy.win_data_drive`**：
    パラメタ`disk_number`で指定したストレージに未割り当て領域が無い場合エラーになります。
    `disk_number`に0を指定する（つまり、OSをインストールしたストレージに割り当てる）場合は、
    OSインストール時に未割り当て領域が出来るようにパーティションを設定をする必要があります。

#### 2.3.3 実行方法

- **OSインストール有り**:

  ```shell
  ansible-playbook -i inventory.ini ./examples/playbooks/primergy_setup_with_os_installation.yml
  ```

  OSインストールが始まったら、
  iRMC WebUI上のリモートコンソール機能であるAVR（Advanced Video Redirection）を開き、
  コンソールからインストーラーを操作してください。

- **OSインストール無し**:

  ```shell
  ansible-playbook -i inventory.ini ./examples/playbooks/primergy_setup.yml
  ```

- **共通**:
  - どちらの場合でも電源投入後、
    起動したWindowsサーバーでWinRMが有効になるまで、プレイブックによって一定時間待機します
    （WinRMはWindowsをAnsibleで管理する場合に必要になるサービスです）。
  - Windowsサーバー起動後にしばらく（２～３分程度）しても待機から抜けない場合は、
    WinRMへの接続が出来ていません。
    その場合はファイアウォールの設定が必要です。
    管理者権限でWindowsサーバーにログインして、以下のコマンドを実行してください。

    ```powershell
    New-NetFirewallRule -Name 'WinRM HTTP' -DisplayName 'Allow WinRM over HTTP' -Enabled True -Direction Inbound -Protocol TCP -LocalPort 5985 -Action Allow
    ```

    ファイアウォールを設定することでWinRMへの接続が可能になり、
    プレイブックは待機状態から抜けて、次のタスクへ処理を進めます。
