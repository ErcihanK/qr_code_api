from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime
import logging
from app.config import DEMO_USER
from app.schema import Token
from app.utils.common import create_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    logging.debug(f"Login attempt for user: {form_data.username}")
    user = DEMO_USER.get(form_data.username)
    if not user or form_data.password != user["password"]:
        logging.warning(f"Failed login attempt for user: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generate token
    access_token = create_access_token({"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}
