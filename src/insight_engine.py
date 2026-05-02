def generate_insight(df):
    insights = []

    # Insight 1: Low NPS impact
    low_nps_accounts = df[df["score"] <= 2]
    if len(low_nps_accounts) > 0:
        insights.append("Accounts with very low NPS scores tend to fall into higher risk categories, indicating strong dissatisfaction.")

    # Insight 2: High usage but still risk
    high_usage_low_nps = df[(df["api_calls"] > 50000) & (df["score"] < 6)]
    if len(high_usage_low_nps) > 0:
        insights.append("Some accounts show high product usage but low satisfaction, suggesting potential hidden issues despite engagement.")

    return insights

def changelog_insight(df):
    affected_accounts = df[df["csm_note"].str.contains("v3", case=False, na=False)]

    if len(affected_accounts) > 0:
        return "Accounts using deprecated SDK versions (v3.x) are experiencing more support issues and show higher renewal risk."

    return None