from fastapi import FastAPI
from app.database import Base, engine
from app.routers import contacts

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Contacts API",
    description="REST API для зберігання та управління контактами.",
    version="1.0.0",
)

app.include_router(contacts.router, prefix="/api")


@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Contacts API is running", "docs": "/docs"}
