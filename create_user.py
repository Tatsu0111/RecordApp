from database import Session
from sqlalchemy import text


session = Session()

try:
    # 最初のユーザーを取得
    user_id = session.execute(
        text("SELECT id FROM users ORDER BY id LIMIT 1")
    ).scalar()

    if user_id is None:
        print("ユーザーが存在しません")
        exit()

    print(f"既存データを user_id={user_id} に紐付けます")

    # places に user_id を追加
    session.execute(
        text("ALTER TABLE places ADD COLUMN user_id INTEGER")
    )

    # categories に user_id を追加
    session.execute(
        text("ALTER TABLE categories ADD COLUMN user_id INTEGER")
    )

    # 既存データを最初のユーザーに紐付け
    session.execute(
        text("UPDATE places SET user_id = :user_id"),
        {"user_id": user_id}
    )

    session.execute(
        text("UPDATE categories SET user_id = :user_id"),
        {"user_id": user_id}
    )

    session.commit()

    print("user_id の追加と既存データの紐付けが完了しました")

except Exception as e:
    session.rollback()
    print("エラーが発生しました")
    print(e)

finally:
    session.close()