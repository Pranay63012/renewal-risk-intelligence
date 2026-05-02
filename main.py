import sys
import pandas as pd

from src.insight_engine import generate_insight, changelog_insight
from src.action_engine import recommend_action
from src.explainer import generate_explanation, combine_explanation
from src.risk_engine import calculate_risk
from src.ai_engine import analyze_notes, split_notes, extract_account_id


print("STARTING PROGRAM...\n")

# ==============================
# CONFIG (DAYS PARAMETER)
# ==============================

days = 90  # default

if len(sys.argv) > 1:
    arg = sys.argv[1].lower()
    if arg == "all":
        days = "all"
    else:
        try:
            days = int(arg)
        except:
            print("Invalid input. Using default 90 days.")
            days = 90

# ==============================
# LOAD DATA
# ==============================

accounts = pd.read_csv("data/accounts.csv")
usage = pd.read_csv("data/usage_metrics.csv")
tickets = pd.read_csv("data/support_tickets.csv")
nps = pd.read_csv("data/nps_responses.csv")

with open("data/csm_notes.txt", "r", encoding="utf-8") as f:
    notes = f.read()

with open("data/changelog.md", "r", encoding="utf-8") as f:
    changelog = f.read()

# ==============================
# FILTER ACCOUNTS
# ==============================

accounts["contract_end_date"] = pd.to_datetime(accounts["contract_end_date"])
today = pd.Timestamp.today()

if days == "all":
    renewals = accounts.copy()
    print("Processing ALL accounts")
else:
    future_date = today + pd.Timedelta(days=days)
    renewals = accounts[
        (accounts["contract_end_date"] >= today) &
        (accounts["contract_end_date"] <= future_date)
    ]
    print(f"Processing accounts renewing in next {days} days")

print("Total accounts:", renewals.shape[0])

# ==============================
# AGGREGATIONS
# ==============================

usage_agg = usage.groupby("account_id").mean(numeric_only=True).reset_index()
ticket_agg = tickets.groupby("account_id").size().reset_index(name="ticket_count")
nps_agg = nps.groupby("account_id")["score"].mean().reset_index()

# ==============================
# MERGE DATA
# ==============================

final_df = renewals.copy()

final_df = final_df.merge(usage_agg, on="account_id", how="left")
final_df = final_df.merge(ticket_agg, on="account_id", how="left")
final_df = final_df.merge(nps_agg, on="account_id", how="left")

final_df.fillna(0, inplace=True)

# ==============================
# RISK + EXPLANATION + ACTION
# ==============================

final_df["risk"] = final_df.apply(calculate_risk, axis=1)
final_df["reason"] = final_df.apply(generate_explanation, axis=1)
final_df["action"] = final_df.apply(recommend_action, axis=1)

# ==============================
# MAP NOTES TO ACCOUNTS
# ==============================

note_blocks = split_notes(notes)
account_notes = {}

for note in note_blocks:
    acc_id = extract_account_id(note)

    if acc_id:
        account_notes[acc_id] = note
    else:
        for _, row in accounts.iterrows():
            if row["account_name"].lower() in note.lower():
                account_notes[row["account_id"]] = note

final_df["csm_note"] = final_df["account_id"].map(account_notes)

# ==============================
# AI PER ACCOUNT (SAFE)
# ==============================

def safe_ai_call(note):
    if pd.isna(note):
        return "No notes available"
    try:
        return analyze_notes(note[:500])
    except Exception as e:
        return "AI error"

final_df["ai_summary"] = final_df["csm_note"].apply(safe_ai_call)

# ==============================
# FINAL EXPLANATION
# ==============================

final_df["final_reason"] = final_df.apply(combine_explanation, axis=1)

# ==============================
# INSIGHTS
# ==============================

insights = generate_insight(final_df)
extra_insight = changelog_insight(final_df)

print("\nKEY INSIGHTS:")
for i, insight in enumerate(insights, 1):
    print(f"{i}. {insight}")

if extra_insight:
    print(f"{len(insights)+1}. {extra_insight}")

# ==============================
# FINAL OUTPUT
# ==============================

final_output = final_df[[
    "account_name",
    "risk",
    "final_reason",
    "action"
]]

print("\nFINAL OUTPUT:\n")
print(final_output.head(30))

# Save output
final_output.to_csv("output/final_output.csv", index=False)

print("\nProgram completed successfully.")

# ==============================
# HIGH RISK ACCOUNTS
# ==============================

print("\nHIGH RISK ACCOUNTS:\n")

high_risk = final_output[final_output["risk"] == "High"]

if high_risk.empty:
    print("No high-risk accounts found.")
else:
    print(high_risk[["account_name", "final_reason", "action"]])