from datetime import date, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Contact
from app.schemas import ContactCreate, ContactResponse, ContactUpdate

router = APIRouter(prefix="/contacts", tags=["Contacts"])


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
def create_contact(payload: ContactCreate, db: Session = Depends(get_db)):
    contact = Contact(**payload.model_dump())
    db.add(contact)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="A contact with this email already exists")
    db.refresh(contact)
    return contact


@router.get("/", response_model=list[ContactResponse])
def list_contacts(
    search: str | None = Query(default=None, description="Пошук за ім'ям, прізвищем або email"),
    db: Session = Depends(get_db),
):
    query = db.query(Contact)
    if search:
        term = f"%{search.strip()}%"
        query = query.filter(or_(
            Contact.first_name.ilike(term),
            Contact.last_name.ilike(term),
            Contact.email.ilike(term),
        ))
    return query.order_by(Contact.id).all()


@router.get("/birthdays", response_model=list[ContactResponse])
def upcoming_birthdays(db: Session = Depends(get_db)):
    today = date.today()
    end = today + timedelta(days=7)
    contacts = db.query(Contact).all()

    def occurs_soon(contact):
        birthday = contact.birthday
        try:
            next_birthday = birthday.replace(year=today.year)
        except ValueError:  # 29 лютого у невисокосному році
            next_birthday = date(today.year, 2, 28)
        if next_birthday < today:
            try:
                next_birthday = birthday.replace(year=today.year + 1)
            except ValueError:
                next_birthday = date(today.year + 1, 2, 28)
        return today <= next_birthday <= end

    return sorted((c for c in contacts if occurs_soon(c)),
                  key=lambda c: (c.birthday.month, c.birthday.day))


@router.get("/{contact_id}", response_model=ContactResponse)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.get(Contact, contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
def update_contact(contact_id: int, payload: ContactUpdate, db: Session = Depends(get_db)):
    contact = db.get(Contact, contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(contact, key, value)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="A contact with this email already exists")
    db.refresh(contact)
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.get(Contact, contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
