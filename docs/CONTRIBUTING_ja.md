# コントリビューションガイドライン

**ご注意**：
このドキュメントは、<https://galaxy.ansible.com/>上で閲覧する際に、
レイアウトが崩れる場合があります。
そのため[github.com](https://github.com/fujitsu/fujitsu-ansible-irmc-integration)
上で閲覧することを推奨します。

## 1. はじめに

このプロジェクトではエフサステクノロジーズのPRIMERGYシリーズを運用するためのAnsibleコレクションの提供を行っています。

- PRIMERGYの遠隔管理機能であるiRMC経由でノードを制御するAnsibleモジュール
- PRIMERGYシリーズの「環境設定シート」に基づき、iRMC機器やWindowsServerをセットアップするAnsibleロール
- それらを包括するプレイブックのサンプル

このガイドラインでは、このプロジェクトの開発保守担当者に向けた情報を提供します。

---

## 2. 行動規範

[Ansible Community code of conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)
に準拠します。

---

## 3. 開発を始める前に

### 3.1 前提条件

- Ansibleの実行にはUnix（Linux）環境が必要です。
- Windows Subsystem for Linux（WSL）では実行できますが、
  正式なサポートでは無く、本番システムへの適用には推奨されていません。
  詳細はこのURLを参照してください：
  <https://docs.ansible.com/ansible/latest/os_guide/intro_windows.html#using-windows-as-the-control-node>
  を参照してください。
- このプロジェクトには二つのGitリポジトリがあります：
  1. **公開用**: <https://github.com/fujitsu/fujitsu-ansible-irmc-integration>
  2. **社内開発用**: URL非公開

  当社社員として開発に参加する場合は「社内開発用」のGitリポジトリを使ってください。
  以下の説明で`github.com`のURLで記述していますが、
  適宜「社内開発用GitリポジトリのURL」に読み替えてください。

### 3.2 開発環境のセットアップ

1. Ansibleコレクションとして実行するためにディレクトリ構成が重要です。
   以下の方法でgitリポジトリをcloneしてください。

   ```shell
   $ mkdir -p ~/git/ansible_collections/fujitsu && cd $_
   $ git clone https://github.com/fujitsu/fujitsu-ansible-irmc-integration.git primergy && cd $_
   $ pwd
   # => ~/git/ansible_collections/fujitsu/primergy
   ```

   `~/git`は任意のパスで構いませんが、
   `ansible_collections/fujitsu/primergy`というディレクトリ階層でcloneされている必要があります。

2. PythonおよびAnsible実行環境の構築を行います。
   [Rye](https://rye.astral.sh/) でPythonプロジェクト環境を記述していますので、
   `rye`コマンドを使って環境構築を行うのが最も簡単です。
   `rye`コマンドのインストールについては <https://rye.astral.sh/guide/installation/> を参照してください。
   RyeはPythonインタープリタのダウンロードも行いますので、Python実行環境を用意する必要はありません。

   ```shell
   $ rye sync
   Initializing new virtualenv in ~/git/ansible_collections/fujitsu/primergy/.venv
   Python version: cpython@3.10.14
   （略）
   Done!  
   ```
  
   Ryeを使って環境構築した場合、
   インストールしたコマンドは`rye`コマンド経由で実行するか、
   `rye sync`によって生成された仮想環境を有効化して実行します。

   ```shell
   # ryeから実行
   $ rye run python -V
   $ rye run ansible --version

   # 仮想環境を有効化して実行
   $ . .venv/bin/activate
   $ python -V
   $ ansible --version
   ```

   ---

   Ryeを使わず環境構築する場合はPython3.10以降のPython実行環境を用意してください。
   仮想環境（venv）を作成・有効化してから、必要なライブラリをインストールしてください。

   ```shell
   $ python -V
   Python 3.10.14
   $ python -m venv .venv
   $ . .venv/bin/activate
   (.venv) $ python -m pip install -r requirements.lock -r requirements-dev.lock
   ```

3. `ansible.cfg`ファイルに、`ansible_collections`ディレクトリがあるディレクトリを指定してください。

   ```ini
   [defaults]
   collections_path = ~/git
   ```

4. `inventory.ini`ファイルを用意してください。
   `iRMC_group`と`windows`グループが必要です。
   実在のターゲットノードのIPアドレス・ユーザID・パスワードを記述してください。
   この例ではそれぞれのグループで使うパラメタもこのファイル（`inventory.ini`）で定義しています。
   特にAnsibleでWindowsをターゲットノードとして管理する場合、WinRMの接続設定が必要です。

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

5. 疎通テストをします。

   - iRMC機器への疎通テストをします：

     ```shell
     $ ansible localhost -m fujitsu.primergy.irmc_facts -a "irmc_url=192.0.2.1 irmc_username=admin irmc_password=P@ssw0rd! validate_certs=false"
     localhost | SUCCESS => {
         "changed": false,
         "facts": {
             "hardware": {
                 "ethernetinterfaces": {
     ```

   - Windowsサーバーへの疎通テストをします：

     ```shell
     $ ansible -i inventory.ini windows -m ansible.windows.win_ping
     192.0.2.2 | SUCCESS => {
         "changed": false,
         "ping": "pong"
     }
     ```

     Windowsサーバーへの疎通が失敗する場合は、Windowsサーバーでファイアウォールの設定を実施してください：

     ```powershell
     New-NetFirewallRule -Name "WinRM HTTP" -DisplayName "Allow WinRM over HTTP" -Enabled True -Direction Inbound -Protocol TCP -LocalPort 5985 -Action Allow
     ```

6. プレイブックを実行します。 
   インベントリファイル（`inventory.ini`）の`[iRMC_group]`に機器が設定されている状態で、
   以下のコマンドを実行してください。
   iRMC機器にライセンスを登録するロールを実行します：

   ```shell
   ansible-playbook -i inventory.ini ./roles/irmc_set_license/tests/test.yml -e license_keys='["XXX"]' -vvv
   ```

   この例で登録しようとしているライセンス（`"XXX"`）は正しく無いので、
   「無効なライセンスキー」のエラーが表示されれば、正しくロールが実行されていると判断できます。

---

## 4. 貢献方法

### 4.1 問題やバグの報告

- GitHubのIssue（もしくは社内開発用のGitリポジトリのBugのWorkItem）を使用して、
  問題やバグを報告してください。
- 報告する際には、以下の情報を含めるようにしてください：
  - **現象の概要**: 問題やバグの内容を簡潔に記述します。
  - **再現手順**: 問題が発生した手順を詳細に記述します。
  - **期待される動作**: 問題がなかった場合の期待される動作を記述します。
  - **エラーメッセージ**: 必要に応じてエラーメッセージを添付してください。
  - **環境情報**: 使用しているPythonやAnsibleのバージョン、OSやiRMC・BIOSのバージョンなど、関連する環境情報を提供してください。

### 4.2 機能の提案

- GitHubのIssue（もしくは社内開発用のGitリポジトリのFeatureのWorkItem）を使用して、新機能や改善点の提案を行ってください。
- 提案内容には、以下の情報を含めてください：
  - **提案の概要**: 追加したい機能や改善したい点について簡潔に記述します。
  - **目的**: 提案の目的や、それによって解決される課題を説明します。

---

## 5. コーディング規約

開発の効率化とコードの品質向上を目的として、以下のコーディング規約を採用しています。

### 5.1 全般

- `.editorconfig`で全体的なコーディングスタイルを定義しています。
- `.editorconfig`は[EditorConfig](https://editorconfig.org/)対応のIDEやエディタで適用されます。
- プロジェクトに参加する開発者は、対応ツールの使用を推奨します。

### 5.2 Python

- [Ruff](https://docs.astral.sh/ruff/)を使ってください。
  Ruffの設定は`pyproject.toml`に記述してあります。
- コードのチェックには以下のコマンドを使用してください：

  ```shell
  ruff check ./plugins/filter/email_alert_profile_filters.py
  ```

### 5.3 Ansible

- Ansibleコードの静的解析ツールとして`ansible-lint`を使用します：

  ```shell
  ansible-lint ./roles/irmc_email_alert
  ```

- 修正が難しい指摘もある（たとえば`platforms`に記述できる機器・OSには制限がある）ため、
  警告を完全に取り除くこと出来ません。
  対応可能な箇所だけ対応するようにして下さい。
- 設定ファイル（`.ansible-lint`）で警告の制御を行うことが可能です。

### 5.4 コーディング規約の適用

- いずれの検証ツールも2024/07から適用開始したため、
  古いコードについては警告が残っている場合があります。
- また、運用期間が浅いこともあり、各警告の有効・無効化や制限値については、
  調整の余地があると思われます。
  チーム内で相談しながら適用ルールは調整しながら最適化を進めてください。

---

## 6. テスト

### 6.1 現在の状況

- 既存の単体テストコードは`./tests`ディレクトリに配置されていますが、
  十分に整備されていません。（2024/12現在）

### 6.2 今後の方針

#### テスト対象の分離

- iRMC機器へのリクエスト部分と、それ以外のロジック部分を分離する設計を進めて下さい。
- 特にロジック部分はレグレッションテストの対象とし、メンテナンス性を向上させます。
- ロジック部分に関しては、単体テストのカバレッジを向上させ、安定性の確保を重視します。

#### Moleculeの活用

- [Molecule](https://ansible.readthedocs.io/projects/molecule/)などを利用したテスト環境の整備を視野に入れてください。
- ただし、以下の制約がある点を考慮してください:
  - テスト対象の大半がiRMC機器向けのAPIであるため、Dockerなどの仮想環境では対応が難しい。
  - 実機を用意し、Moleculeのdelegatedドライバを使用してテストを実行する必要がある。
  - 開発機材であるiRMC機器を借用している現状では、
    中長期的なレグレッションテストに借用機材を組み込むことは現実的ではない。
- 短期的なテストのために「枠組みだけ」用意しておくこともプランの一つとして考えられます。

---

## 7. ドキュメント

- 利用者が目にすることになるドキュメントは英語（マニュアルやAnsible実行メッセージ）で記述してください。
- 開発者のみが目にすることになるドキュメント（本書やコード中の詳細コメント）は日本語で記述してください。

---

## 8. ライセンス

GPL-3.0-or-later
