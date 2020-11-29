# Import data analysis dependencies
import pandas as pd

# Fetch data and fromat date
#df = pd.read_csv("https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/OxCGRT_latest.csv")
df = pd.read_csv("data/OxCGRT_latest.csv")
df["Date"] = df["Date"].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))

# List of used variables
restrictions = ["None", "School closing", "Workplace closing", "Cancel public events", "Restrictions on gatherings", "Close public transport", "Stay at home requirements", "Restrictions on internal movement", "International travel controls", "Public information campaigns", "Testing policy", "Contact tracing", "Facial Coverings", "Income support", "Debt/contract relief"]
restrictions_code = ["None", "C1_School closing", "C2_Workplace closing", "C3_Cancel public events", "C4_Restrictions on gatherings", "C5_Close public transport", "C6_Stay at home requirements", "C7_Restrictions on internal movement", "C8_International travel controls", "H1_Public information campaigns", "H2_Testing policy", "H3_Contact tracing", "H6_Facial Coverings", "E1_Income support", "E2_Debt/contract relief"]

# Read json with descriptions
coding = pd.read_json("data/ox_coding.json").fillna("NaN")

def get_oxcgrt_key(key):
    i = restrictions.index(key)
    return restrictions_code[i]

