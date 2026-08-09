# Recommendation Microservice

A REST microservice that ranks a collection of items according to supplied user preferences.

The microservice is intentionally domain-independent. A client provides a list of items and their attributes along with a set of preferences. The service compares those preferences against the item attributes and returns matching items ordered by relevance.

## Communication

The microservice communicates through an HTTP REST API using JSON.

**Base URL**

```text
http://127.0.0.1:8004
```

**Endpoint**

```text
POST /recommendations
```

The client application and Recommendation Microservice run as separate processes. Clients communicate with the microservice by sending HTTP requests and receiving JSON responses. No direct function calls between programs are required.

---

## Requirements

- Python 3
- Flask
- pytest for running the automated tests

Install the dependencies with:

```bash
pip install -r requirements.txt
```

---

## Running the Microservice

From the repository directory, run:

```bash
python app.py
```

The Recommendation Microservice will then listen for requests at:

```text
http://127.0.0.1:8004
```

Keep this process running while a client application is using the service.

---

# Requesting Recommendations

Send an HTTP `POST` request to:

```text
/recommendations
```

The request body must be JSON containing:

| Field | Type | Required | Description |
|---|---|---:|---|
| `items` | array | Yes | Candidate items that may be recommended |
| `preferences` | object | Yes | Attributes the client wants to match |

Each item must contain:

| Field | Type | Required | Description |
|---|---|---:|---|
| `item_id` | string | Yes | Unique identifier supplied by the client |
| `attributes` | object | Yes | Attributes used to compare the item with the preferences |

Additional item fields may be included by the client, but ranking is based on the contents of `attributes`.

## Example Request

```json
{
  "items": [
    {
      "item_id": "activity-1",
      "attributes": {
        "category": "outdoor",
        "cost": "free"
      }
    },
    {
      "item_id": "activity-2",
      "attributes": {
        "category": "indoor",
        "cost": "paid"
      }
    },
    {
      "item_id": "activity-3",
      "attributes": {
        "category": "outdoor",
        "cost": "paid"
      }
    }
  ],
  "preferences": {
    "category": "outdoor",
    "cost": "free"
  }
}
```

## Python Example

```python
import requests

payload = {
    "items": [
        {
            "item_id": "activity-1",
            "attributes": {
                "category": "outdoor",
                "cost": "free"
            }
        },
        {
            "item_id": "activity-2",
            "attributes": {
                "category": "indoor",
                "cost": "paid"
            }
        }
    ],
    "preferences": {
        "category": "outdoor",
        "cost": "free"
    }
}

response = requests.post(
    "http://127.0.0.1:8004/recommendations",
    json=payload,
    timeout=5
)

data = response.json()

print(data)
```

---

# Receiving Recommendations

A successful request returns HTTP `200 OK` and a JSON response containing the recommendations ordered by relevance.

Each recommendation includes the item's identifier and its recommendation score.

Example:

```json
{
  "recommendations": [
    {
      "item_id": "activity-1",
      "score": 2
    },
    {
      "item_id": "activity-3",
      "score": 1
    }
  ],
  "count": 2
}
```

A higher score indicates that more of the item's attributes matched the supplied preferences.

For example, if the preferences are:

```json
{
  "category": "outdoor",
  "cost": "free"
}
```

an item matching both preferences receives a higher score than an item matching only one.

Items that do not match any supplied preference are not returned as recommendations.

---

# No Recommendations Available

A request can be valid even when none of the candidate items match the supplied preferences.

In this situation, the microservice returns HTTP `200 OK` with an empty recommendation array:

```json
{
  "recommendations": [],
  "count": 0
}
```

This allows the client application to distinguish between:

- a valid request that produced no recommendations, and
- an invalid request.

---

# Request Validation

Invalid requests return HTTP `400 Bad Request` with a structured JSON error response.

Example:

```json
{
  "error": "validation_error",
  "message": "The 'items' field is required.",
  "field": "items"
}
```

The microservice validates the following cases:

- request body is missing or is not valid JSON;
- request body is not a JSON object;
- `items` is missing;
- `items` is not an array;
- `items` is empty;
- an item is not a JSON object;
- an item has a missing or empty `item_id`;
- an item has a missing or invalid `attributes` object;
- `preferences` is missing;
- `preferences` is not a JSON object;
- `preferences` is empty.

Invalid requests do not cause the service to crash.

---

# Error Response Format

Validation errors use the following structure:

```json
{
  "error": "validation_error",
  "message": "Description of the validation problem.",
  "field": "field_name"
}
```

The `field` value identifies the part of the request that caused the validation failure.

For malformed individual items, the field may identify the item's position, for example:

```text
items[0].item_id
```

---

# Ranking Behavior

The Recommendation Microservice compares each item's `attributes` object against the supplied `preferences`.

For every matching preference, the item's score increases.

For example:

```json
"attributes": {
  "category": "outdoor",
  "cost": "free"
}
```

compared with:

```json
"preferences": {
  "category": "outdoor",
  "cost": "free"
}
```

produces a higher score than:

```json
"attributes": {
  "category": "outdoor",
  "cost": "paid"
}
```

because the first item matches both preferences while the second matches only the category.

Only items with at least one matching preference are returned. Recommendations are ordered from highest score to lowest score.

---

# Running the Tests

Run all automated tests from the repository directory:

```bash
python -m pytest -v
```

The test suite covers both normal recommendation behavior and request validation, including:

- ranking multiple matching items;
- ordering recommendations by relevance;
- returning an empty array when nothing matches;
- missing request data;
- malformed items;
- missing item identifiers;
- invalid attributes;
- empty items;
- missing or empty preferences.

---

# Example Client Integration

The microservice can be used with any application capable of sending HTTP requests.

For example, a family activity application could send candidate activities:

```json
{
  "items": [
    {
      "item_id": "bike-ride",
      "attributes": {
        "category": "outdoor",
        "cost": "free"
      }
    },
    {
      "item_id": "museum",
      "attributes": {
        "category": "indoor",
        "cost": "paid"
      }
    }
  ],
  "preferences": {
    "category": "outdoor"
  }
}
```

The client can then use the returned `item_id` values to identify and display the recommended activities.

The Recommendation Microservice does not need to know how the client stores or displays those items. It only receives candidate items and preferences and returns ranked recommendations.

---

# API Summary

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/recommendations` | Rank supplied items according to supplied preferences |

### Successful recommendation

```text
POST /recommendations
→ 200 OK
```

### Valid request with no matches

```text
POST /recommendations
→ 200 OK
→ {"recommendations": [], "count": 0}
```

### Invalid request

```text
POST /recommendations
→ 400 Bad Request
→ structured JSON validation error
```
