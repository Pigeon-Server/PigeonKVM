import hashlib
import app.util.Config


def PasswordToMd5(password: str):
    md5 = hashlib.md5(app.util.Config.main_config.get("main").get("Cryptographic_salt").encode())
    md5.update(password.encode('utf-8'))
    return md5.hexdigest()
