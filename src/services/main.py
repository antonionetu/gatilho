from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from models import Password
import util

app = FastAPI()


@app.get("/status")
async def get_status(db: Session = Depends(util.get_db)):
    return {"working": True}


@app.post("/create")
async def create_password(guest: str, slug: str, db: Session = Depends(util.get_db)):
    if not util.is_guest_valid(db, guest):
        raise HTTPException(status_code=403, detail="Guest is not valid")

    slug = slug.strip().lower().replace(" ", "_")
    password = util.generate_pass()

    new_password = Password(slug=slug, key=password)
    db.add(new_password)
    db.commit()
    db.refresh(new_password)

    return {"slug": new_password.slug}


@app.get("/get/{slug}")
async def get_password(slug: str, guest: str, db: Session = Depends(util.get_db)):
    if not util.is_guest_valid(db, guest):
        raise HTTPException(status_code=403, detail="Guest is not valid")

    password = db.query(Password).filter(Password.slug == slug).first()

    if password is None:
        raise HTTPException(status_code=404, detail="Password not found")

    return {"key": password.key}


@app.get("/search")
async def search_passwords(guest: str, q: str, db: Session = Depends(util.get_db)):
    if not util.is_guest_valid(db, guest):
        raise HTTPException(status_code=403, detail="Guest is not valid")

    query = q.strip().lower().replace(" ", "_")
    passwords = db.query(Password).filter(Password.slug.contains(query)).all()

    return {"keys": [password.slug for password in passwords]}
