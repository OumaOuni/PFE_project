from passlib.context import CryptContext
from backend.database import SessionLocal
from backend.models.user_model import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# List of users you want to create
users_to_create = [
    {"username": "oumaima", "password": "1234", "role": "admin"},
    {"username": "oussama", "password": "1234", "role": "ceo"},
    {"username": "rym", "password": "1234", "role": "sales_manager"},
    {"username": "henda", "password": "1234", "role": "inventory_manager"},
    {"username": "taher", "password": "1234", "role": "sales_manager"}
]

db = SessionLocal()

for u in users_to_create:
    hashed_password = pwd_context.hash(u["password"])
    new_user = User(
        username=u["username"],
        password=hashed_password,
        role=u["role"]
    )
    db.add(new_user)
    print(f"Created user: {u['username']} with role: {u['role']}")

db.commit()
db.close()

print("All users created successfully!")