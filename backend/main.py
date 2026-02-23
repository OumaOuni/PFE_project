from fastapi import FastAPI
from backend.routes.auth_route import router as auth_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Important pour SAP UI5 (sinon erreur CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)