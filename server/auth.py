import bcrypt
import base64
import uuid
import db
from tinydb import Query
import jwt
import time
import schema

from typing import TypedDict

JWTClaim = TypedDict("JWTClaim", {
    "sub_id": str,
    "sub": str,
    "exp": int
})

def new_uuid() -> str:
    return str(uuid.uuid4())


def register(username: str, password: str, displayname: str) -> bool:
    hashed_pw = base64.b64encode(
        bcrypt.hashpw(password.encode(), bcrypt.gensalt(12))
    ).decode()
    uid = new_uuid()
    db.AuthStore.insert(schema.AuthenticationEntry(userID=uid, hashedPassword=hashed_pw))

    db.UserStore.insert(
        schema.User(
            userID=uid,
            username=username,
            displayname=displayname,
            public=True,
            disabled=False,
            achievements=schema.UserAchievements(badges=[], leveling=[]),
            metrics=schema.UserMetrics(health=100, energy=0, exp=0),
            social=schema.UserSocialLink(facebook="", threads="", tiktok=""),
            relationships=[],
            habits=[],
            todos=[],
            creationTimestamp=round(time.time())
        )
    )

    return True


def login(username: str, password: str) -> tuple[bool, schema.User | None, str]:
    if result := db.UserStore.query_first(Query().username == username):
        if rp := db.AuthStore.query_first(Query().userID == result.userID):
            if bcrypt.checkpw(
                password.encode(), base64.b64decode(rp.hashedPassword)
            ):
                return True, result, "OK"
            return False, None, "Incorrect password"
        return False, None, "UNREACHABLE: User defined, but authentication info wasn't"
    return False, None, "User not found"


def generate_token(username: str, uid: str, private_key: str) -> str:
    return jwt.encode(
        {
            "sub_id": uid,
            "sub": username,
            "exp": round(time.time()) + 60 * 60,
        },
        private_key,
        algorithm="RS256",
    )


def verify_token(token: str, private_key: str) -> tuple[bool, JWTClaim, str]:
    try:
        return True, jwt.decode(token, private_key, algorithms=["RS256"]), "OK"
    except jwt.InvalidSignatureError:
        return False, {}, "OK"  # type: ignore
    except jwt.DecodeError as e:
        return False, {}, f"JWT token parsing error: {e}"  # type: ignore
