import schema

ALL_BADGES = {
    "cancu": schema.BadgeInfo(
        badgeID="cancu",
        name="Cần Cù Bù Siêng Năng",
        maxLevel=99,
        coverArtURL=["/static/badges/cancubusiengnang1.svg"]
    )
}

ALL_LEVELING_CATEGORIES = {
    "benbi": schema.LevelingCategoryInfo(
        catID="benbi",
        name="Bền bỉ",
        allTimeXPRequired=[10, 50, 100],
        maxLevel=3
    )
}