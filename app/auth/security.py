import bcrypt

# on create
def hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed.decode()

# on attempted login
def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

# created_access_token()?

# change password()
def change_password(current_password: str, new_password: str) -> None:
    raise NotImplementedError

# change_role()? admin only