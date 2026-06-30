Active link : https://upi-bank-sms-transaction-extractor-1.onrender.com/

# 💳 UPI SMS Parser & Categorizer

An interactive Streamlit-based web application that extracts structured financial transactional data from UPI SMS alerts using a hybrid extraction pipeline and automatically categorizes them by merchant.

---

## 🚀 Features

- **Hybrid Merchant Extraction Engine:** Replaced naive regex matching with a production-grade extraction cascade achieving 100% accuracy on simulated test cases:
  1. **Regex Extraction:** Captures structured text from 16+ common debit and credit message patterns.
  2. **spaCy Named Entity Recognition (NER):** Fallback parser running spaCy's standard NER to detect `ORG` and `PERSON` entity candidates.
  3. **VPA Parsing:** Detects UPI IDs and handles VPA name extractions.
  4. **Cleaning Pipeline:** Strips transaction UTRs, dates, amounts, bank names, filler text, and special characters.
  5. **Merchant Alias Dictionary:** Maps over 1,200 programmatically expanded aliases to 80+ canonical Indian merchants.
  6. **RapidFuzz Fuzzy Matcher:** Resolves spelling variations and sub-brands (e.g., `ZOMATO LTD` -> `Zomato`).
  7. **Confidence Scorer:** Scores extraction candidates based on source and dictionary matching.
- **Regex-based Parsing:** Extracts crucial transaction details:
  - Account Number (e.g., `XX1234`)
  - Reference ID / UTR Number
  - Transaction Amount (INR)
  - Transaction Type (`Debit` / `Credit`)
  - Transaction Date
  - Merchant Name
  - Bank Name (SBI, HDFC, ICICI, etc.)
- **Automatic Categorization:** Uses a comprehensive mapping system to automatically classify merchants into over 20 spending categories (e.g., *Food, Travel, Groceries, Utilities, Entertainment, Healthcare, Finance*).
- **Persistent Local Database:** Appends parsed transactions to a local CSV database (`transactions.csv`) for persistent record-keeping.
- **Modern Web Dashboard:** A clean, intuitive Streamlit user interface to paste SMS text, view extracted JSON payloads, and browse parsed transaction tables.

---

## 🛠️ Technology Stack

- **Frontend & Dashboard:** [Streamlit](https://streamlit.io/)
- **Data Manipulation:** [Pandas](https://pandas.pydata.org/)
- **Fuzzy Matching:** [RapidFuzz](https://github.com/rapidfuzz/RapidFuzz)
- **Natural Language Processing:** [spaCy](https://spacy.io/) (`en_core_web_sm` model)
- **Parsing Engine:** Python Standard Library Regular Expressions (`re`)
- **Language:** Python 3.8+

---

## 📁 Project Structure

```text
UPI-Bank-SMS-Transaction-Extractor/
├── app.py                  # Streamlit application UI and driver logic
├── merchant_pipeline.py    # Redesigned hybrid NLP & fuzzy merchant extraction module
├── test_samples.py         # Test suite generating 200 SMS formats to verify parser accuracy
├── requirements.txt        # Project dependencies (Streamlit, Pandas, spaCy, RapidFuzz)
├── README.md               # Markdown documentation (this file)
├── transactions.csv        # Local CSV storage for parsed transaction logs
└── parser_results.csv      # Archive of parsed transaction outputs
```

---

## 📦 Installation & Setup

1. **Navigate to the project directory:**
   ```bash
   cd c:/Users/vaishnavi/OneDrive/Desktop/coding/UPI-Bank-SMS-Transaction-Extractor
   ```

2. **Set up a Virtual Environment (Optional but recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   python -m pip install -r requirements.txt
   ```

4. **Download the spaCy English NLP model:**
   ```bash
   python -m spacy download en_core_web_sm
   ```

5. **Run the Streamlit Application:**
   ```bash
   streamlit run app.py
   ```

---

## 🧪 Running the Test Suite

Verify the accuracy of the parser by running the test suite of 200 simulated SMS samples across all major Indian banks (SBI, HDFC, ICICI, etc.) and UPI apps (GPay, PhonePe, Paytm, etc.):
```bash
python test_samples.py
```
This prints a structured report showing the original SMS, extracted merchant, normalized merchant, category, confidence score, and accuracy metrics (target: >= 95%, current: **100%**).

---

## 💡 How to Use

1. Launch the Streamlit application using the command above.
2. Open the application in your browser (usually starts at `http://localhost:8501`).
3. Paste a standard UPI SMS alert into the text area.
   - *Example:* `A/c XX1234 debited by Rs. 150 for Zomato on 20-10-23 Ref 123456789012`
4. Click **Extract Information**.
5. View the real-time parsed details in **JSON format** and as a **DataFrame**.
6. The transaction will automatically be saved to `transactions.csv` in the root folder.

---

## 🏦 Supported Banks & Categories

### Supported Banks
- State Bank of India (`SBI`)
- HDFC Bank (`HDFC`)
- ICICI Bank (`ICICI`)
- Axis Bank (`AXIS`)
- Punjab National Bank (`PNB`)
- Kotak Mahindra Bank (`KOTAK`)
- Bank of Baroda (`BOB`)
- Canara Bank (`CANARA`)
- Union Bank of India (`UNION`)
- IDFC First Bank (`IDFC`)
- Yes Bank (`YES BANK`)
- IndusInd Bank (`INDUSIND`)
- Federal Bank (`FEDERAL`)
- RBL Bank (`RBL`)
- UCO Bank (`UCO`)
- Paytm Payments Bank (`Paytm Payments Bank`)
- Airtel Payments Bank (`Airtel Payments Bank`)

### Merchant Categories
- **Food Delivery:** Zomato, Swiggy, EatSure, Faasos, Dominos, Pizza Hut, McDonalds, Burger King, KFC, Subway, Starbucks
- **Travel:** Uber, Ola, Rapido, RedBus, IRCTC, MakeMyTrip, Goibibo, Yatra
- **Shopping:** Amazon, Flipkart, Myntra, Ajio, Meesho, Nykaa, Snapdeal
- **Groceries:** BigBasket, DMart, Blinkit, Zepto, Reliance Fresh, JioMart
- **Utilities & Recharge:** Airtel, Jio, Vi, BSNL, UPPCL, Torrent Power, BSES, Adani Electricity, Jal Board
- **Entertainment & Subscriptions:** Netflix, Amazon Prime, Disney Hotstar, Sony LIV, Spotify, YouTube Premium, ChatGPT, Canva, GitHub, Notion
- **Healthcare:** Apollo Pharmacy, 1mg, NetMeds, Practo, Apollo Hospital
- **Education:** Udemy, Coursera, Unacademy, Physics Wallah, Byjus, Scaler
- **Finance & Insurance:** Groww, Zerodha, Upstox, Angel One, Paytm Money, LIC, PolicyBazaar, HDFC Life, ICICI Lombard
- **Fuel:** Indian Oil, BPCL, HP Petrol Pump, Shell
- **Other:** Rent, Donations (PM CARES, ISKCON, Akshaya Patra), Personal Transfers, Fitness, Beauty, Electronics, Government Services, and Miscellaneous.
