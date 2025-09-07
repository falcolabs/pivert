import tinydb
import time
from tinydb.table import Table
from tinydb import Query
import schema

_DB = tinydb.TinyDB("db.json")
AuthStore: schema.TypedTable[schema.AuthenticationEntry] = schema.__AuthStore(
    _DB.table("auth")
)
UserStore: schema.TypedTable[schema.User] = schema.__UserStore(_DB.table("users"))
HabitsStore: schema.TypedTable[schema.Habit] = schema.__HabitsStore(_DB.table("habits"))
TodosStore: schema.TypedTable[schema.Todo] = schema.__TodosStore(_DB.table("todos"))
RelationshipStore: schema.TypedTable[schema.Relationship] = schema.__RelationshipStore(
    _DB.table("relationships")
)


def reset_testuser():
    fake_habits = [
        schema.Habit(
            taskID="00000000-0000-0000-0000-000000000001",
            name="Chống đẩy nghiêng 10 lần",
            icon="dumbbell",
            description=None,
            congratsMessage="Gooned. Changed. Ripped.",
            rewards=schema.TaskReward(health=20, cash=10, xp=5),
        ),
        schema.Habit(
            taskID="00000000-0000-0000-0000-000000000002",
            name="Làm 10 bài toán",
            icon="sigma",
            description=None,
            congratsMessage="Albert Einstein 0% → 0.0001%",
            rewards=schema.TaskReward(health=10, cash=10, xp=10),
        ),
        schema.Habit(
            taskID="00000000-0000-0000-0000-000000000003",
            name="Tài xỉu",
            icon="banknote-x",
            description=None,
            congratsMessage="You miss all chances you don't take.",
            rewards=schema.TaskReward(health=-20, cash=-50, xp=5),
        ),
        schema.Habit(
            taskID="00000000-0000-0000-0000-000000000004",
            name="Chứng khoán (tài xỉu)",
            icon="chart-line",
            description=None,
            congratsMessage="r/WallStreetsBet future member",
            rewards=schema.TaskReward(health=10, cash=1, xp=20),
        ),
    ]

    fake_todos = [
        schema.Todo(
            taskID="00000000-0000-0000-0000-000000000001",
            name="Chống đẩy nghiêng 10 lần",
            icon="dumbbell",
            description=None,
            congratsMessage="Gooned. Changed. Ripped.",
            rewards=schema.TaskReward(health=20, cash=10, xp=5),
            deadline=1789103640,
            completed=False,
        ),
        schema.Todo(
            taskID="00000000-0000-0000-0000-000000000002",
            name="Làm 10 bài toán",
            icon="sigma",
            description=None,
            congratsMessage="Albert Einstein 0% → 0.0001%",
            rewards=schema.TaskReward(health=10, cash=10, xp=10),
            deadline=1789103640,
            completed=False,
        ),
        schema.Todo(
            taskID="00000000-0000-0000-0000-000000000003",
            name="Tài xỉu",
            icon="banknote-x",
            description=None,
            congratsMessage="You miss all chances you don't take.",
            rewards=schema.TaskReward(health=-20, cash=-50, xp=5),
            deadline=1789103640,
            completed=False,
        ),
        schema.Todo(
            taskID="00000000-0000-0000-0000-000000000004",
            name="Chứng khoán (tài xỉu)",
            icon="chart-line",
            description=None,
            congratsMessage="r/WallStreetsBet future member",
            rewards=schema.TaskReward(health=10, cash=1, xp=20),
            deadline=1789103640,
            completed=False,
        ),
    ]

    resetted_data = schema.User(
        userID="00000000-0000-0000-0000-000000000000",
        username="test",
        displayname="Kirigaya Kazuto",
        avatarURL="/static/avatars/default.png",
        public=True,
        disabled=False,
        achievements=schema.UserAchievements(
            badges=["cancu"],
            leveling=[schema.LevelingStatus(category="benbi", progress=0.99)],
        ),
        metrics=schema.UserMetrics(health=100, cash=100, xp=49, allTimeXP=49),
        social=schema.UserSocialLink(
            facebook="https://www.facebook.com/doraemon.ch", threads="", tiktok=""
        ),
        relationships=[],
        habits=[i.taskID for i in fake_habits],
        todos=[i.taskID for i in fake_todos],
        creationTimestamp=round(time.time()),
    )

    if (
        len(
            UserStore.update(
                resetted_data.model_dump(),
                Query().userID == "00000000-0000-0000-0000-000000000000",
            )
        )
        == 0
    ):
        UserStore.insert(resetted_data)

    a = schema.AuthenticationEntry(
        userID="00000000-0000-0000-0000-000000000000",
        hashedPassword="JDJiJDEyJHNUL1IxaS9zeTNBcW93eGR2SzNqeHVzZjRLcVZhQ25XNWgxcXdkVXk3aS5yV2R4Y1MyQU5x",
    )

    if (
        len(
            AuthStore.update(
                a.model_dump(),
                Query().userID == "00000000-0000-0000-0000-000000000000",
            )
        )
        == 0
    ):
        AuthStore.insert(a)

    for i in fake_todos:
        TodosStore.table.remove(Query().taskID == i.taskID)
        TodosStore.insert(i)

    for i in fake_habits:
        HabitsStore.table.remove(Query().taskID == i.taskID)
        HabitsStore.insert(i)
