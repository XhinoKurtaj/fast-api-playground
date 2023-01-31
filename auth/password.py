from passlib.context import CryptoContext

pwd_context = CryptoContext(schemes=['bcrypt'], deprecated='auto')

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)