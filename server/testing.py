from db import *


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
            name="Hoàn thành chức năng ứng dụng",
            icon="pi",
            description=None,
            congratsMessage="Gooned. Changed. Ripped.",
            rewards=schema.TaskReward(health=20, cash=10, xp=5),
            deadline=1789103640,
            completed=False,
        ),
        schema.Todo(
            taskID="00000000-0000-0000-0000-000000000002",
            name="Rửa bát",
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
            name="Thiền",
            icon="accessibility",
            description=None,
            congratsMessage="r/WallStreetsBet future member",
            rewards=schema.TaskReward(health=10, cash=1, xp=20),
            deadline=1789103640,
            completed=False,
        ),
    ]

    fake_rewards_user = [
        schema.Reward(
            rewardID="00000000-0000-0000-0000-000000000000",
            name="Matcha Latte",
            icon="cup-soda",
            description=None,
            congratsMessage=None,
            cost=schema.TaskReward(health=-99, cash=-99, xp=0),
            maxClaims=-1,
            timesClaimed=0,
        ),
        schema.Reward(
            rewardID="00000000-0000-0000-0000-000000000001",
            name="Matcha Latte",
            icon="soup",
            description=None,
            congratsMessage=None,
            cost=schema.TaskReward(health=0, cash=0, xp=-72),
            maxClaims=-1,
            timesClaimed=0,
        ),
        schema.Reward(
            rewardID="00000000-0000-0000-0000-000000000002",
            name="Matcha Latte",
            icon="banknote-x",
            description=None,
            congratsMessage=None,
            cost=schema.TaskReward(health=0, cash=0, xp=0),
            maxClaims=-1,
            timesClaimed=0,
        ),
        schema.Reward(
            rewardID="00000000-0000-0000-0000-000000000003",
            name="Matcha Latte",
            icon="bed-double",
            description=None,
            congratsMessage=None,
            cost=schema.TaskReward(health=-20, cash=-1, xp=0),
            maxClaims=-1,
            timesClaimed=0,
        ),
    ]

    fake_rewards_system = [
        schema.Reward(
            rewardID="00000000-0000-0000-0000-000000000000",
            name="Voucher Free Fire",
            icon="gamepad-2",
            description=None,
            congratsMessage=None,
            cost=schema.TaskReward(health=-99, cash=-99, xp=0),
            maxClaims=-1,
            timesClaimed=0,
        ),
        schema.Reward(
            rewardID="00000000-0000-0000-0000-000000000001",
            name="Ủng hộ từ thiện 20k",
            icon="gift",
            description=None,
            congratsMessage=None,
            cost=schema.TaskReward(health=0, cash=0, xp=20),
            maxClaims=-1,
            timesClaimed=0,
        ),
        schema.Reward(
            rewardID="00000000-0000-0000-0000-000000000002",
            name="Nạp 200k vào FB88",
            icon="banknote-x",
            description=None,
            congratsMessage=None,
            cost=schema.TaskReward(health=0, cash=0, xp=0),
            maxClaims=-1,
            timesClaimed=0,
        ),
        schema.Reward(
            rewardID="00000000-0000-0000-0000-000000000003",
            name="Người yêu",
            icon="bed-double",
            description=None,
            congratsMessage=None,
            cost=schema.TaskReward(health=999, cash=999, xp=0),
            maxClaims=-1,
            timesClaimed=0,
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
        userRewards=[i.rewardID for i in fake_rewards_user],
        systemRewards=[i.rewardID for i in fake_rewards_system],
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

    for i in fake_rewards_user + fake_rewards_system:
        RewardsStore.table.remove(Query().rewardID == i.rewardID)
        RewardsStore.insert(i)
