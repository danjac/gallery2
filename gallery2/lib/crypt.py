from passlib.hash import bcrypt


def encrypt_password(password):
    return bcrypt.encrypt(password)


def check_password(password, encrypted):
    try:
        return bcrypt.verify(password, encrypted)
    except TypeError:
        return False
