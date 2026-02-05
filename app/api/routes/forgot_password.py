from fastapi import Depends, HTTPException, status, BackgroundTasks, APIRouter
from sqlalchemy.orm import Session
from app.core.security import create_reset_token
from app.schemas.user_schema import ForgetPasswordRequest
from app.core.database import get_db
from app.crud.user_crud import get_user_by_email
import os
from fastapi_mail import FastMail, MessageSchema, MessageType, ConnectionConfig
from starlette.responses import JSONResponse
from dotenv import load_dotenv

load_dotenv()

FORGET_PASSWORD_EXPIRE_MINUTES = int(
        os.getenv("FORGET_PASSWORD_EXPIRE_MINUTES", 10))

router = APIRouter(prefix="/auth", tags=["Auth"])

mail_conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),   
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),   
    MAIL_FROM=os.getenv("MAIL_FROM"),           
    MAIL_FROM_NAME="MY APP",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER="app/templates/mail",
)


@router.post("/forget_password")
async def forgot_password(
    background_tasks: BackgroundTasks,
    data: ForgetPasswordRequest,
    db: Session = Depends(get_db)
):
    try:
        user = get_user_by_email(db, data.email)

        if user:
            token = create_reset_token(
                user.email, expires_minutes=FORGET_PASSWORD_EXPIRE_MINUTES)

            forgot_url_link = (
                                f"http://localhost:3000/reset-password?"
                                f"token={token}"
                            )       

            message = MessageSchema(
                subject="Password Reset Instructions",
                recipients=[data.email],
                template_body={
                    "link_expiry_min": FORGET_PASSWORD_EXPIRE_MINUTES,
                    "reset_link": forgot_url_link
                },
                subtype=MessageType.html
            )

            fm = FastMail(mail_conf)
            background_tasks.add_task(
                fm.send_message,
                message,
                template_name="password_reset.html"
            )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "If this email exists,"
                "a password reset link has been sent.",
                "success": True
            }
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something unexpected happened"
        )