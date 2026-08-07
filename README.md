# Eitan implementation notes

This branch contains Eitan's portion of the Recommendation Microservice:

- Flask application and `POST /recommendations`
- Recommendation ranking engine
- Successful-path endpoint test
- Recommendation-engine tests

Derin owns validation and edge-case handling. 

Expected validation interface:

```python
def validate_recommendation_request(payload):
    # Return [] when valid.
    # Return a list of {"field": ..., "message": ...} dictionaries when invalid.
    ...
```

Run:

```bash
pip install -r requirements.txt
python app.py
```

Tests:

```bash
pytest
```

Example request:

```json
{
  "items": [
    {
      "item_id": "activity-1",
      "attributes": {
        "setting": "outdoor",
        "cost": "free"
      }
    },
    {
      "item_id": "activity-2",
      "attributes": {
        "setting": "outdoor",
        "cost": "paid"
      }
    }
  ],
  "preferences": {
    "setting": "outdoor",
    "cost": "free"
  }
}
```

Example response:

```json
{
  "recommendations": [
    {
      "item_id": "activity-1",
      "score": 1.0
    },
    {
      "item_id": "activity-2",
      "score": 0.5
    }
  ],
  "count": 2
}
```
