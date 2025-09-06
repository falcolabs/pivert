import fastapi
import auth
import _crypto
import db
import schema
import pivert_resource
from enum import Enum

from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")
PUBLIC_KEY, PRIVATE_KEY = _crypto.init_keystore()
APP = fastapi.FastAPI()
PIVERT_HOMEPAGE = """Welcome to FTUGate!

Project Pivert Server API Endpoint
==================================

The API is located at /api/v1/
OpenAPI specs is located at /openapi.json
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


class UserDataQueryType(str, Enum):
    uuid = "uuid"
    username = "username"


class TaskType(str, Enum):
    todo = "todo"
    habit = "habit"


APP.mount("/static", StaticFiles(directory="./static/"), name="static")


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
def register(username: str, password: str, displayname: str):
    print("dname:", repr(displayname))
    if auth.register(username, password, displayname):
        return {"message": "Registration success"}
    raise HTTPException(status_code=500, detail="Failure")


@APP.post("/api/v1/token")
def login_formdata(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> schema.Token:
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


class AuthBodyJSON(schema.BaseModel):
    username: str
    password: str


@APP.post("/api/v1/login")
def login(data: AuthBodyJSON) -> schema.Token:
    success, user, fail_reason = auth.login(data.username, data.password)
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
def verify_token(_: CurrentUser):
    return {
        "success": True,
        "message": "OK",
    }


@APP.get("/api/v1/user/me")
def me(current_user: CurrentUser) -> schema.User:
    return current_user


@APP.get("/api/v1/user/{ident}")
def get_userdata(ident: str, queryType: UserDataQueryType) -> schema.User:
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
                detail="Invalid query type specified. Only uuid and username is supported.",
            )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with specified identity not found.",
        )

    if not user.public:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User profile is not public.",
        )

    return user


@APP.get("/api/v1/complete/{task_type}/{task_id}")
def complete_task(
    current_user: CurrentUser, task_type: TaskType, task_id: str
) -> schema.User:
    match task_type:
        case TaskType.todo:
            if r := db.TodosStore.query_first(db.Query().taskID == task_id):
                nm = schema.UserMetrics(
                    health=current_user.metrics.health + r.rewards.health,
                    energy=current_user.metrics.energy + r.rewards.energy,
                    xp=current_user.metrics.xp + r.rewards.xp,
                    allTimeXP=current_user.metrics.allTimeXP + r.rewards.xp,
                )
                db.UserStore.update(
                    {"metrics": nm.model_dump()},
                    db.Query().userID == current_user.userID,
                )
                db.TodosStore.update({"completed": True}, db.Query().taskID == r.taskID)
                current_user.metrics = nm
                return current_user
        case TaskType.habit:
            if r := db.HabitsStore.query_first(db.Query().taskID == task_id):
                nm = schema.UserMetrics(
                    health=current_user.metrics.health + r.rewards.health,
                    energy=current_user.metrics.energy + r.rewards.energy,
                    xp=current_user.metrics.xp + r.rewards.xp,
                    allTimeXP=current_user.metrics.allTimeXP + r.rewards.xp,
                )
                db.UserStore.update(
                    {"metrics": nm.model_dump()},
                    db.Query().userID == current_user.userID,
                )
                current_user.metrics = nm
                return current_user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"The provided id does not point to any existing {task_type.value}s",
    )


@APP.post("/api/v1/create/habit")
def create_habit(current_user: CurrentUser, habit: schema.Habit) -> str:
    h = habit.model_dump()
    h["taskID"] = auth.new_uuid()
    db.HabitsStore.insert(schema.Habit.model_validate(h))
    db.UserStore.update(
        {
            "habits": current_user.habits
            + [
                h["taskID"],
            ]
        },
        db.Query().userID == current_user.userID,
    )
    return h["taskID"]


@APP.post("/api/v1/create/todo")
def create_todo(current_user: CurrentUser, todo: schema.Todo) -> str:
    t = todo.model_dump()
    t["taskID"] = auth.new_uuid()
    db.HabitsStore.insert(schema.Habit.model_validate(t))
    db.UserStore.update(
        {
            "todos": current_user.todos
            + [
                t["taskID"],
            ]
        },
        db.Query().userID == current_user.userID,
    )
    return t["taskID"]


@APP.get("/api/v1/shortcuts/tasks")
def shortcut_tasks(current_user: CurrentUser) -> schema.ShortcutTasks:
    return schema.ShortcutTasks(
        todos=list(
            map(
                lambda t: db.TodosStore.query_first(db.Query().taskID == t),
                current_user.todos,
            )
        ),
        habits=list(
            map(
                lambda t: db.HabitsStore.query_first(db.Query().taskID == t),
                current_user.todos,
            )
        ),
    )

@APP.get("/api/v1/resources/badges/{badgeID}")
def get_badge(badgeID: str):
    if badgeID not in pivert_resource.ALL_BADGES.keys():
        raise HTTPException(status_code=404, detail=f"No badge with id {badgeID} found.")

    return pivert_resource.ALL_BADGES[badgeID]


@APP.get("/api/v1/resources/leveling_categories/{catID}")
def get_leveling_category(catID: str):
    if catID not in pivert_resource.ALL_LEVELING_CATEGORIES.keys():
        raise HTTPException(status_code=404, detail=f"No badge with id {catID} found.")

    return pivert_resource.ALL_LEVELING_CATEGORIES[catID]
