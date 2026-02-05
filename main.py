from fastapi import FastAPI
from app.api.routes.auth_routes import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.api.routes.forgot_password import router as forgot_password_router
from app.api.routes.reset_password import router as reset_password_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth_router)
app.include_router(forgot_password_router)
app.include_router(reset_password_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
