import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from . import models, database
from .routers import speedtest

app = FastAPI()

# Path to the static directory
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}

# Create the SQLite database and tables when the app starts
@app.on_event("startup")
def startup_event():
    models.Base.metadata.create_all(bind=database.engine)

# Include the speedtest router
app.include_router(speedtest.router)
