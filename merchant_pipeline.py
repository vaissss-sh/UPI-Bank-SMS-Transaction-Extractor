import re
import spacy
from typing import Tuple, List, Dict, Optional
from rapidfuzz import fuzz, process

# Load spaCy model for NER
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # Fallback to loading it programmatically if downloaded but not linked yet
    try:
        import en_core_web_sm
        nlp = en_core_web_sm.load()
    except ImportError:
        nlp = None

# =====================================================
# CANONICAL MERCHANTS & BASE ALIASES (80+ Merchants)
# =====================================================

CANONICAL_MERCHANTS: Dict[str, Dict] = {
    "Amazon": {
        "category": "Shopping",
        "aliases": ["AMZN", "Amazon India", "Amazon Pay", "Amazon Seller Services", "AMAZONPAY", "AMZN IN", "AMAZON SELLER", "AMAZON RETAIL", "AMAZON WEB SERVICES"]
    },
    "Flipkart": {
        "category": "Shopping",
        "aliases": ["FLIPKART INTERNET", "FLIPKART PAYMENTS", "FLIPKART GROCERY", "FLIPKART INDIA", "FLIPKART ONLINE", "SHOPSY", "SHOPSY BY FLIPKART"]
    },
    "Myntra": {
        "category": "Shopping",
        "aliases": ["MYNTRA DESIGNS", "MYNTRA FASHION", "MYNTRA LIFESTYLE", "MYNTRA ONLINE"]
    },
    "Ajio": {
        "category": "Shopping",
        "aliases": ["AJIO ONLINE", "AJIO FASHION", "AJIO RELIANCE", "AJIO TRENDS"]
    },
    "Meesho": {
        "category": "Shopping",
        "aliases": ["MEESHO ONLINE", "MEESHO PAYMENTS", "MEESHO FASHION", "FASHNEAR TECHNOLOGIES"]
    },
    "Nykaa": {
        "category": "Shopping",
        "aliases": ["NYKAA E-RETAIL", "FSN E-COMMERCE", "NYKAA FASHION", "NYKAA BEAUTY"]
    },
    "Snapdeal": {
        "category": "Shopping",
        "aliases": ["SNAPDEAL LIMITED", "SNAPDEAL ONLINE", "SNAPDEAL RETAIL"]
    },
    "Tata Cliq": {
        "category": "Shopping",
        "aliases": ["TATA CLIQ ONLINE", "TATA CLIQ FASHION", "TATA DIGITAL"]
    },
    "Swiggy": {
        "category": "Food",
        "aliases": ["SWIGGY LTD", "SWIGGY INSTAMART", "SWIGGY FOOD", "SWIGGY DELIVERY", "SWIGGY BUNDL", "BUNDL TECHNOLOGIES", "SWIGGY DINE OUT"]
    },
    "Zomato": {
        "category": "Food",
        "aliases": ["ZOMATO LIMITED", "ZOMATO ONLINE", "ZOMATO FOOD", "ZOMATO ORDER", "ZOMATO DELIVERY", "ZOMATO HYPERPURE"]
    },
    "EatSure": {
        "category": "Food",
        "aliases": ["EATSURE ONLINE", "REBEL FOODS", "EATSURE DELIVERY"]
    },
    "Faasos": {
        "category": "Food",
        "aliases": ["FAASOS FOODS", "FAASOS DELIVERY", "FAASOS ONLINE"]
    },
    "Dominos": {
        "category": "Food",
        "aliases": ["DOMINOS PIZZA", "JUBILANT FOODWORKS", "DOMINOS DELIVERY"]
    },
    "Pizza Hut": {
        "category": "Food",
        "aliases": ["PIZZA HUT ONLINE", "PIZZA HUT DELIVERY", "DEVYANI INTERNATIONAL"]
    },
    "McDonalds": {
        "category": "Food",
        "aliases": ["MCDONALDS INDIA", "WESTLIFE DEVELOPMENT", "HARDCASTLE RESTAURANTS", "MCDONALDS DELIVERY"]
    },
    "Burger King": {
        "category": "Food",
        "aliases": ["BURGER KING INDIA", "RESTAURANT BRAND ASIA", "BURGER KING ONLINE"]
    },
    "KFC": {
        "category": "Food",
        "aliases": ["KFC INDIA", "KFC ONLINE", "KFC DELIVERY"]
    },
    "Subway": {
        "category": "Food",
        "aliases": ["SUBWAY INDIA", "SUBWAY ONLINE", "SUBWAY SANDWICHES"]
    },
    "Starbucks": {
        "category": "Food",
        "aliases": ["TATA STARBUCKS", "STARBUCKS COFFEE", "STARBUCKS ONLINE"]
    },
    "Uber": {
        "category": "Travel",
        "aliases": ["UBER INDIA", "UBER CABS", "UBER TRIP", "UBER RIDE", "UBER SYSTEMS", "UBER BV"]
    },
    "Ola": {
        "category": "Travel",
        "aliases": ["OLA CABS", "ANI TECHNOLOGIES", "OLA RIDE", "OLA ELECTRIC", "OLA FLEET"]
    },
    "Rapido": {
        "category": "Travel",
        "aliases": ["RAPIDO BIKE", "ROPPEN TRANSPORTATION", "RAPIDO AUTO", "RAPIDO CABS"]
    },
    "RedBus": {
        "category": "Travel",
        "aliases": ["REDBUS INDIA", "IBIBO GROUP", "REDBUS TICKETS"]
    },
    "IRCTC": {
        "category": "Travel",
        "aliases": ["IRCTC LITE", "IRCTC TOURISM", "IRCTC APP", "INDIAN RAILWAYS"]
    },
    "MakeMyTrip": {
        "category": "Travel",
        "aliases": ["MAKEMYTRIP INDIA", "MMT TRAVEL", "MAKEMYTRIP ONLINE"]
    },
    "Goibibo": {
        "category": "Travel",
        "aliases": ["GOIBIBO ONLINE", "IBIBO GROUP PRIVATE"]
    },
    "Yatra": {
        "category": "Travel",
        "aliases": ["YATRA ONLINE", "YATRA TRAVELS"]
    },
    "BigBasket": {
        "category": "Groceries",
        "aliases": ["BIGBASKET ONLINE", "SUPERMARKET GROCERY", "BB INSTANT", "BB DAILY", "INNOVATIVE RETAIL"]
    },
    "DMart": {
        "category": "Groceries",
        "aliases": ["DMART READY", "AVENUE SUPERMARTS", "DMART SUPERMARKET"]
    },
    "Blinkit": {
        "category": "Groceries",
        "aliases": ["BLINKIT GROCERY", "BLINK COMMERCE", "GROFERS INDIA", "BLINKIT DELIVERY"]
    },
    "Zepto": {
        "category": "Groceries",
        "aliases": ["ZEPTO DELIVERY", "KIRANAKART", "ZEPTO GROCERY", "ZEPTO NOW"]
    },
    "Reliance Fresh": {
        "category": "Groceries",
        "aliases": ["RELIANCE FRESH ON", "RELIANCE RETAIL", "RELIANCE SMART", "JIO MART"]
    },
    "Airtel": {
        "category": "Recharge",
        "aliases": ["AIRTEL PREPAID", "AIRTEL POSTPAID", "BHARTI AIRTEL", "AIRTEL BROADBAND", "AIRTEL DIGITAL TV"]
    },
    "Jio": {
        "category": "Recharge",
        "aliases": ["JIO PREPAID", "JIO FIBER", "RELIANCE JIO", "JIO DIGITAL LIFE", "JIO POSTPAID"]
    },
    "Vi": {
        "category": "Recharge",
        "aliases": ["VODAFONE IDEA", "VI PREPAID", "VI POSTPAID", "VI RECHARGE"]
    },
    "BSNL": {
        "category": "Recharge",
        "aliases": ["BSNL RECHARGE", "BSNL MOBILE", "BSNL LANDLINE"]
    },
    "UPPCL": {
        "category": "Utilities",
        "aliases": ["UPPCL ONLINE", "UP POWER CORP", "UPPCL BILL"]
    },
    "Torrent Power": {
        "category": "Utilities",
        "aliases": ["TORRENT POWER BILL", "TORRENT ELECTRICITY"]
    },
    "BSES": {
        "category": "Utilities",
        "aliases": ["BSES RAJDHANI", "BSES YAMUNA", "BSES BILL"]
    },
    "Adani Electricity": {
        "category": "Utilities",
        "aliases": ["ADANI POWER", "ADANI ELECTRICITY BILL"]
    },
    "Jal Board": {
        "category": "Utilities",
        "aliases": ["DELHI JAL BOARD", "JAL BOARD BILL"]
    },
    "Netflix": {
        "category": "Entertainment",
        "aliases": ["NETFLIX INDIA", "NETFLIX ENTERTAINMENT", "NETFLIX STREAMING", "NETFLIX SUBSCRIPTION"]
    },
    "Amazon Prime": {
        "category": "Entertainment",
        "aliases": ["PRIME VIDEO", "AMAZON PRIME VIDEO", "AMAZON PRIME MEMBER"]
    },
    "Disney Hotstar": {
        "category": "Entertainment",
        "aliases": ["NOVI DIGITAL", "HOTSTAR SUBSCRIPTION", "DISNEY HOTSTAR BILL"]
    },
    "Sony LIV": {
        "category": "Entertainment",
        "aliases": ["SONY LIV SUBSCRIPTION", "SPN NETWORKS", "SONY PICTURES"]
    },
    "Spotify": {
        "category": "Entertainment",
        "aliases": ["SPOTIFY INDIA", "SPOTIFY MUSIC", "SPOTIFY PREMIUM"]
    },
    "YouTube Premium": {
        "category": "Entertainment",
        "aliases": ["YOUTUBE PREMIUM BILL", "GOOGLE YOUTUBE"]
    },
    "Apollo Pharmacy": {
        "category": "Healthcare",
        "aliases": ["APOLLO PHARMACIES", "APOLLO HOSPITALS", "APOLLO CLINIC", "APOLLO HEALTH"]
    },
    "1mg": {
        "category": "Healthcare",
        "aliases": ["TATA 1MG", "1MG TECHNOLOGIES", "1MG HEALTHCARE"]
    },
    "NetMeds": {
        "category": "Healthcare",
        "aliases": ["NETMEDS MARKETPLACE", "NETMEDS ONLINE", "NETMEDS PHARMACY"]
    },
    "Practo": {
        "category": "Healthcare",
        "aliases": ["PRACTO TECHNOLOGIES", "PRACTO CONSULTATION", "PRACTO HEALTH"]
    },
    "Udemy": {
        "category": "Education",
        "aliases": ["UDEMY INDIA", "UDEMY ONLINE", "UDEMY COURSE"]
    },
    "Coursera": {
        "category": "Education",
        "aliases": ["COURSERA ONLINE", "COURSERA INDIA", "COURSERA COURSE"]
    },
    "Unacademy": {
        "category": "Education",
        "aliases": ["SORTING HAT TECHNOLOGIES", "UNACADEMY LEARNING", "UNACADEMY APP"]
    },
    "Physics Wallah": {
        "category": "Education",
        "aliases": ["PHYSICSWALLAH", "PW ONLINE", "PW APP"]
    },
    "Byjus": {
        "category": "Education",
        "aliases": ["THINK AND LEARN", "BYJUS LEARNING", "BYJUS APP"]
    },
    "Scaler": {
        "category": "Education",
        "aliases": ["SCALER ACADEMY", "INTERVIEWBIT", "SCALER LERNING"]
    },
    "Groww": {
        "category": "Finance",
        "aliases": ["GROWW INVESTMENTS", "GROWW MUTUAL FUND", "NEXTBILLION TECHNOLOGY", "GROWW BROKING"]
    },
    "Zerodha": {
        "category": "Finance",
        "aliases": ["ZERODHA BROKING", "ZERODHA ONLINE", "ZERODHA MUTUAL FUND", "RAINMATTER"]
    },
    "Upstox": {
        "category": "Finance",
        "aliases": ["UPSTOX SECURITIES", "RKSV SECURITIES", "UPSTOX ONLINE"]
    },
    "Angel One": {
        "category": "Finance",
        "aliases": ["ANGEL ONE LIMITED", "ANGEL BROKING", "ANGEL ONE ONLINE", "ANGEL ONE"]
    },
    "Paytm Money": {
        "category": "Finance",
        "aliases": ["PAYTM MONEY LTD", "PAYTM MUTUAL FUND", "PAYTM STOCK"]
    },
    "LIC": {
        "category": "Insurance",
        "aliases": ["LIFE INSURANCE CORP", "LIC OF INDIA", "LIC PREMIUM"]
    },
    "PolicyBazaar": {
        "category": "Insurance",
        "aliases": ["POLICYBAZAAR INSURANCE", "PB FINTECH", "POLICY BAZAAR"]
    },
    "HDFC Life": {
        "category": "Insurance",
        "aliases": ["HDFC LIFE INSURANCE", "HDFC STANDARD LIFE"]
    },
    "ICICI Lombard": {
        "category": "Insurance",
        "aliases": ["ICICI LOMBARD GENERAL", "ICICI LOMBARD GIC"]
    },
    "Indian Oil": {
        "category": "Fuel",
        "aliases": ["INDIAN OIL CORP", "IOCL", "INDIAN OIL PETROL"]
    },
    "BPCL": {
        "category": "Fuel",
        "aliases": ["BHARAT PETROLEUM", "BPCL PUMP", "BPCL PETROL"]
    },
    "HP Petrol Pump": {
        "category": "Fuel",
        "aliases": ["HINDUSTAN PETROLEUM", "HPCL", "HP PETROL"]
    },
    "Shell": {
        "category": "Fuel",
        "aliases": ["SHELL INDIA", "SHELL PETROL", "SHELL PUMP"]
    },
    "Landlord": {
        "category": "Rent",
        "aliases": ["HOUSE RENT", "OWNER RENT", "FLAT RENT"]
    },
    "House Owner": {
        "category": "Rent",
        "aliases": ["ROOM RENT", "OWNER TRANSFER", "HOUSE OWNER RENT"]
    },
    "PM CARES": {
        "category": "Donation",
        "aliases": ["PM CARES FUND", "PRIME MINISTER RELIEF"]
    },
    "ISKCON": {
        "category": "Donation",
        "aliases": ["ISKCON TEMPLE", "ISKCON DONATION"]
    },
    "Akshaya Patra": {
        "category": "Donation",
        "aliases": ["AKSHAYA PATRA FOUNDATION", "AKSHAYAPATRA"]
    },
    "Rahul": {
        "category": "Personal Transfer",
        "aliases": ["RAHUL SHARMA", "RAHUL KUMAR", "RAHUL SINGH"]
    },
    "Amit": {
        "category": "Personal Transfer",
        "aliases": ["AMIT KUMAR", "AMIT SINGH", "AMIT SHARMA"]
    },
    "Priya": {
        "category": "Personal Transfer",
        "aliases": ["PRIYA SHARMA", "PRIYA KUMAR", "PRIYA SINGH"]
    },
    "Neha": {
        "category": "Personal Transfer",
        "aliases": ["NEHA KUMAR", "NEHA SHARMA", "NEHA SINGH"]
    },
    "Cult Fit": {
        "category": "Fitness",
        "aliases": ["CULTFIT", "CULT GYM", "CUREFIT", "CURE FIT"]
    },
    "Gold Gym": {
        "category": "Fitness",
        "aliases": ["GOLDS GYM", "GOLDS GYM INDIA"]
    },
    "Anytime Fitness": {
        "category": "Fitness",
        "aliases": ["ANYTIME FITNESS INDIA", "ANYTIME GYM"]
    },
    "Lakme": {
        "category": "Beauty",
        "aliases": ["LAKME SALON", "LAKME ACADEMY", "LAKME COSMETICS"]
    },
    "Purplle": {
        "category": "Beauty",
        "aliases": ["PURPLLE ONLINE", "PURPLLE COSMETICS"]
    },
    "Mamaearth": {
        "category": "Beauty",
        "aliases": ["HONASA CONSUMER", "MAMAEARTH PRODUCTS", "MAMAEARTH ONLINE"]
    },
    "Croma": {
        "category": "Electronics",
        "aliases": ["CROMA RETAIL", "INFINITI RETAIL", "CROMA ONLINE"]
    },
    "Reliance Digital": {
        "category": "Electronics",
        "aliases": ["RELIANCE DIGITAL RESQ", "RELIANCE DIGITAL STORE"]
    },
    "Vijay Sales": {
        "category": "Electronics",
        "aliases": ["VIJAY SALES STORE", "VIJAY SALES ONLINE"]
    },
    "ChatGPT": {
        "category": "Subscription",
        "aliases": ["OPENAI", "CHATGPT PLUS", "CHATGPT SUBSCRIPTION"]
    },
    "Canva": {
        "category": "Subscription",
        "aliases": ["CANVA DESIGN", "CANVA PRO", "CANVA PREMIUM"]
    },
    "GitHub": {
        "category": "Subscription",
        "aliases": ["GITHUB COPILOT", "GITHUB SPONSORS", "GITHUB INC"]
    },
    "Notion": {
        "category": "Subscription",
        "aliases": ["NOTION LABS", "NOTION PRO", "NOTION SUBSCRIPTION", "NOTION PAY"]
    },
    "Passport Seva": {
        "category": "Government",
        "aliases": ["PASSPORT OFFICE", "PASSPORT SERVICE"]
    },
    "Income Tax": {
        "category": "Government",
        "aliases": ["INCOME TAX DEPT", "INCOME TAX E-FILING", "IT DEPT"]
    },
    "GST Portal": {
        "category": "Government",
        "aliases": ["GSTIN", "GST BILL", "GOODS AND SERVICES TAX"]
    },
    "PhonePe": {
        "category": "Finance",
        "aliases": ["PHONE PE", "PHONEPE PVT LTD", "PHONEPE TRANSACTION", "PHONEPE WALLET"]
    },
    "Google Pay": {
        "category": "Finance",
        "aliases": ["GPAY", "GOOGLEPAY", "GOOGLE INDIA DIGITAL", "GOOGLE PAY INDIA"]
    },
    "Paytm": {
        "category": "Finance",
        "aliases": ["PAYTMPG", "PAYTM PAYMENTS", "PAYTM WALLET", "ONE97 COMMUNICATIONS", "PAYTM ONLINE"]
    }
}

