from sqlalchemy import text
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_all_users(db):
    rows = db.execute(text("""
        SELECT id, username, role, full_name, email, is_active
        FROM luxury.users
        ORDER BY id
    """)).fetchall()
    return [
        {
            "id": r.id,
            "username": r.username,
            "role": r.role,
            "full_name": r.full_name,
            "email": r.email,
            "is_active": r.is_active,
        }
        for r in rows
    ]


def create_user(db, data: dict):
    hashed = pwd_context.hash(data["password"])
    db.execute(
        text("""
            INSERT INTO luxury.users (username, password, role, full_name, email)
            VALUES (:username, :password, :role, :full_name, :email)
        """),
        {
            "username": data["username"],
            "password": hashed,
            "role": data["role"],
            "full_name": data.get("full_name", ""),
            "email": data.get("email", ""),
        },
    )
    db.commit()
    return {"message": "User created"}


def update_user(db, user_id: int, data: dict):
    if data.get("password"):
        hashed = pwd_context.hash(data["password"])
        db.execute(
            text("""
                UPDATE luxury.users
                SET username=:username, role=:role, full_name=:full_name,
                    email=:email, password=:password
                WHERE id=:id
            """),
            {
                "username": data["username"],
                "role": data["role"],
                "full_name": data.get("full_name", ""),
                "email": data.get("email", ""),
                "password": hashed,
                "id": user_id,
            },
        )
    else:
        db.execute(
            text("""
                UPDATE luxury.users
                SET username=:username, role=:role, full_name=:full_name, email=:email
                WHERE id=:id
            """),
            {
                "username": data["username"],
                "role": data["role"],
                "full_name": data.get("full_name", ""),
                "email": data.get("email", ""),
                "id": user_id,
            },
        )
    db.commit()
    return {"message": "User updated"}


def delete_user(db, user_id: int):
    db.execute(text("DELETE FROM luxury.users WHERE id=:id"), {"id": user_id})
    db.commit()
    return {"message": "User deleted"}
