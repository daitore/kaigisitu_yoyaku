main.py
models.pyで設計 Base
SQLAlchemyの親クラス
（models.pyで継承してたやつ）
        ↓
metadataに保存 テーブル設計情報が全部入っている
        ↓
create_all()
        ↓
SQLiteにテーブル作成

API呼び出し
    ↓
get_db()実行 DB接続管理
    ↓
db作成
    ↓
read_users()などに渡す
    ↓
処理終了
    ↓
db.close()

ブラウザ → /users/ にGET
    ↓
FastAPI
    ↓
read_users()
    ↓
crud.get_users() crud.py
    ↓
DB問い合わせ
    ↓
ユーザー一覧取得
    ↓
JSONで返す

response_model は
APIの返り値の設計図
セキュリティフィルター:schemas.User に password が無い場合、passwordは自動で消える
Swaggerの自動ドキュメント生成

FastAPI × SQLAlchemy の核心
| コード        | 役割     |
| create_all | テーブル作成 |
| FastAPI()  | API本体  |
| get_db     | DB接続管理 |
| yield      | DBを渡す  |
| finally    | 接続クローズ |

models,schemas
フロント
   ↓
schemas（入力チェック）
   ↓
models（DB保存）
   ↓
models（DB取得）
   ↓
schemas（出力整形）
   ↓
フロントへ返す