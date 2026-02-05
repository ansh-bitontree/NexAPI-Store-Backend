from fastapi import FastAPI
from app.api.routes.auth_routes import router as auth_router
from app.core.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
