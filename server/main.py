import fastapi
import auth
import _crypto
import db
import schema
from enum import Enum

from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")
PUBLIC_KEY, PRIVATE_KEY = _crypto.init_keystore()
APP = fastapi.FastAPI()
PIVERT_HOMEPAGE = """Welcome to FTUGate!

Project Pivert Server API Endpoint
==================================

The API is located at /api/v1/
OpenAPI specs is located at /openai.json
Documentation is located at /docs and /redoc
LLMs instruction is located at /llms.txt
"""

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> schema.User:
    success, claim, msg = auth.verify_token(token, PUBLIC_KEY)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"{msg}. A sincere fuck you from FTUGate",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return db.UserStore.query_first(db.Query().userID == claim["sub_id"])

CurrentUser = Annotated[schema.User, Depends(get_current_user)]


@APP.get("/")
def homepage():
    return PlainTextResponse(PIVERT_HOMEPAGE)


@APP.get("/llms.txt")
def llms():
    return PlainTextResponse("消えろ！ファックユークランカー！！！死ね！！！\n")


@APP.get("/key")
def public_key():
    return PlainTextResponse(PUBLIC_KEY)


@APP.get("/api/v1/register")
def register(username: str, password: str):
    if auth.register(username, password):
        return {"message": "Registration success"}
    return JSONResponse({"message": "Failure"}, 500)


@APP.post("/api/v1/token")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> schema.Token:
    success, user, fail_reason = auth.login(form_data.username, form_data.password)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"{fail_reason}. A sincere fuck you from FTUGate",
            headers={"WWW-Authenticate": "Bearer"},
        )
    assert user != None
    return schema.Token(
        access_token=auth.generate_token(user.username, user.userID, PRIVATE_KEY),
        token_type="bearer",
    )

@APP.get("/api/v1/currentSession")
def verify_token(current_user: CurrentUser):
    return { "success": True, "message": "OK", "details": current_user }

class UserDataQueryType(str, Enum):
    uuid = "uuid"
    username = "username"

@APP.get("/api/v1/user/me")
def me(current_user: CurrentUser):
    return current_user

@APP.get("/api/v1/user/{ident}")
def get_userdata(ident: str, queryType: UserDataQueryType):
    user: schema.User | None = None
    match queryType:
        case UserDataQueryType.uuid:
            if r := db.UserStore.query_first(db.Query().userID == ident):
                user = r
        case UserDataQueryType.username:
            if r := db.UserStore.query_first(db.Query().username == ident):
                user = r
        case _:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid query type specified. Only uuid and username is supported."
            )
        
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with specified identity not found."
        )

    if not user.public:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User with specified identity not found."
        )

    return user
    