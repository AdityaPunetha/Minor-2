from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import user, auth, appointment


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(user.router)
app.include_router(auth.router)
app.include_router(appointment.router)


@app.get("/")
def root():
    return {"message": "Hello World"}


# uvicorn app.main:app --reload
