from passlib.context import CryptContext
from backend.database import SessionLocal
from backend.models.user_model import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# List of users you want to create
users_to_create = [
    {"username": "oumaima", "email": "oumaima@luxury.com", "password": "1234", "role": "admin"},
    {"username": "oussama", "email": "oussama@luxury.com", "password": "1234", "role": "ceo"},
    {"username": "rym",     "email": "rym@luxury.com",     "password": "1234", "role": "sales_manager"},
    {"username": "henda",   "email": "henda@luxury.com",   "password": "1234", "role": "inventory_manager"},
    {"username": "taher",   "email": "taher@luxury.com",   "password": "1234", "role": "sales_manager"},
]

db = SessionLocal()

for u in users_to_create:
    existing = db.query(User).filter(User.username == u["username"]).first()
    if existing:
        print(f"Skipped (already exists): {u['username']}")
        continue
    hashed_password = pwd_context.hash(u["password"])
    new_user = User(
        username=u["username"],
        email=u["email"],
        password=hashed_password,
        role=u["role"],
    )
    db.add(new_user)
    print(f"Created user: {u['username']} ({u['role']})")

db.commit()
db.close()
print("Done!")
