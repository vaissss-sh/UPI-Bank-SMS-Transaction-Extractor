import random
import re
from typing import List, Dict
from app import extract_info
from merchant_pipeline import CANONICAL_MERCHANTS

# Define bank, app, and merchant lists
BANKS = [
    "SBI", "HDFC", "ICICI", "AXIS", "PNB", "KOTAK", "BOB", "CANARA", 
    "UNION", "IDFC", "YES BANK", "INDUSIND", "FEDERAL", "RBL", "UCO", 
    "Airtel Payments Bank", "Paytm Payments Bank"
]

APPS = [
    "PhonePe", "Google Pay", "Paytm", "BHIM", "Amazon Pay", 
    "CRED", "Mobikwik", "WhatsApp Pay", "Freecharge"
]

# Get list of canonical merchants and their categories
MERCHANT_INFO = [(name, info["category"]) for name, info in CANONICAL_MERCHANTS.items()]

# Standard Indian SMS templates
DEBIT_TEMPLATES = [
    "Dear {bank} User, your A/c X{acc} debited by Rs.{amount} on {date} trf to {merchant_var} Ref No {ref}",
    "Transaction successful. Rs.{amount} paid to {merchant_var} via UPI Ref {ref} on {date}",
    "Your A/c XX{acc} is debited by Rs.{amount} on {date} towards {merchant_var} - {bank} Bank",
    "UPI Txn Successful. Rs.{amount} debited from A/c XX{acc} towards {merchant_var} Ref {ref}",
    "Spent Rs.{amount} at {merchant_var} on {date} using {app} Ref {ref}",
    "Rs.{amount} spent using UPI at {merchant_var} Ref No {ref} on {date}",
    "Payment of Rs.{amount} successful to {merchant_var} via UPI Ref {ref}",
    "A/c XX{acc} debited by Rs.{amount} for {merchant_var} on {date} UTR {ref}"
]

CREDIT_TEMPLATES = [
    "Dear {bank} User, your A/c X{acc}-credited by Rs.{amount} on {date} transfer from {merchant_var} Ref No {ref} -{bank_partner}",
    "Your A/c XX{acc} has been credited with Rs.{amount} on {date} transfer from {merchant_var} via UPI Ref {ref}",
    "Money received from {merchant_var} Rs.{amount} to A/c X{acc} Ref {ref}",
    "Dear SBI User, your A/c X{acc}-credited by Rs.{amount} on {date} transfer from {merchant_var} Ref No {ref}"
]

def generate_200_samples() -> List[Dict]:
    random.seed(42)  # For deterministic generation
    samples = []
    
    # We want exactly 200 samples
    for i in range(200):
        # Pick a merchant and its category
        merchant, category = random.choice(MERCHANT_INFO)
        
        # Create a realistic variation of the merchant name (alias style)
        alias_choices = [
            merchant, 
            merchant.upper(),
            f"{merchant} Ltd",
            f"{merchant} Pvt Ltd",
            f"{merchant.upper()} ONLINE",
            f"{merchant} Store",
            f"{merchant.upper()} PAY",
            f"{merchant.lower()}@okhdfcbank" if random.random() > 0.5 else merchant
        ]
        merchant_var = random.choice(alias_choices)
        
        # Decide transaction type
        txn_type = "Credit" if i % 4 == 0 else "Debit"  # 25% credit, 75% debit
        
        # Random parameters
        bank = random.choice(BANKS)
        bank_partner = random.choice(BANKS)
        app = random.choice(APPS)
        acc = str(random.randint(1000, 9999))
        amount = str(round(random.uniform(10.0, 50000.0), 2))
        date = f"{random.randint(10, 28)}Aug26"
        ref = "".join([str(random.randint(0, 9)) for _ in range(12)])
        
        # Select and format template
        if txn_type == "Debit":
            template = random.choice(DEBIT_TEMPLATES)
            sms_text = template.format(
                bank=bank, acc=acc, amount=amount, date=date, 
                merchant_var=merchant_var, ref=ref, app=app
            )
        else:
            template = random.choice(CREDIT_TEMPLATES)
            sms_text = template.format(
                bank=bank, acc=acc, amount=amount, date=date, 
                merchant_var=merchant_var, ref=ref, bank_partner=bank_partner
            )
            
        samples.append({
            "sms_text": sms_text,
            "expected_merchant": merchant,
            "expected_category": category,
            "txn_type": txn_type
        })
        
    return samples

def run_tests():
    samples = generate_200_samples()
    correct_merchants = 0
    correct_categories = 0
    
    print("=" * 100)
    print(f"{'INDEX':<6} | {'TXN':<6} | {'EXTRACTED MERCHANT':<25} | {'EXPECTED':<15} | {'CATEGORY':<15} | {'CONF':<5} | {'STATUS'}")
    print("=" * 100)
    
    for idx, sample in enumerate(samples, 1):
        parsed = extract_info(sample["sms_text"])
        
        # Import confidence scoring dynamically for reporting
        from merchant_pipeline import extract_merchant
        _, confidence = extract_merchant(sample["sms_text"])
        
        extracted_m = parsed["merchant"]
        expected_m = sample["expected_merchant"]
        extracted_c = parsed["category"]
        expected_c = sample["expected_category"]
        
        # A match is case-insensitive match on normalized/canonical merchant
        is_merchant_correct = extracted_m.lower() == expected_m.lower()
        is_category_correct = extracted_c.lower() == expected_c.lower()
        
        if is_merchant_correct:
            correct_merchants += 1
        if is_category_correct:
            correct_categories += 1
            
        status = "OK" if is_merchant_correct else "FAIL"
        
        # Print a selection or all if needed. Let's print every 10th sample, plus all failed samples.
        if idx <= 20 or idx % 10 == 0 or not is_merchant_correct:
            print(f"{idx:<6} | {sample['txn_type']:<6} | {extracted_m:<25} | {expected_m:<15} | {extracted_c:<15} | {confidence:<5.2f} | {status}")
            
    merchant_accuracy = (correct_merchants / len(samples)) * 100
    category_accuracy = (correct_categories / len(samples)) * 100
    
    print("=" * 100)
    print(f"RESULTS SUMMARY:")
    print(f"Total Test Samples: {len(samples)}")
    print(f"Merchant Extraction Accuracy: {merchant_accuracy:.2f}% (Target: >= 95%)")
    print(f"Category Detection Accuracy: {category_accuracy:.2f}%")
    print("=" * 100)

if __name__ == "__main__":
    run_tests()
