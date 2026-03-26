
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.router import router as v1_router
#from app.db.init_db import init_db

# 1️⃣ Criar a app FastAPI
app = FastAPI(
    title="Mini-SIEM",
    version="0.1.0"
)

# 2️⃣ CORS (frontend poder chamar o backend)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=["*"]
)


# 3️⃣ Ligar os endpoints (/health, /ingest, etc.)
app.include_router(v1_router, prefix="/api/v1")

# 4️⃣ Código que corre quando a app arranca
#@app.on_event("startup")
#def on_startup():
 #   init_db()
