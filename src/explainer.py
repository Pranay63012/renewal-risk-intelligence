def generate_explanation(row):
    usage = row.get("api_calls", 0)
    tickets = row.get("ticket_count", 0)
    nps = row.get("score", 0)

    signals = []

    # Usage signal
    if usage < 5000:
        signals.append("low engagement")
    else:
        signals.append("good engagement")

    # Support signal
    if tickets > 10:
        signals.append("high support issues")
    elif tickets > 5:
        signals.append("moderate support issues")

    # Satisfaction signal
    if nps < 5:
        signals.append("low satisfaction")
    elif nps < 7:
        signals.append("moderate satisfaction")

    # Combine into one clean sentence
    return ", ".join(signals).capitalize() + "."


def combine_explanation(row):
    base = row["reason"]
    ai_text = row.get("ai_summary", "")

    # If no AI output
    if not ai_text or "No notes" in ai_text:
        return base

    # Extract sentiment
    sentiment = "neutral"
    if "Negative" in ai_text:
        sentiment = "negative"
    elif "Positive" in ai_text:
        sentiment = "positive"

    # Clean final sentence
    return f"{base} {sentiment.capitalize()} customer sentiment detected."