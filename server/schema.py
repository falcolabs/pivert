import tinydb
from abc import ABC, abstractmethod
from pydantic import BaseModel
from pydantic_core import from_json

from tinydb.table import Table
from typing import (
    TypeAlias,
    Literal,
    Optional,
    Generic,
    TypeVar,
    Union, Mapping, Callable, Iterable,
    Any,
)

UserUUID: TypeAlias = str
RelationshipUUID: TypeAlias = str
HabitUUID: TypeAlias = str
TodoUUID: TypeAlias = str
BadgeUUID: TypeAlias = str
CategoryID: TypeAlias = str
RelationshipLevel = Literal["none", "friends", "close"]
T = TypeVar("T", bound=BaseModel)

class UserMetrics(BaseModel):
    health: int
    energy: int
    exp: int

class UserSocialLink(BaseModel):
    facebook: str
    threads: str
    tiktok: str

class LevelingStatus(BaseModel):
    category: CategoryID
    progress: float

class UserAchievements(BaseModel):
    badges: list[BadgeUUID]
    leveling: list[LevelingStatus]

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    userID: UserUUID
    username: str
    displayname: Optional[str]
    public: bool
    disabled: bool
    creationTimestamp: int

    metrics: UserMetrics
    social: UserSocialLink
    achievements: UserAchievements

    relationships: list[RelationshipUUID]
    habits: list[HabitUUID]
    todos: list[TodoUUID]

class AuthenticationEntry(BaseModel):
    userID: UserUUID
    hashedPassword: str

class Relationship(BaseModel):
    target: UserUUID
    level: RelationshipLevel

class TaskReward(BaseModel):
    health: int
    energy: int
    exp: int

class Habit(BaseModel):
    taskID: HabitUUID
    name: str
    description: Optional[str]
    congratsMessage: str
    rewards: TaskReward

class Todo(BaseModel):
    taskID: TodoUUID
    name: str
    description: Optional[str]
    congratsMessage: Optional[str]
    rewards: TaskReward
    deadline: int
    completed: bool

class ShortcutTasks(BaseModel):
    habits: list[Habit]
    todos: list[Todo]

class QueryResultMultiple(tuple[T]):
    def __new__(cls, *args: T):
        return super().__new__(cls, args)

    def is_empty(self):
        return len(self) == 0

    def __bool__(self):
        return len(self) != 0

    __nonzero__ = __bool__


class QueryResultSingle(Generic[T]):
    __inner__: BaseModel

    def __init__(self, inner: BaseModel):
        self.__inner__ = inner

    def is_empty(self):
        return self.__inner__ is None

    def __bool__(self):
        if self.__inner__:
            return True
        return False 

    def __getattribute__(self, name: str) -> Any:
        if name in ("__inner__", "is_empty", "__bool__"): return object.__getattribute__(self, name)
        return getattr(self.__inner__, name)

    __nonzero__ = __bool__


class TypedTable(Generic[T], ABC):
    table: Table

    def __init__(self, t: Table):
        self.table = t

    def insert(self, obj: T) -> int:
        return self.table.insert(obj.model_dump())  # type: ignore[reportArgumentType]

    def query(
        self, cond: tinydb.queries.QueryLike, n: int | None = None
    ) -> tuple[T]:
        if n is None:
            return QueryResultMultiple(*[from_json(i) for i in self.table.search(cond)])  # type: ignore[reportReturnType]
        else:
            return QueryResultMultiple(*[from_json(i) for i in self.table.search(cond)[:n]])  # type: ignore[reportReturnType]

    @property
    @abstractmethod
    def model(self) -> type[T]:
        ...

    def query_first(
        self, cond: tinydb.queries.QueryLike
    ) -> T:
        result = self.table.search(cond)
        return QueryResultSingle(self.model.model_validate(result[0]) if len(result) >= 1 else None)  # type: ignore[reportReturnType]

    def update(
        self,
        fields: Union[Mapping, Callable[[Mapping], None]],
        cond: Optional[tinydb.queries.QueryLike] = None,
        doc_ids: Optional[Iterable[int]] = None,
    ) -> list[int]:
        return self.table.update(fields, cond, doc_ids)


class __AuthStore(TypedTable[AuthenticationEntry]):
    @property
    def model(self):
        return AuthenticationEntry

class __UserStore(TypedTable[User]):
    @property
    def model(self):
        return User

class __HabitsStore(TypedTable[Habit]):
    @property
    def model(self):
        return Habit

class __TodosStore(TypedTable[Todo]):
    @property
    def model(self):
        return Todo

class __RelationshipStore(TypedTable[Relationship]):
    @property
    def model(self):
        return Relationship
