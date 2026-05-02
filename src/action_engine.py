def recommend_action(row):
    risk = row["risk"]

    if risk == "High":
        return "Schedule an urgent call with the customer and address their concerns immediately."

    elif risk == "Medium":
        return "Monitor the account closely and engage with the customer to improve satisfaction."

    else:
        return "Maintain regular engagement and ensure continued satisfaction."