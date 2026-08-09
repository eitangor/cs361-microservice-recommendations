def validate_recommendation_request(payload):
    errors = []

    if payload is None:
        return [
            {
                "field": "request",
                "message": "Request body must contain valid JSON."
            }
        ]

    if not isinstance(payload, dict):
        return [
            {
                "field": "request",
                "message": "Request body must be a JSON object."
            }
        ]

    items = payload.get("items")
    preferences = payload.get("preferences")

    if "items" not in payload:
        errors.append({
            "field": "items",
            "message": "The 'items' field is required."
        })
    elif not isinstance(items, list):
        errors.append({
            "field": "items",
            "message": "The 'items' field must be a list."
        })
    elif len(items) == 0:
        errors.append({
            "field": "items",
            "message": "The 'items' field must contain at least one item."
        })
    else:
        for index, item in enumerate(items):
            if not isinstance(item, dict):
                errors.append({
                    "field": f"items[{index}]",
                    "message": "Each item must be a JSON object."
                })
                continue

            item_id = item.get("item_id")
            attributes = item.get("attributes")

            if not isinstance(item_id, str) or not item_id.strip():
                errors.append({
                    "field": f"items[{index}].item_id",
                    "message": "Each item must contain a non-empty string 'item_id'."
                })

            if not isinstance(attributes, dict):
                errors.append({
                    "field": f"items[{index}].attributes",
                    "message": "Each item must contain an 'attributes' object."
                })

    if "preferences" not in payload:
        errors.append({
            "field": "preferences",
            "message": "The 'preferences' field is required."
        })
    elif not isinstance(preferences, dict):
        errors.append({
            "field": "preferences",
            "message": "The 'preferences' field must be a JSON object."
        })
    elif len(preferences) == 0:
        errors.append({
            "field": "preferences",
            "message": "The 'preferences' field must contain at least one preference."
        })

    return errors