# =====================================================
# PROGRAMMATIC ALIAS GENERATOR (Guarantees 500+ Entries)
# =====================================================

MERCHANT_ALIASES: Dict[str, str] = {}

# Expand dictionary to reach 500+ aliases programmatically
for canonical, info in CANONICAL_MERCHANTS.items():
    category = info["category"]
    
    # Store standard combinations
    MERCHANT_ALIASES[canonical.upper()] = canonical
    
    # Pre-defined aliases
    for alias in info["aliases"]:
        MERCHANT_ALIASES[alias.upper()] = canonical
        
    # Programmatic corporate suffixes (Adds highly realistic real-world combinations)
    corporate_suffixes = [
        " PVT LTD", " LTD", " LIMITED", " ONLINE", " SERVICES", 
        " INDIA", " PAY", " STORE", " RETAIL", " SHOP", " PRIVATE LIMITED"
    ]
    for suffix in corporate_suffixes:
        expanded = (canonical + suffix).upper()
        MERCHANT_ALIASES[expanded] = canonical
        
        # Expand primary alias with suffixes too
        primary_alias = info["aliases"][0]
        expanded_alias = (primary_alias + suffix).upper()
        MERCHANT_ALIASES[expanded_alias] = canonical

# =====================================================
# REGEX & NLP EXTRACTION PIPELINE
# =====================================================

