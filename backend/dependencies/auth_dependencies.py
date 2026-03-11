from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from backend.utils.security import decode_token
from backend.database import SessionLocal
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")




def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    username = payload.get("sub")
    role = payload.get("role")

    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    return {"username": username, "role": role}

def require_role(required_role: str):
    def role_checker(current_user = Depends(get_current_user)):
        if current_user["role"] != required_role:
            raise HTTPException(status_code=403, detail="Access forbidden")
        return current_user
    return role_checker