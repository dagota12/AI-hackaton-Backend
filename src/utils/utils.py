from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pwd(password:str):
    return pwd_context.hash(password)
print(hash_pwd("sample_password"))
print(hash_pwd("sample_password"))
print(pwd_context.verify("sample_password", "$2b$12$rwnUjhczVd2R21Gqz6hW0.y/zj9ZaYopBGMiH5b67oFlKMSLl0R06"))