# Suffix keywords indicating stops for the lazy capture groups
SUFFIX_STOPS = r'(?:\s+Ref\b|\s+UTR\b|\s+via\b|\s+on\b|\s+at\b|\s+Rs\b|\s+INR\b|\s+\-\s+|\.|$)'

MERCHANT_PATTERNS: List[str] = [
    # Explicit merchant labels
    r'(?:merchant name|merchant|payee|receiver|beneficiary|sender|org|business|company|store name)[:\s\-]+([^,\n.]+)',
    
    # Payments and Transfers (Debits/Credits)
    rf'transfer(?:red)? to\s+([^,\n.]+?){SUFFIX_STOPS}',
    rf'transfer(?:red)? from\s+([^,\n.]+?){SUFFIX_STOPS}',
    rf'trf to\s+([^,\n.]+?){SUFFIX_STOPS}',
    rf'trf from\s+([^,\n.]+?){SUFFIX_STOPS}',
    rf'payment(?: made)? to\s+([^,\n.]+?){SUFFIX_STOPS}',
    rf'paid(?: via UPI| through UPI| using UPI)? to\s+([^,\n.]+?){SUFFIX_STOPS}',
    rf'paid using UPI at\s+([^,\n.]+?){SUFFIX_STOPS}',
    rf'spent(?: using UPI)? at\s+([^,\n.]+?){SUFFIX_STOPS}',
    rf'purchase at\s+([^,\n.]+?){SUFFIX_STOPS}',
    rf'POS purchase at\s+([^,\n.]+?){SUFFIX_STOPS}',
    rf'online payment to\s+([^,\n.]+?){SUFFIX_STOPS}',
    
    # Generic "towards", "for", "at", or "to" patterns
    rf'towards\s+([^,\n.]+?){SUFFIX_STOPS}',
    rf'for\s+([^,\n.]+?){SUFFIX_STOPS}',
    rf'\bat\s+([^,\n.]+?){SUFFIX_STOPS}',
    rf'to VPA\s+([^,\n.]+?){SUFFIX_STOPS}',
    
    # Received from patterns (Credits)
    rf'received from\s+([^,\n.]+?){SUFFIX_STOPS}',
    rf'credit from\s+([^,\n.]+?){SUFFIX_STOPS}',
    
    # Standard "to XYZ" debits
    rf'\bto\s+([^,\n.]+?){SUFFIX_STOPS}',
]

