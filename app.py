
import streamlit as st
import pandas as pd
import re
from pathlib import Path

# =====================================================
# MERCHANT CATEGORIES
# =====================================================

merchant_categories = {

    # Food Delivery
    "Zomato": "Food",
    "Swiggy": "Food",
    "EatSure": "Food",
    "Faasos": "Food",
    "Dominos": "Food",
    "Pizza Hut": "Food",
    "McDonalds": "Food",
    "Burger King": "Food",

    # Travel
    "Uber": "Travel",
    "Ola": "Travel",
    "Rapido": "Travel",
    "RedBus": "Travel",
    "IRCTC": "Travel",
    "MakeMyTrip": "Travel",
    "Goibibo": "Travel",
    "Yatra": "Travel",

    # Shopping
    "Amazon": "Shopping",
    "Flipkart": "Shopping",
    "Myntra": "Shopping",
    "Ajio": "Shopping",
    "Meesho": "Shopping",
    "Nykaa": "Shopping",
    "Snapdeal": "Shopping",

    # Groceries
    "BigBasket": "Groceries",
    "DMart": "Groceries",
    "Blinkit": "Groceries",
    "Zepto": "Groceries",
    "Instamart": "Groceries",
    "Reliance Fresh": "Groceries",

    # Recharge
    "Airtel": "Recharge",
    "Jio": "Recharge",
    "Vi": "Recharge",
    "BSNL": "Recharge",

    # Utilities
    "UPPCL": "Utilities",
    "Torrent Power": "Utilities",
    "BSES": "Utilities",
    "Adani Electricity": "Utilities",
    "Jal Board": "Utilities",

    # Entertainment
    "Netflix": "Entertainment",
    "Amazon Prime": "Entertainment",
    "Disney Hotstar": "Entertainment",
    "Sony LIV": "Entertainment",
    "Spotify": "Entertainment",
    "YouTube Premium": "Entertainment",

    # Healthcare
    "Apollo Pharmacy": "Healthcare",
    "1mg": "Healthcare",
    "NetMeds": "Healthcare",
    "Practo": "Healthcare",
    "Apollo Hospital": "Healthcare",

    # Education
    "Udemy": "Education",
    "Coursera": "Education",
    "Unacademy": "Education",
    "Physics Wallah": "Education",
    "Byjus": "Education",
    "Scaler": "Education",

    # Finance
    "Groww": "Finance",
    "Zerodha": "Finance",
    "Upstox": "Finance",
    "Angel One": "Finance",
    "Paytm Money": "Finance",

    # Insurance
    "LIC": "Insurance",
    "PolicyBazaar": "Insurance",
    "HDFC Life": "Insurance",
    "ICICI Lombard": "Insurance",

    # Fuel
    "Indian Oil": "Fuel",
    "BPCL": "Fuel",
    "HP Petrol Pump": "Fuel",
    "Shell": "Fuel",

    # Rent
    "Landlord": "Rent",
    "House Owner": "Rent",

    # Donations
    "PM CARES": "Donation",
    "ISKCON": "Donation",
    "Akshaya Patra": "Donation",

    # Personal Transfer
    "Rahul": "Personal Transfer",
    "Amit": "Personal Transfer",
    "Priya": "Personal Transfer",
    "Neha": "Personal Transfer",

    # Fitness
    "Cult Fit": "Fitness",
    "Gold Gym": "Fitness",
    "Anytime Fitness": "Fitness",

    # Beauty
    "Lakme": "Beauty",
    "Purplle": "Beauty",
    "Mamaearth": "Beauty",

    # Electronics
    "Croma": "Electronics",
    "Reliance Digital": "Electronics",
    "Vijay Sales": "Electronics",

    # Subscription
    "ChatGPT": "Subscription",
    "Canva": "Subscription",
    "GitHub": "Subscription",
    "Notion": "Subscription",

    # Government
    "Passport Seva": "Government",
    "Income Tax": "Government",
    "GST Portal": "Government",

    # Miscellaneous
    "Local Store": "Miscellaneous",
    "Unknown Merchant": "Miscellaneous"
}


# =====================================================
# CATEGORY DETECTION
# =====================================================

def get_category(merchant):
    from merchant_pipeline import categorize_merchant
    return categorize_merchant(merchant)

# =====================================================
# SMS PARSER
# =====================================================

