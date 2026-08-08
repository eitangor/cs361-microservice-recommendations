def rank_items(items, preferences):
    """Rank candidate items by the percentage of supplied preferences they match.

    Each item must contain:
        {
            "item_id": "...",
            "attributes": {...}
        }

    Returns only items with at least one matching preference, sorted from
    highest to lowest score.
    """
    recommendations = []

    for item in items:
        attributes = item.get("attributes", {})

        if not preferences:
            score = 0.0
        else:
            matches = sum(
                1
                for key, value in preferences.items()
                if attributes.get(key) == value
            )
            score = matches / len(preferences)

        if score > 0:
            recommendations.append({
                "item_id": item["item_id"],
                "score": round(score, 2),
            })

    recommendations.sort(
        key=lambda recommendation: recommendation["score"],
        reverse=True,
    )

    return recommendations
