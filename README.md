# 💳 UPI SMS Parser & Categorizer

An interactive Streamlit-based web application that extracts structured financial transactional data from UPI SMS alerts using regular expression-based pattern matching and automatically categorizes them by merchant.

---

## 🚀 Features

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
- **Parsing Engine:** Python Standard Library Regular Expressions (`re`)
- **Language:** Python 3.8+

---

## 📁 Project Structure

```text
upi_sms_parser_project/
├── app.py                  # Core application file containing parser logic and Streamlit UI
├── requirements.txt        # Project dependencies (Streamlit, Pandas)
├── README.md               # Markdown documentation (this file)
├── README.txt              # Plain-text version of startup commands
├── transactions.csv        # Local CSV storage for parsed transaction logs
└── parser_results.csv      # Archive of parsed transaction outputs
```

---

## 📦 Installation & Setup

1. **Clone or navigate to the project directory:**
   ```bash
   cd c:/Users/vaishnavi/Downloads/upi_sms_parser_project
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
   pip install -r requirements.txt
   ```

4. **Run the Streamlit Application:**
   ```bash
   streamlit run app.py
   ```

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

### Merchant Categories
- **Food Delivery:** Zomato, Swiggy, EatSure, Faasos, Dominos, Pizza Hut, McDonalds, Burger King
- **Travel:** Uber, Ola, Rapido, RedBus, IRCTC, MakeMyTrip, Goibibo, Yatra
- **Shopping:** Amazon, Flipkart, Myntra, Ajio, Meesho, Nykaa, Snapdeal
- **Groceries:** BigBasket, DMart, Blinkit, Zepto, Instamart, Reliance Fresh
- **Utilities & Recharge:** Airtel, Jio, Vi, BSNL, UPPCL, Torrent Power, BSES, Adani Electricity, Jal Board
- **Entertainment & Subscriptions:** Netflix, Amazon Prime, Disney Hotstar, Sony LIV, Spotify, YouTube Premium, ChatGPT, Canva, GitHub, Notion
- **Healthcare:** Apollo Pharmacy, 1mg, NetMeds, Practo, Apollo Hospital
- **Education:** Udemy, Coursera, Unacademy, Physics Wallah, Byjus, Scaler
- **Finance & Insurance:** Groww, Zerodha, Upstox, Angel One, Paytm Money, LIC, PolicyBazaar, HDFC Life, ICICI Lombard
- **Fuel:** Indian Oil, BPCL, HP Petrol Pump, Shell
- **Other:** Rent, Donations (PM CARES, ISKCON, Akshaya Patra), Personal Transfers, Fitness, Beauty, Electronics, Government Services, and Miscellaneous.
