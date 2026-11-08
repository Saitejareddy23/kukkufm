"""
Curated, Verified Statutory Knowledge Base for Indian Everyday Legal Issues.
Prevents LLM hallucination by restricting citations to verified Indian acts and rules.
"""

import re

VERIFIED_STATUTES = {
    "TENANCY_DEPOSIT": {
        "domain": "Tenancy & Security Deposit Recovery",
        "primary_law": "Transfer of Property Act, 1882 (Section 108(m) - Reasonable Wear & Tear) & Model Tenancy Act principles",
        "summary": "Landlord cannot unilaterally forfeit security deposit for normal wear and tear unless explicitly detailed with written invoices. Security deposit must be refunded within 30 days of vacant possession.",
        "key_provisions": [
            "Transfer of Property Act, 1882, Section 108: Lessee is bound to keep property in good condition, reasonable wear and tear excepted.",
            "Indian Contract Act, 1872, Section 73: Compensation for loss or damage caused by breach of contract.",
            "State Rent Control Acts / Model Tenancy Framework: Maximum deposit limits and mandatory settlement timeline."
        ],
        "remedies": [
            "Issue formal 15-day Legal Demand Notice demanding refund with 18% p.a. interest.",
            "File petition before Rent Authority / Rent Court (where Model Tenancy Act is notified) or Civil Court (Summary Suit under Order XXXVII CPC for liquidated debt).",
            "File Consumer Complaint if landlord is a commercial co-living company (e.g., Stanza, Zolo) under Consumer Protection Act, 2019."
        ],
        "evidence_needed": [
            "Registered or signed Rental Agreement",
            "Proof of initial deposit payment (bank transaction/UPI receipt)",
            "Notice of termination given via Email/WhatsApp with date of handover",
            "Photos/videos of the empty flat showing clean condition at handover",
            "Keys handover acknowledgement or chat confirmation"
        ]
    },
    "CONSUMER_REFUND": {
        "domain": "Consumer Protection & E-Commerce Disputes",
        "primary_law": "Consumer Protection Act, 2019 & Consumer Protection (E-Commerce) Rules, 2020",
        "summary": "Consumers have statutory right against deficiency in service and unfair trade practices. Sellers and marketplace platforms cannot hide behind unreasonable return policies if defective/wrong goods were delivered.",
        "key_provisions": [
            "Consumer Protection Act, 2019, Section 2(47): Definition of 'Unfair Trade Practice' including deceptive claims and refusing refund for defective items.",
            "Consumer Protection Act, 2019, Section 2(11): Definition of 'Deficiency in Service'.",
            "Consumer Protection (E-Commerce) Rules, 2020, Rule 5 & 6: Mandatory grievance officer, 48-hour acknowledgement, and refund obligations."
        ],
        "remedies": [
            "Issue formal 15-day Legal Demand Notice to seller and e-commerce platform.",
            "Register grievance on National Consumer Helpline (NCH / 1915 or consumerhelpline.gov.in / INGRAM portal).",
            "File online complaint on e-Daakhil portal (edaakhil.nic.in) before the District Consumer Disputes Redressal Commission."
        ],
        "evidence_needed": [
            "Tax Invoice / Order Confirmation with Order ID",
            "Unboxing video or photographs of the defective/wrong product",
            "Support ticket history / Email threads / Chat logs showing timely complaint",
            "Payment proof (Credit card / UPI statement)",
            "Refusal email or arbitrary ticket closure confirmation"
        ]
    },
    "UNPAID_SALARY": {
        "domain": "Unpaid Wages, Notice Pay & F&F Settlement",
        "primary_law": "Payment of Wages Act, 1936 & Indian Contract Act, 1872 (Section 73)",
        "summary": "Employers are legally obligated to disburse earned wages and clear Full & Final (F&F) settlement within statutory timelines (typically by 7th-10th of succeeding month, or within 30 days of resignation).",
        "key_provisions": [
            "Payment of Wages Act, 1936, Section 5: Time of payment of wages (before expiry of 7th or 10th day).",
            "Payment of Wages Act, 1936, Section 7: Authorized deductions only; arbitrary forfeiture is illegal.",
            "Indian Contract Act, 1872, Section 73: Breach of employment agreement and recovery of dues."
        ],
        "remedies": [
            "Issue formal 15-day Legal Demand Notice to Managing Director and HR.",
            "File complaint with the jurisdictional State Labour Commissioner (Conciliation Officer).",
            "For non-workman/managerial employees, initiate civil recovery summary suit or Section 9 IBC (Insolvency) notice if company is corporate debtor (>₹1 Cr threshold) or MSME Samadhaan if eligible."
        ],
        "evidence_needed": [
            "Appointment Letter / Employment Agreement showing CTC and notice terms",
            "Salary slips of prior months",
            "Bank statements showing cessation of salary credits",
            "Resignation email, acceptance confirmation, and handover sign-off",
            "Follow-up emails sent to HR/Finance demanding F&F settlement"
        ]
    }
}

OUT_OF_SCOPE_TRIGGERS = [
    r'\bmurder\b', r'\bkill\b', r'\bassault\b', r'\brape\b', r'\bsexual\b',
    r'\bbail\b', r'\bfir\b', r'\bpolice station\b', r'\barrested\b', r'\bjail\b',
    r'\bdowry\b', r'\bdivorce\b', r'\bcustody\b', r'\bancestral land\b', r'\bwill contest\b',
    r'\bdrugs\b', r'\bndps\b', r'\bcheque bounce\b', r'\bsec 138\b', r'\briot\b'
]

def check_scope(text):
    """Verifies whether the matter is within everyday civil/consumer scope or requires immediate criminal/family advocate."""
    text_lower = text.lower()
    for trigger in OUT_OF_SCOPE_TRIGGERS:
        if re.search(trigger, text_lower):
            return {
                "in_scope": False,
                "reason": f"Matter touches criminal, matrimonial, or high-stakes civil litigation ('{trigger}').",
                "recommendation": "This platform strictly handles everyday civil, consumer, and employment disputes. For criminal, matrimonial, or custody matters, please immediately consult a qualified Advocate in your district court or approach the National Legal Services Authority (NALSA) Helpline at 15100 for free legal aid."
            }
            
    # Classify category
    if any(k in text_lower for k in ['rent', 'landlord', 'tenant', 'deposit', 'flat', 'broker', 'pg', 'lease', 'evict']):
        return {"in_scope": True, "category": "TENANCY_DEPOSIT"}
    elif any(k in text_lower for k in ['salary', 'wages', 'employer', 'hr', 'resignation', 'f&f', 'settlement', 'company unpaid', 'stipend']):
        return {"in_scope": True, "category": "UNPAID_SALARY"}
    elif any(k in text_lower for k in ['refund', 'amazon', 'flipkart', 'order', 'defective', 'warranty', 'flight', 'hotel', 'e-commerce', 'scam', 'product']):
        return {"in_scope": True, "category": "CONSUMER_REFUND"}
    else:
        return {"in_scope": True, "category": "CONSUMER_REFUND"} # Default everyday dispute
