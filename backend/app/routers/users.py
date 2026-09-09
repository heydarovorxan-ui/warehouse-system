from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.schemas.login import LoginRequest
from app.security import create_access_token, require_roles

router = APIRouter()


@router.post("/users", response_model=UserResponse)
def create_user(
    user: UserCreate,
    current_user = Depends(require_roles("admin")),
    db: Session = Depends(get_db)
):
    new_user = User(
        username=user.username,
        password=user.password,
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/users", response_model=list[UserResponse])
def get_users(
    current_user = Depends(require_roles("admin")),
    db: Session = Depends(get_db)
):
    users = db.query(User).all()

    return users


@router.put("/users/{user_id}/reset-password")
def reset_password(
    user_id: int,
    new_password: str,
    current_user = Depends(require_roles("admin")),
    db: Session = Depends(get_db)
):
    user = db.get(User, user_id)

    if user is None:
        return {
            "message": "User not found"
        }

    user.password = new_password

    db.commit()

    return {
        "message": "Password reset successfully"
    }


@router.post("/login")
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.username == login_data.username)
        .first()
    )

    if user is None:
        return {
            "message": "Invalid username or password"
        }

    if user.password != login_data.password:
        return {
            "message": "Invalid username or password"
        }

    token = create_access_token(
        {
            "username": user.username,
            "role": user.role
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role
    }


@router.post("/login/oauth2")
def login_oauth2(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.username == form_data.username)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if user.password != form_data.password:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    token = create_access_token(
        {
            "username": user.username,
            "role": user.role
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }