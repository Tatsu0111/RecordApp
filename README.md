# 収支管理アプリ
https://recordappweb.onrender.com/
<img width="1887" height="915" alt="image" src="https://github.com/user-attachments/assets/4a5110e9-c705-4cdb-9d52-118c97b2d10c" />

## 概要
様々なカテゴリや場所についての収支を一元管理し、項目別に集計・分析することができるアプリです。

## 目的
- データベースの扱いを学ぶ
- Webアプリ制作について学ぶ

## 開発環境
- WSL2 / Ubuntu
- VSCode
- Git / GitHub

## 使用ツール
- Python3
  
→ 機械学習やデータ分析などで用いられる、汎用性の高いオブジェクト指向型プログラミング言語

　アプリのバックエンド処理や収支計算に使用
- HTML

→ Webページの構造を定義するマークアップ言語

　画面のレイアウトや入力フォームなどの作成に使用
- CSS

→ Webページのデザインを指定するスタイルシート言語

　文字・色・配置・ボタンなどの装飾に使用
- Flask

→ Python製の軽量Webアプリケーションフレームワーク

　URLのルーティングやフォーム処理など、Webアプリの基本機能に使用
- jinja2

→ Pythonで利用されるテンプレートエンジン

　HTMLへのデータ表示や条件分岐など、画面生成に使用
- Plotly

→ インタラクティブなグラフ作成ライブラリ

　収支や累積収支などのデータの可視化に使用
- SQLite

→ 軽量なデータベース

　ローカル環境でのデータ保存に使用
- SQLAlchemy

→ Python向けのORM

　データベースへのデータ登録・取得・更新・削除などに使用
- Render

→ クラウド上でWebアプリを公開できるサービス

　アプリのデプロイ・公開に使用
- Supabase

→ PostgreSQLを利用したクラウドデータベースサービス

　本番環境でのデータ保存に使用

## データベース設計
- records

→ 収支記録を管理するテーブル

　日付・タイトル・投資額・回収額・メモなどを保存
- users

→ ユーザー情報を管理するテーブル

　ユーザー名やパスワード情報を保存
- categories

→ ギャンブル種別を管理するテーブル

　パチンコ・スロット・競馬などの分類を保存
- places

→ 店舗・開催場所などを管理するテーブル

　収支記録に紐づく場所情報を保存

## 機能
### ユーザー関連
<img width="1695" height="289" alt="image" src="https://github.com/user-attachments/assets/ea800b9d-41ce-4080-8a8b-12d794e887cc" />

- ユーザー登録機能

→ ユーザー名・パスワードを登録
<img width="1721" height="291" alt="スクリーンショット 2026-09-16 173403" src="https://github.com/user-attachments/assets/7fbc4d6c-031e-4c8d-8b1b-27020c1591a2" />

- ログイン機能

→ 登録したユーザーでログイン
<img width="1695" height="289" alt="image" src="https://github.com/user-attachments/assets/29d46c6c-b930-4bb9-9f5e-4ad08e071528" />

- ログアウト機能

→ ログイン状態を解除

### 収支関連
- 収支登録機能

→ パチンコ・スロット・競馬などの収支を登録
<img width="1818" height="689" alt="image" src="https://github.com/user-attachments/assets/f8c46482-ac41-49ed-951d-1e5fa6a87e78" />

- 収支一覧表示機能

→ 登録した収支を一覧表示
<img width="1814" height="618" alt="image" src="https://github.com/user-attachments/assets/f858540d-cd8e-49b2-bf80-faf05801fdeb" />

- 収支編集・削除機能

→ 登録済みの収支を編集・削除
- 収支検索・絞り込み機能

→ 日付・カテゴリ・店舗・タイトルなどから収支を検索
- 収支分析機能

→ 年・月・日・カテゴリ・店舗などの単位で収支を集計・可視化
<img width="1868" height="765" alt="image" src="https://github.com/user-attachments/assets/afff9345-71e7-446d-9ee2-3c0539377999" />

### マスタ管理
- カテゴリ管理機能

→ パチンコ・スロット・競馬などのカテゴリを登録・編集・削除
<img width="1841" height="560" alt="image" src="https://github.com/user-attachments/assets/ca1ae85b-a8e2-49a4-8b5f-0091a0a04b01" />

- 店舗管理機能

→ 店舗・開催場所を登録・編集・削除
<img width="1705" height="680" alt="image" src="https://github.com/user-attachments/assets/10b34fac-455d-49c7-b2ec-174e3cf4e9c2" />

### その他
おみくじ機能

→ その日の運勢を表示
<img width="1802" height="657" alt="image" src="https://github.com/user-attachments/assets/3017175b-5078-4d89-87fb-2697acca2f9c" />

## 成果
### データベースの扱い
- データベース設計の理解

→ 収支・ユーザー・カテゴリ・店舗などのデータ構造を設計し、テーブル間の関係を整理できるようになった
- SQLAlchemyによるデータ操作の習得

→ ORMを利用したデータの登録・取得・更新・削除や、条件検索・集計などを実装することで、習得できた
- データベースの移行経験

→ ローカルのSQLiteから、クラウド上のPostgreSQL（Supabase）へ移行し、環境に応じたデータベースの扱いを学べた

### Webアプリ制作
- Flaskを用いたWebアプリ開発の理解

→ URLごとの処理やGET・POST、フォーム処理など、Webアプリの基本的な仕組みを理解できた
- 処理の分離

→ ルーティング・テンプレート・データベース処理などを分離し、役割を意識した構成で開発し、実際のモデルのような開発ができた
- ユーザーごとのデータ管理

→ ログイン機能を実装し、ユーザーごとに収支データを分離して管理できるようにすることで、認証処理について理解できた
- Webアプリの公開経験

→ RenderとSupabaseを利用して、作成したWebアプリをクラウド上に公開する一連の流れを体感できた
