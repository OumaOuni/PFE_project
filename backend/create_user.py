from passlib.context import CryptContext
from backend.database import SessionLocal
from backend.models.user_model import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

users_to_create = [
    {"username": "oussama", "password": "ceo123",   "role": "ceo",               "full_name": "Oussama Mansouri", "email": "oussama@luxdecor.com"},
    {"username": "rym",     "password": "sales123", "role": "sales_manager",     "full_name": "Rym Bouaziz",      "email": "rym@luxdecor.com"},
    {"username": "henda",   "password": "stock123", "role": "inventory_manager", "full_name": "Henda Slim",       "email": "henda@luxdecor.com"},
    {"username": "admin",   "password": "admin123", "role": "admin",             "full_name": "IT Admin",         "email": "admin@luxdecor.com"},
]

db = SessionLocal()

for u in users_to_create:
    hashed_password = pwd_context.hash(u["password"])
    new_user = User(
        username=u["username"],
        password=hashed_password,
        role=u["role"],
        full_name=u["full_name"],
        email=u["email"],
    )
    db.add(new_user)
    print(f"Created user: {u['username']} with role: {u['role']}")

db.commit()
db.close()

print("All users created successfully!")
