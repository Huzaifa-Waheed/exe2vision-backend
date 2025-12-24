from fastapi import FastAPI
from app.database.init_db import init_db
from app.api import auth, scan, admin

app = FastAPI(title="Exe2Vision API")

# Register routers
app.include_router(auth.router)
app.include_router(scan.router)
app.include_router(admin.router)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def root():
    return {"status": "Database Connected"}
