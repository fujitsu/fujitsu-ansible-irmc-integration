# Ansibleコレクション `fujitsu.primergy` ユーザーガイド

## 1. はじめに

このドキュメントはAnsibleコレクション`fujitsu.primergy`の利用者に向けたガイドです。
Ansibleコレクションとは、Ansibleのプレイブックやモジュール、
ロール、プラグイン、ドキュメントなどをまとめたパッケージです。
Ansibleコレクション`fujitsu.primergy`では、
PRIMERGYの「環境設定シート」に基づいた設定作業の自動化を目的とし、
Ansibleのロールやモジュールを提供しています。

このユーザーガイドでは、
Ansibleコレクションのセットアップ方法やロールの使用例、
トラブルシューティングに関する情報を提供します。

### 対象読者

このドキュメントは、Ansibleの基本的な知識を持つ方を対象としています。

## 2. インストールとセットアップ

### 必要な前提条件

#### OSとソフトウェア

- Linux（Windowsの場合は「5. よくある質問 (FAQ)」の「WindowsでAnsibleを実行できますか？」を参照）
- Python 3.10

#### Pythonモジュール

- `ansible` >= 8.0.0
- `pywinrm` >= 0.5.0
- `requests` >= 2.32.0
- `requests_toolbelt` >= 1.0.0
- `urllib3` >= 2.2.0

### Ansible実行環境のセットアップ

Pythonの仮想環境（venv）を作成・有効化してから、
Ansibleを含む必要なPythonモジュールをインストールします：

```shell
$ mkdir -p ~/ansible/primergy && cd $_  # 任意のディレクトリを作成し移動
$ python -m venv venv && . $_/bin/activate
(venv) $ python -m pip install ansible pywinrm requests requests_toolbelt urllib3
```

仮想環境（venv）にインストールしたAnsbileを使って、
<https://galaxy.ansible.com/>からAnsibleコレクション`fujitsu.primergy`をインストールします：

```bash
(venv) $ ansible-galaxy collection install fujitsu.primergy
```

### インベントリファイルの設定例

Ansibleでは管理対象の機器を「インベントリファイル」で定義します。

- `[iRMC_group]`と`[windows]`の二つのグループを定義してください。
  これらのグループ名は、この「ユーザーガイド」や「設定ガイド」で説明するAnsibleプレイブックの実行方法の例と揃えてあります。
- `[iRMC_group]`にはPRIMERGYの遠隔管理インターフェイスのIPアドレス、
  管理者権限のあるアカウント（出荷状態であれば`admin`が利用可能）と、
  そのパスワードを記述します。
- `[windows]`にはWindowsサーバーのIPアドレス、
  管理者権限のあるアカウント（通常は`Administrator`）と、
  そのパスワードを記述します。
- いずれも、複数の機器・サーバーを列挙可能です。
- `[*:vars]`には各グループ向けの共通パラメタを指定できます。
  ここでは接続設定のパラメタを記述しています。

`inventory.ini`というファイル名で以下の内容を記述してください：

```ini
[iRMC_group]
<ipaddress-of-iRMC-device> irmc_user=admin irmc_password=<password>

[windows]
<ipaddress-of-windows> ansible_user=Administrator ansible_password=<password>

[iRMC_group:vars]
validate_certificate=false  # iRMC機器にSSLサーバー証明書を登録していない場合は必要

[windows:vars]
ansible_port=5985
ansible_connection=winrm
ansible_winrm_transport=ntlm
ansible_winrm_server_cert_validation=ignore
```

### 疎通テスト

#### iRMC機器への疎通テスト

指定したiRMC機器の構成・設定などを取得し表示します：

```shell
$ ansible localhost -m fujitsu.primergy.irmc_facts -a "irmc_url=192.0.2.1 irmc_username=admin irmc_password=P@ssw0rd! validate_certs=false"
localhost | SUCCESS => {
    "changed": false,
    "facts": {
        "hardware": {
            "ethernetinterfaces": {
（略）
```

`irmc_url`や`irmc_username`、`irmc_password`は
インベントリファイルで`[iRMC_group]`グループに記述した内容です。

#### Windowsサーバーへの疎通テスト

インベントリファイルで指定した`[windows]`グループに接続確認をします：