def extract_info(sms):

    result = {

        "account_no": "NaN",
        "reference_id": "NaN",
        "amount": "NaN",
        "txn_type": "NaN",
        "date": "NaN",
        "merchant": "NaN",
        "category": "NaN",
        "bank": "NaN"

    }


    # --------------------
    # ACCOUNT NUMBER
    # --------------------

    account_patterns = [

        r'A/C\s*([A-Z0-9]+)',
        r'A/c\s*([A-Z0-9]+)',
        r'A/c\s*XX(\d+)',
        r'account\s*XX(\d+)'

    ]


    for pattern in account_patterns:

        match = re.search(
            pattern,
            sms,
            re.IGNORECASE
        )

        if match:

            result["account_no"] = match.group(1)
            break

    # --------------------
    # AMOUNT
    # --------------------

    amount_patterns = [

        r'debited by\s*(\d+(?:\.\d+)?)',
        r'credited by\s*(\d+(?:\.\d+)?)',
        r'Rs\.?\s*(\d+(?:\.\d+)?)',
        r'INR\s*(\d+(?:\.\d+)?)'

    ]


    for pattern in amount_patterns:

        match = re.search(
            pattern,
            sms,
            re.IGNORECASE
        )

        if match:

            result["amount"] = match.group(1)
            break

    # --------------------
    # REFERENCE ID
    # --------------------

    ref_patterns = [

        r'Refno[: ]*(\d+)',
        r'Ref No[: ]*(\d+)',
        r'Reference[: ]*(\d+)',
        r'Ref[: ]*(\d+)',
        r'UTR[: ]*(\d+)'

    ]



    for pattern in ref_patterns:

        match = re.search(
            pattern,
            sms,
            re.IGNORECASE
        )

        if match:

            result["reference_id"] = match.group(1)
            break

    # --------------------
    # DATE
    # --------------------

    date_patterns = [

        r'(\d{2}[A-Za-z]{3}\d{2})',
        r'(\d{2}-\d{2}-\d{2})',
        r'(\d{2}/\d{2}/\d{4})',
        r'(\d{4}-\d{2}-\d{2})'

    ]


    for pattern in date_patterns:

        match = re.search(
            pattern,
            sms
        )

        if match:

            result["date"] = match.group(1)
            break

    # --------------------
    # TXN TYPE
    # --------------------

    sms_lower = sms.lower()

    debit_keywords = [
        "debited",
        "spent",
        "paid",
        "purchase",
        "withdrawn",
        "sent",
        "trf to",
        "transferred to",
        "successful to"
    ]

    credit_keywords = [
        "credited",
        "received",
        "payment received",
        "money received",
        "deposit",
        "received from",
        "upi cr",
        "credit",
        "refund",
        "refunded",
        "added"
    ]

    result["txn_type"] = "Unknown"

    for word in debit_keywords:

        if word in sms_lower:

            result["txn_type"] = "Debit"
            break

    if result["txn_type"] == "Unknown":

        for word in credit_keywords:

            if word in sms_lower:

                result["txn_type"] = "Credit"
                break
        else:
            if re.search(r'\bcr\b', sms_lower):
                result["txn_type"] = "Credit"

    # --------------------
    # --------------------
    # MERCHANT
    # --------------------

    from merchant_pipeline import extract_merchant, categorize_merchant
    merchant, confidence = extract_merchant(sms)
    result["merchant"] = merchant

    # --------------------
    # CATEGORY
    # --------------------

    if merchant != "NaN":
        result["category"] = categorize_merchant(merchant)
    else:
        result["category"] = "NaN"

    # --------------------
    # BANK
    # --------------------

    banks = [

        "SBI",
        "HDFC",
        "ICICI",
        "AXIS",
        "PNB",
        "KOTAK",
        "BOB",
        "CANARA",
        "UNION",
        "IDFC",
        "YES BANK",
        "INDUSIND",
        "FEDERAL",
        "RBL",
        "UCO"

   ]


    for bank in banks:

        if bank in sms.upper():

            result["bank"] = bank
            break

    # Fill missing values with NaN

    for key in result:

        if str(result[key]).strip() == "":
            result[key] = "NaN"

    return result


# =====================================================
# STREAMLIT UI
# =====================================================

st.set_page_config(
    page_title="UPI SMS Parser",
    layout="wide"
)

st.title("💳 UPI SMS Parser & Categorizer")

sms = st.text_area(
    "Paste UPI SMS Here",
    height=200
)

if st.button("Extract Information"):

    if sms.strip() == "":

        st.warning(
            "Please enter a UPI SMS."
        )

    else:

        data = extract_info(sms)

        st.subheader(
            "Extracted Information"
        )

        st.json(data)

        columns = [

            "account_no",
            "reference_id",
            "amount",
            "txn_type",
            "date",
            "merchant",
            "category",
            "bank"

        ]

        df = pd.DataFrame(
            [data],
            columns=[
                "account_no",
                "reference_id",
                "amount",
                "txn_type",
                "date",
                "merchant",
                "category",
                "bank"
            ]
        )

        file_name = "transactions.csv"

        if Path(file_name).exists():

            df.to_csv(
                file_name,
                mode="a",
                header=False,
                index=False
            )

        else:

            df.to_csv(
                file_name,
                index=False
            )

        st.success(
            "Transaction saved to transactions.csv"
        )

        st.dataframe(df)