# VPA Pattern matching
VPA_PATTERN = r'\b([a-zA-Z0-9.-]+@[a-zA-Z]+)\b'

def clean_merchant(text: str) -> str:
    """
    Cleans merchant strings by removing noise (UTRs, dates, amounts, bank names, etc.).
    """
    if not text or text.upper() == "NAN":
        return ""
    
    # Convert to string and decode spaces
    cleaned = text.strip()
    
    # Remove VPAs domain suffix (e.g. "@okhdfcbank") instead of stripping the entire word before "@"
    cleaned = re.sub(r'@[a-zA-Z0-9.-]+', '', cleaned)
    
    # Remove Ref/UTR/Txn numbers (10 to 16+ digits)
    cleaned = re.sub(r'\b\d{10,16}\b', '', cleaned)
    cleaned = re.sub(r'\b(?:Ref No|Ref|UTR|Txn|Txn ID)[:\s\-]*[A-Z0-9]+', '', cleaned, flags=re.IGNORECASE)
    
    # Remove Date/Time stamps
    cleaned = re.sub(r'\b\d{2}[A-Za-z]{3}\d{2,4}\b', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\b\d{2}[\-\/]\d{2}[\-\/]\d{2,4}\b', '', cleaned)
    cleaned = re.sub(r'\b\d{4}[\-\/]\d{2}[\-\/]\d{2}\b', '', cleaned)
    
    # Remove Amounts
    cleaned = re.sub(r'\b(?:Rs\.?|INR)\s*\d+(?:\.\d+)?\b', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\b\d+(?:\.\d+)?\s*(?:Rs|INR)\b', '', cleaned, flags=re.IGNORECASE)
    
    # Remove trailing bank identifiers (e.g. "- ICICI Bank", "-AXIS", etc.)
    cleaned = re.sub(r'[\-\s]+(?:SBI|HDFC|ICICI|AXIS|PNB|KOTAK|BOB|CANARA|UNION|IDFC|YES BANK|INDUSIND|FEDERAL|RBL|UCO|KOTAK)\s*Bank\b', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'[\-\s]+(?:SBI|HDFC|ICICI|AXIS|PNB|KOTAK|BOB|CANARA|UNION|IDFC|YES BANK|INDUSIND|FEDERAL|RBL|UCO|KOTAK)\b', '', cleaned, flags=re.IGNORECASE)
    
    # Remove common filler words
    filler_patterns = [
        r'\bvia\b', r'\bthrough\b', r'\busing\b', r'\bUPI\b', r'\bIMPS\b', 
        r'\bNEFT\b', r'\bRTGS\b', r'\bdebited\b', r'\bcredited\b', r'\btransfer\b',
        r'\bsent\b', r'\bpaid\b', r'\bspent\b', r'\bsuccessful\b', r'\bfrom\b', r'\bon\b'
    ]
    for pattern in filler_patterns:
        cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
        
    # Clean special characters and duplicate spaces
    cleaned = re.sub(r'[^a-zA-Z0-9\s\.\&\-]', ' ', cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    return cleaned

def merchant_candidates(sms: str) -> List[Dict]:
    """
    Finds potential merchant string candidates using Regex and spaCy NER.
    """
    candidates = []
    
    # 1. Check for VPAs/UPI IDs
    vpa_matches = re.findall(VPA_PATTERN, sms)
    for vpa in vpa_matches:
        candidates.append({"text": vpa, "source": "vpa"})
        # Extract handle prefix before the '@' as a candidate
        handle = vpa.split('@')[0]
        # Clean handles that might contain numbers/dots (e.g., swiggy.instamart123 -> swiggy.instamart)
        handle_cleaned = re.sub(r'\d+', '', handle).strip('.-')
        if len(handle_cleaned) > 2:
            candidates.append({"text": handle_cleaned, "source": "vpa_handle"})
            
    # 2. Run regex patterns
    for pattern in MERCHANT_PATTERNS:
        match = re.search(pattern, sms, re.IGNORECASE)
        if match:
            candidate_text = match.group(1).strip()
            if candidate_text:
                candidates.append({"text": candidate_text, "source": "regex"})
                
    # 3. Run spaCy NER if regex candidates are missing or weak
    if nlp:
        doc = nlp(sms)
        for ent in doc.ents:
            if ent.label_ in ["ORG", "PERSON"]:
                # Exclude bank names and technical terms from ORG detection
                ent_text = ent.text.upper()
                is_bank = any(b in ent_text for b in ["BANK", "SBI", "HDFC", "ICICI", "AXIS", "PNB", "KOTAK", "BOB", "CANARA", "UNION", "IDFC", "RBL", "UCO", "FEDERAL", "INDUSIND"])
                is_noise = ent_text in ["UTR", "REF", "TXN", "UPI", "IMPS", "NEFT", "RTGS", "RS", "INR"]
                if not is_bank and not is_noise:
                    candidates.append({"text": ent.text, "source": "ner"})
                    
    return candidates

def score_candidate(candidate: str, source: str) -> Tuple[float, Optional[str]]:
    """
    Scores a candidate based on alias match, fuzzy match, and extraction source.
    Returns: (Score, Normalized/Canonical Name)
    """
    cleaned = clean_merchant(candidate).upper()
    if not cleaned or len(cleaned) < 2:
        return 0.0, None
        
    # Check if candidate is just a bank account number (e.g. "A C X1234", "AC XX1234", etc.)
    if re.match(r'^A\s*C\s*X+', cleaned) or re.match(r'^A\s*[\/\s]\s*C\s*X+', cleaned) or re.match(r'^ACCOUNT\s*X+', cleaned):
        return 0.0, None
        
    # Check 1: Exact Alias match (Score: 0.95 - 0.98)
    if cleaned in MERCHANT_ALIASES:
        source_boost = 0.03 if source in ["regex", "vpa_handle"] else 0.0
        return 0.95 + source_boost, MERCHANT_ALIASES[cleaned]
        
    # Check 2: Fuzzy match with known aliases using RapidFuzz (Score: Up to 0.90)
    # Get best fuzzy match from the keys of MERCHANT_ALIASES
    alias_keys = list(MERCHANT_ALIASES.keys())
    best_match = process.extractOne(cleaned, alias_keys, scorer=fuzz.ratio)
    
    if best_match:
        match_string, match_score, _ = best_match
        if match_score >= 80.0:  # Threshold of 80%
            normalized_name = MERCHANT_ALIASES[match_string]
            # Scale score between 0.60 and 0.90 based on match ratio
            scaled_score = 0.60 + (match_score - 80.0) * (0.30 / 20.0)
            # Add a slight source weight
            if source == "regex":
                scaled_score += 0.05
            elif source == "vpa_handle":
                scaled_score += 0.03
            return min(scaled_score, 0.94), normalized_name

    # Check 3: Raw candidate score without normalization
    # Give a default baseline score based on extraction source
    if source == "regex":
        return 0.75, None
    elif source == "vpa_handle":
        return 0.70, None
    elif source == "vpa":
        return 0.65, None
    elif source == "ner":
        return 0.55, None
        
    return 0.20, None

def extract_merchant(sms: str) -> Tuple[str, float]:
    """
    Extracts the merchant name from the SMS, normalized if possible, with a confidence score.
    Returns: (Merchant Name, Confidence Score)
    """
    candidates = merchant_candidates(sms)
    if not candidates:
        return "NaN", 0.0
        
    best_merchant = "NaN"
    best_score = 0.0
    
    for item in candidates:
        score, normalized = score_candidate(item["text"], item["source"])
        if score > best_score:
            best_score = score
            best_merchant = normalized if normalized else clean_merchant(item["text"])
            
    # Apply a final clean to the best candidate if it wasn't normalized
    if best_merchant != "NaN" and best_merchant.upper() not in [m.upper() for m in CANONICAL_MERCHANTS.keys()]:
        best_merchant = clean_merchant(best_merchant).title()
        
    if not best_merchant or best_merchant == "Nan":
        best_merchant = "NaN"
        best_score = 0.0
        
    return best_merchant, round(best_score, 2)

def normalize_merchant(merchant: str) -> str:
    """
    Utility wrapper to resolve a merchant name to its canonical form if it exists.
    """
    merchant_upper = merchant.upper().strip()
    if merchant_upper in MERCHANT_ALIASES:
        return MERCHANT_ALIASES[merchant_upper]
    return merchant

def categorize_merchant(merchant: str) -> str:
    """
    Assigns a spending category to the merchant using multiple search tiers:
    Exact match -> Alias match -> Fuzzy match -> Keyword match.
    """
    if not merchant or merchant == "NaN":
        return "Miscellaneous"
        
    merchant_upper = merchant.upper().strip()
    
    # Tier 1: Exact Canonical Match
    for canonical, info in CANONICAL_MERCHANTS.items():
        if merchant_upper == canonical.upper():
            return info["category"]
            
    # Tier 2: Alias Dictionary Map
    if merchant_upper in MERCHANT_ALIASES:
        canonical_name = MERCHANT_ALIASES[merchant_upper]
        return CANONICAL_MERCHANTS[canonical_name]["category"]
        
    # Tier 3: Fuzzy match with canonical names
    canonical_names = list(CANONICAL_MERCHANTS.keys())
    best_match = process.extractOne(merchant_upper, [c.upper() for c in canonical_names], scorer=fuzz.ratio)
    if best_match:
        match_string, match_score, _ = best_match
        if match_score >= 85.0:
            for canonical in canonical_names:
                if canonical.upper() == match_string:
                    return CANONICAL_MERCHANTS[canonical]["category"]
                    
    # Tier 4: Keyword matching rules (Word-boundary based to avoid substring bugs)
    category_keywords = {
        "Food": [r'\bZOMATO\b', r'\bSWIGGY\b', r'\bFOOD\b', r'\bRESTAURANT\b', r'\bCAFE\b', r'\bPIZZA\b', r'\bBURGER\b', r'\bBAKERY\b', r'\bCATERERS\b', r'\bKITCHEN\b'],
        "Travel": [r'\bUBER\b', r'\bOLA\b', r'\bRAPIDO\b', r'\bCABS\b', r'\bTRAVEL\b', r'\bMETRO\b', r'\bRAILWAY\b', r'\bFLIGHT\b', r'\bBUS\b', r'\bTOUR\b', r'\bCAR\b', r'\bYATRA\b'],
        "Shopping": [r'\bAMAZON\b', r'\bFLIPKART\b', r'\bMYNTRA\b', r'\bAJIO\b', r'\bMALL\b', r'\bSTORE\b', r'\bFASHION\b', r'\bCLOTH\b', r'\bAPPAREL\b', r'\bSHOPSY\b', r'\bMEESHO\b'],
        "Groceries": [r'\bGROCERY\b', r'\bSUPERMARKET\b', r'\bMART\b', r'\bBLINKIT\b', r'\bZEPTO\b', r'\bINSTAMART\b', r'\bFRESH\b', r'\bPROVISION\b'],
        "Recharge": [r'\bRECHARGE\b', r'\bAIRTEL\b', r'\bJIO\b', r'\bBSNL\b', r'\bVODAFONE\b', r'\bIDEA\b', r'\bMOBILE\b'],
        "Utilities": [r'\bPOWER\b', r'\bELECTRICITY\b', r'\bWATER\b', r'\bGAS\b', r'\bBILL\b', r'\bUPPCL\b', r'\bENERGY\b'],
        "Finance": [r'\bINVEST\b', r'\bMUTUAL\b', r'\bSECURITIES\b', r'\bBROKING\b', r'\bGROWW\b', r'\bZERODHA\b', r'\bUPSTOX\b', r'\bFINANCE\b', r'\bPAYTM\b', r'\bPHONEPE\b'],
        "Healthcare": [r'\bPHARMACY\b', r'\bHOSPITAL\b', r'\bCLINIC\b', r'\bHEALTH\b', r'\bMEDICAL\b', r'\bCHEMIST\b', r'\bDR\b', r'\bDOCTOR\b'],
        "Education": [r'\bSCHOOL\b', r'\bCOLLEGE\b', r'\bUNIVERSITY\b', r'\bACADEMY\b', r'\bCOURSE\b', r'\bCLASSES\b', r'\bUDEMY\b', r'\bBYJUS\b', r'\bPW\b'],
        "Fuel": [r'\bPETROL\b', r'\bFUEL\b', r'\bHPCL\b', r'\bIOCL\b', r'\bBPCL\b', r'\bSHELL\b', r'\bOIL\b'],
        "Subscription": [r'\bCHATGPT\b', r'\bOPENAI\b', r'\bCANVA\b', r'\bGITHUB\b', r'\bNOTION\b', r'\bMICROSOFT\b', r'\bADOBE\b'],
        "Entertainment": [r'\bNETFLIX\b', r'\bSPOTIFY\b', r'\bHOTSTAR\b', r'\bPLAY\b', r'\bCINEMA\b', r'\bTHEATRE\b', r'\bSHOW\b', r'\bPRIME\b', r'\bMUSIC\b'],
        "Government": [r'\bTAX\b', r'\bGST\b', r'\bGOVT\b', r'\bPASSPORT\b', r'\bCHALLAN\b', r'\bPORTAL\b'],
        "Donation": [r'\bDONATION\b', r'\bCHARITY\b', r'\bFUND\b', r'\bTRUST\b', r'\bRELIEF\b', r'\bISKCON\b']
    }
    
    for category, patterns in category_keywords.items():
        for pattern in patterns:
            if re.search(pattern, merchant_upper):
                return category
                
    return "Miscellaneous"
