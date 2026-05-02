def calculate_risk(row):
    score = 0

    # usage check
    if row["api_calls"] < 5000:
        score += 2

    # ticket check
    if row["ticket_count"] > 10:
        score += 2

    # nps check
    if row["score"] < 6:
        score += 3

    if score >= 5:
        return "High"
    elif score >= 3:
        return "Medium"
    else:
        return "Low"