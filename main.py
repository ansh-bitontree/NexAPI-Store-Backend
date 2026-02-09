from fastapi import FastAPI
from app.api.routes.auth_routes import router as auth_router
from app.api.routes.forgot_password import router as forgot_password_router
from app.api.routes.reset_password import router as reset_password_router
from app.api.routes.user_routes import router as user_router
from app.api.routes.product_routes import router as product_router
from app.core.database import engine, Base
from app.core.config import settings
from app.middleware.cors import setup_cors

Base.metadata.create_all(bind=engine)

app = FastAPI(title="NextAPI", version="1.0.0")

app.include_router(auth_router)
app.include_router(forgot_password_router)
app.include_router(reset_password_router)
app.include_router(user_router)
app.include_router(product_router)

setup_cors(app, settings.FRONTEND_BASE_URL)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