```shell
$ ansible -i inventory.ini windows -m ansible.windows.win_ping
192.0.2.2 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

`[windows]`に複数のサーバーが記述されている場合は、
その全てのサーバーに対して接続確認が実施されます。

指定したWindowsサーバーの
[WinRM](https://learn.microsoft.com/ja-jp/windows/win32/winrm/portal)
へのリクエストが可能である必要があります。  
Windowsサーバーをインストールした直後の状態でHTTP経由のWinRM接続は有効になっているという想定です
（Powershellから`"winrm enumerate winrm/config/Listener"`で確認可能）。
疎通テストが失敗する場合は以下のファイアウォールの設定を実施してください：

```powershell
New-NetFirewallRule -Name "WinRM HTTP" -DisplayName "Allow WinRM over HTTP" -Enabled True -Direction Inbound -Protocol TCP -LocalPort 5985 -Action Allow
```

## 3. 使用方法

### コレクションの全体構成

このコレクションの詳細なモジュールやロールの一覧については、
[Ansible Galaxyのコレクションページ](https://galaxy.ansible.com/fujitsu/primergy)
を参照してください。

### 各ロールの使い方

[設定ガイド（`CONFIGURATION_ja.md`）](./CONFIGURATION_ja.md)
（link to [galaxy.ansible.com](https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/docs/CONFIGURATION_ja/)）
を参照してください。

### サンプルプレイブックの説明

[サンプルプレイブック（`EXAMPLE_PLAYBOOKS_ja.md`）](./EXAMPLE_PLAYBOOKS_ja.md)
（link to [galaxy.ansible.com](https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/docs/EXAMPLE_PLAYBOOKS_ja/)）
を参照してください。

### トラブルシューティング

プレイブック実行中に発生したエラーの詳細を確認するには、`-vvv`オプションを使用してデバッグログを取得し、エラーメッセージや変数の値を確認してください。

```shell
ansible-playbook -i inventory.ini playbook.yml -vvv
```

## 4. フィードバックと貢献方法

本プロジェクトへのフィードバックや貢献を歓迎しています。
バグ報告、機能リクエスト、改善提案などは、以下の連絡先までお寄せください。  
日本語または英語で対応いたします。

### 連絡方法

#### メールでの連絡

（当社内利用など）非公開のご連絡や問い合わせは、以下のメールアドレスへご送信ください。

- Shinya Hamano (<[hamano.shinya@fujitsu.com](mailto:hamano.shinya@fujitsu.com)>)
- Yutaka Kamioka (<[yutaka.kamioka@fujitsu.com](mailto:yutaka.kamioka@fujitsu.com)>)
- Jiajun Guo (<[guo.jiajun@fujitsu.com](mailto:guo.jiajun@fujitsu.com)>)
- Tomohisa Nakai (<[nakai.tomohisa@fujitsu.com](mailto:nakai.tomohisa@fujitsu.com)>)

※*メンバーおよびEmailアドレスは2024年12月現在のものです。*

#### GitHub Issues

公開のフィードバックや貢献のご提案は、GitHubの「Issues」ページにて受け付けています。  
GitHub Issues: <https://github.com/fujitsu/fujitsu-ansible-irmc-integration/issues>

#### フィードバックの際のお願い

バグ報告の際は、以下の情報を含めていただけると対応がスムーズになります。

- 目的と操作内容 - 設定の目的と、それを達成するために行った具体的な操作・設定内容を記載してください。
- 発生した事象 - 実行結果や予期しない動作など、実際に起きた内容を具体的に記述してください。
- 再現手順や状況 - 問題の再現に必要な手順や、発生した際の環境や状況を記述してください。
- 使用環境（機器やバージョンなど） - 使用機器の機種名やBIOS・iRMCのバージョンを記述してください（ターゲットがiRMC機器の場合）。
  本ドキュメントの項目「[iRMC機器への疎通テスト](#irmc機器への疎通テスト)」に記載した方法で`irmc_facts`を取得するのも良い方法です。
- Ansible実行ログ - Ansible実行ログも添付していただけると原因の特定に役立ちます。特に`-vvv`オプションを使用した詳細なログがあるとより分析がしやすくなります。

## 5. よくある質問 (FAQ)

### WindowsでAnsibleを実行できますか？

Windowsには対応していません。
Windows Subsystem for Linux（WSL）では実行できますが、
正式なサポートでは無く、本番システムへの適用には推奨されていません。  
詳細はこのURLを参照してください：
<https://docs.ansible.com/ansible/latest/os_guide/intro_windows.html#using-windows-as-the-control-node>

## 6. 追加情報

### Ansible Galaxy

- <https://galaxy.ansible.com/>
- <https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/>

### Ansible

- <https://docs.ansible.com/users.html>
- Start writing Ansible playbooks - <https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_intro.html#playbook-syntax>
- Build inventory files to manage multiple hosts - <https://docs.ansible.com/ansible/latest/inventory_guide/intro_inventory.html>
- Start exploring Ansible Galaxy - <https://docs.ansible.com/ansible/latest/galaxy/user_guide.html#finding-collections-on-galaxy>
