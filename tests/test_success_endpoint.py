from app import app


def test_successful_recommendation_request():
    app.config["TESTING"] = True
    client = app.test_client()

    response = client.post(
        "/recommendations",
        json={
            "items": [
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
            ],
            "preferences": {
                "setting": "outdoor",
                "cost": "free",
            },
        },
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["count"] == 2
    assert data["recommendations"][0] == {
        "item_id": "activity-1",
        "score": 1.0,
    }

