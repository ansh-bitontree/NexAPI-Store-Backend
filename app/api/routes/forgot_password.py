from fastapi import Depends, HTTPException, status, BackgroundTasks, APIRouter
from sqlalchemy.orm import Session
from app.services.auth_service import create_reset_token
from app.schemas.user_schema import ForgetPasswordRequest
from app.core.database import get_db
from app.services.user_service import get_user_by_email
from app.core.config import settings
from fastapi_mail import FastMail, MessageSchema, MessageType, ConnectionConfig
from starlette.responses import JSONResponse


FRONTEND_BASE_URL = settings.FRONTEND_BASE_URL

FORGET_PASSWORD_EXPIRE_MINUTES = int(
        settings.FORGET_PASSWORD_EXPIRE_MINUTES)

router = APIRouter(prefix="/auth", tags=["Auth"])

mail_conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,   
    MAIL_PASSWORD=settings.MAIL_PASSWORD,   
    MAIL_FROM=settings.MAIL_FROM,           
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
                f"{FRONTEND_BASE_URL}/reset-password?"
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