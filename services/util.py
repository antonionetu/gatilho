import random
import string

from models import Guest, SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def is_guest_valid(db, guest):
    guest = db.query(Guest).filter(Guest.name == guest).first()

    if guest is None:
        return False

    if not guest.is_valid:
        return False

    return True


def generate_pass():
    # Generate a random password with 99 characters, including letters, digits, and special characters
    return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=99))
