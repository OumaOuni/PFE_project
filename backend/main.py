from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.auth_route import router as auth_router
from backend.routes.dashboard import router as dashboard_router

app = FastAPI()

# Allow frontend (UI5) to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include authentication routes
app.include_router(auth_router)
app.include_router(dashboard_router)

@app.get("/")
def root():
    return {"message": "Backend is running"}