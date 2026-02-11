from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.user_schema import ResetPasswordRequest
from app.services.auth_service import verify_reset_token, hash_password
from app.services.user_service import get_user_by_email
from app.core.database import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/reset-password")   
def reset_password(
    data: ResetPasswordRequest,
    db: Session = Depends(get_db),
):
    email = verify_reset_token(data.token)
    print("EMAIL FROM TOKEN:", email)

    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.hashed_password = hash_password(data.new_password)
    db.commit()

    return {"message": "Password reset successful"}
