from app import app


def get_client():
    app.config["TESTING"] = True
    return app.test_client()


def test_missing_json_body():
    client = get_client()

    response = client.post("/recommendations")

    assert response.status_code == 400
    assert response.get_json()["error"] == "validation_error"


def test_missing_items():
    client = get_client()

    response = client.post(
        "/recommendations",
        json={
            "preferences": {
                "setting": "outdoor"
            }
        },
    )

    assert response.status_code == 400
    assert response.get_json()["field"] == "items"


def test_items_must_be_list():
    client = get_client()

    response = client.post(
        "/recommendations",
        json={
            "items": "activity-1",
            "preferences": {
                "setting": "outdoor"
            },
        },
    )

    assert response.status_code == 400


def test_empty_items_rejected():
    client = get_client()

    response = client.post(
        "/recommendations",
        json={
            "items": [],
            "preferences": {
                "setting": "outdoor"
            },
        },
    )

    assert response.status_code == 400


def test_missing_item_id():
    client = get_client()

    response = client.post(
        "/recommendations",
        json={
            "items": [
                {
                    "attributes": {
                        "setting": "outdoor"
                    }
                }
            ],
            "preferences": {
                "setting": "outdoor"
            },
        },
    )

    assert response.status_code == 400


def test_missing_attributes():
    client = get_client()

    response = client.post(
        "/recommendations",
        json={
            "items": [
                {
                    "item_id": "activity-1"
                }
            ],
            "preferences": {
                "setting": "outdoor"
            },
        },
    )

    assert response.status_code == 400


def test_empty_preferences_rejected():
    client = get_client()

    response = client.post(
        "/recommendations",
        json={
            "items": [
                {
                    "item_id": "activity-1",
                    "attributes": {
                        "setting": "outdoor"
                    }
                }
            ],
            "preferences": {},
        },
    )

    assert response.status_code == 400


def test_no_match_returns_empty_result():
    client = get_client()

    response = client.post(
        "/recommendations",
        json={
            "items": [
                {
                    "item_id": "activity-1",
                    "attributes": {
                        "setting": "indoor",
                        "cost": "paid"
                    }
                }
            ],
            "preferences": {
                "setting": "outdoor",
                "cost": "free"
            },
        },
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["recommendations"] == []
    assert data["count"] == 0
