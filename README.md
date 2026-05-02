# Renewal Risk Intelligence Engine

## Overview

This project is a prototype Renewal Risk Intelligence system designed to help BizOps teams identify accounts at risk of churn or downgrade before renewal.

It consolidates multiple data sources such as product usage, support tickets, NPS feedback, and unstructured CSM notes, and generates:

- Risk classification (High / Medium / Low)
- Concise explanation of risk
- Recommended actions for account teams
- AI-powered insights from customer notes

---

## Problem Statement

BizOps teams often rely on scattered data and intuition to assess renewal risk. This system provides a structured, data-driven approach to:

- Detect early warning signals  
- Explain why an account is at risk  
- Suggest next actions proactively  

---

## Features

- Multi-source data integration (accounts, usage, tickets, NPS, notes)  
- Risk scoring based on behavioral signals  
- AI-powered analysis of messy CSM notes  
- Concise, business-friendly explanations  
- Action recommendations for account managers  
- Configurable renewal window (30 / 60 / 90 days or all accounts)  
- Insight generation including non-obvious patterns  

---

## Tech Stack

- Python  
- Pandas  
- Groq API (LLM for text analysis)  

---


---

## How to Run

### 1. Install dependencies
pip install -r requirements.txt

---

### 2. Set API Key (Groq)

Windows (PowerShell):
setx GROQ_API_KEY "your_api_key_here"

Restart terminal after setting the key.

---

### 3. Run the project

Default (90 days):
python main.py

python main.py 60  > for 60 days
 
python main.py 30  >  for 30 days 

python main.py all  > for all days


---

## Output

The system generates:
output/final_output.csv


Columns:

- account_name  
- risk  
- final_reason  
- action  

---

## Example Output

| Account | Risk | Reason | Action |
|--------|------|--------|--------|
| NovaTech Industries | High | Low engagement, high support issues, low satisfaction. Negative sentiment detected. | Schedule an urgent call |

---

## Key Insights Generated

- Accounts with low NPS scores are strongly correlated with higher renewal risk  
- High usage with low satisfaction indicates hidden friction  
- Deprecated SDK usage correlates with increased support issues  

---

## AI Usage

LLM is used to:

- Analyze unstructured CSM notes  
- Extract sentiment (Positive / Neutral / Negative)  
- Identify churn signals and issues  
- Enhance explanations with qualitative context  

---

## Design Decisions

- Used rule-based scoring for interpretability  
- Combined structured + unstructured data  
- Built concise explanations for business usability  
- Added configurable time window for flexibility  

---

## What I Would Improve

- Replace rule-based scoring with ML model  
- Improve entity resolution for notes mapping  
- Build a Streamlit dashboard for visualization  
- Add real-time data pipeline integration  
- Improve multilingual support for notes  

---

## Demo

(Add your demo video link here)

---

## Author

Pranay Rachakonda