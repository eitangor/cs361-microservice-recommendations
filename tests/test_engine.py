from recommendation_engine import rank_items


def test_rank_items_orders_by_score():
    items = [
        {
            "item_id": "activity-1",
            "attributes": {
                "setting": "outdoor",
                "cost": "free",
            },
        },
        {
            "item_id": "activity-2",
            "attributes": {
                "setting": "outdoor",
                "cost": "paid",
            },
        },
    ]

    preferences = {
        "setting": "outdoor",
        "cost": "free",
    }

    result = rank_items(items, preferences)

    assert result == [
        {"item_id": "activity-1", "score": 1.0},
        {"item_id": "activity-2", "score": 0.5},
    ]


def test_rank_items_excludes_zero_match_items():
    items = [
        {
            "item_id": "activity-1",
            "attributes": {
                "setting": "indoor",
                "cost": "paid",
            },
        }
    ]

    preferences = {
        "setting": "outdoor",
        "cost": "free",
    }

    assert rank_items(items, preferences) == []


def test_rank_items_handles_single_preference():
    items = [
        {
            "item_id": "activity-1",
            "attributes": {
                "setting": "outdoor",
            },
        }
    ]

    assert rank_items(
        items,
        {"setting": "outdoor"},
    ) == [{"item_id": "activity-1", "score": 1.0}]

