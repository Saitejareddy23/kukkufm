"""
NyayaMitra: AI Legal Companion for Everyday Indian Disputes.
Extracts timelines, assesses legal rights, drafts Legal Demand Notices,
and provides roleplay negotiation practice without hallucinating laws.
"""

import os
import re
import json
import sys
from datetime import datetime

# Local imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from legal_knowledge_base import VERIFIED_STATUTES, check_scope

class CaseBuilder:
    def __init__(self, raw_story, user_details=None, respondent_details=None):
        self.raw_story = raw_story
        self.user = user_details or {"name": "Aggrieved Citizen", "city": "Bengaluru", "phone": "+91-9876543210"}
        self.respondent = respondent_details or {"name": "Opposite Party", "address": "Opposite Party Address"}
        self.scope_check = check_scope(raw_story)
        self.category = self.scope_check.get("category", "CONSUMER_REFUND") if self.scope_check["in_scope"] else None
        self.facts = {}
        self.timeline = []
        self.claim_amount = "To be assessed"
        self._extract_structured_facts()

    def _extract_structured_facts(self):
        text = self.raw_story
        
        # Extract financial amounts (Rs. or INR or numbers like 50,000 / 65000)
        amt_match = re.findall(r'(?:rs\.?|inr|₹)\s*([0-9,]+)', text, re.IGNORECASE)
        if amt_match:
            self.claim_amount = f"INR {amt_match[0].replace(',', '')}"
        else:
            # check bare 5-6 digit numbers
            num_match = re.findall(r'\b([1-9][0-9]{3,6})\b', text)
            if num_match:
                self.claim_amount = f"INR {num_match[0]}"

        # Extract dates / months
        date_patterns = [
            r'\b(\d{1,2}(?:st|nd|rd|th)?\s+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s*(?:\d{2,4})?)\b',
            r'\b((?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{1,2},?\s*(?:\d{2,4})?)\b',
            r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b',
            r'\b(last month|3 months ago|2 weeks ago|yesterday)\b'
        ]
        
        found_dates = []
        for pat in date_patterns:
            matches = re.findall(pat, text, re.IGNORECASE)
            for m in matches:
                found_dates.append(m)

        # Build chronological timeline
        sentences = [s.strip() for s in re.split(r'[.\n]+', text) if len(s.strip()) > 10]
        for idx, s in enumerate(sentences[:6]):
            date_hint = found_dates[idx] if idx < len(found_dates) else f"Phase {idx+1}"
            self.timeline.append({
                "phase": date_hint,
                "event": s
            })

    def get_case_summary(self):
        if not self.scope_check["in_scope"]:
            return {
                "status": "OUT_OF_SCOPE",
                "reason": self.scope_check["reason"],
                "recommendation": self.scope_check["recommendation"]
            }

        kb_info = VERIFIED_STATUTES[self.category]
        return {
            "status": "VALID_EVERYDAY_DISPUTE",
            "domain": kb_info["domain"],
            "disputed_amount": self.claim_amount,
            "timeline": self.timeline,
            "applicable_law": kb_info["primary_law"],
            "plain_language_summary": kb_info["summary"],
            "statutory_provisions": kb_info["key_provisions"],
            "remedies": kb_info["remedies"],
            "evidence_checklist": kb_info["evidence_needed"]
        }

    def draft_legal_notice(self, notice_date=None):
        if not self.scope_check["in_scope"]:
            return "CANNOT DRAFT: Matter is out of civil/consumer scope."

        kb = VERIFIED_STATUTES[self.category]
        ndate = notice_date or datetime.now().strftime("%d-%B-%Y")
        
        notice_text = f"""================================================================================
FORMAL LEGAL DEMAND NOTICE (WITHOUT PREJUDICE)
Issued under Section 108 Transfer of Property Act / Consumer Protection Act, 2019 / Indian Contract Act
================================================================================

DATE: {ndate}

BY REGISTERED POST A.D. / SPEED POST / LEGAL EMAIL NOTIFICATION

TO:
{self.respondent.get('name', 'Opposite Party')}
{self.respondent.get('address', 'Registered Address / Office Location')}
Email / Contact: {self.respondent.get('contact', 'contact@oppositeparty.com')}

FROM:
{self.user.get('name', 'Aggrieved Complainant')}
Residing at / Address: {self.user.get('address', self.user.get('city', 'Bengaluru, Karnataka'))}
Phone: {self.user.get('phone', '+91-XXXXXXXXXX')} | Email: {self.user.get('email', 'claimant@email.com')}

SUBJECT: FORMAL DEMAND NOTICE FOR IMMEDIATE RECOVERY OF {self.claim_amount} ALONG WITH 18% P.A. INTEREST TOWARDS UNLAWFUL WITHHOLDING AND DEFICIENCY IN SERVICE

Sir / Madam,

Under instructions and on behalf of my client / the undersigned, this formal Legal Demand Notice is hereby served upon you as follows:

1. FACTUAL RECITALS & TIMELINE:
   a. That the undersigned entered into a legally binding relationship / agreement with you regarding {kb['domain']}.
"""
        for i, item in enumerate(self.timeline, 1):
            notice_text += f"   b.{i} On/Around {item['phase']}: {item['event']}.\n"

        notice_text += f"""
2. NATURE OF BREACH & DEFICIENCY:
   a. That despite the undersigned having completely fulfilled all contractual and statutory obligations, you have arbitrarily, maliciously, and unlawfully withheld the legitimate sum of {self.claim_amount}.
   b. That your actions constitute a direct breach of contract under Section 73 of the Indian Contract Act, 1872, and amounts to an Unfair Trade Practice and Deficiency in Service as defined under Section 2(47) and Section 2(11) of the Consumer Protection Act, 2019.
   c. That specifically, {kb['summary']}

3. MANDATORY 15-DAY RECTIFICATION DEMAND:
   You are hereby called upon to pay and remit the outstanding sum of {self.claim_amount} directly into the bank account of the undersigned, along with interest calculated @ 18% per annum from the date it fell due until realization, within exactly FIFTEEN (15) DAYS from the receipt of this notice.

4. CONSEQUENCES OF DEFAULT:
   Please take note that if you fail to comply with the requisitions of this notice within the stipulated 15 days, the undersigned shall be constrained to initiate appropriate legal proceedings against you, including:
   i. Filing a formal statutory complaint before the competent District Consumer Disputes Redressal Commission / Rent Authority / Labour Commissioner;
   ii. Instituting a civil summary recovery suit before the Court of competent jurisdiction;
   In which event, you shall be held solely liable for all consequential legal expenses, litigation costs, and compensatory damages for severe mental agony and harassment.

A copy of this notice is retained in our records for future judicial submission.

Yours sincerely,

___________________________
{self.user.get('name', 'Aggrieved Complainant')}
(Signature / Digital Delivery Copy)
================================================================================
"""
        return notice_text

    def simulate_counterparty_objection(self, objection_type="typical"):
        """Plays the counterparty to help the citizen practice defending their position."""
        if not self.scope_check["in_scope"]:
            return "Roleplay disabled for out-of-scope matters."

        if self.category == "TENANCY_DEPOSIT":
            return {
                "opponent_role": "Aggressive Landlord",
                "opponent_message": "Listen, you vacated the flat in a terrible state! The walls need complete repainting and that costs 30,000. Plus 20,000 for deep cleaning and deep polish. I don't owe you anything. Go do whatever you want!",
                "coaching_tip": "Do NOT get emotional or shout back. Ground yourself in the law: Under Section 108 of the Transfer of Property Act, normal wear and tear is the landlord's responsibility. Demand written GST invoices for the alleged repainting and cite your dated handover photos.",
                "suggested_reply": "Dear Landlord, under Section 108(m) of the Transfer of Property Act, 1882, a tenant is only liable for willful damage, not normal wear and tear. I have timestamped photos and videos from the day of handover proving the flat was spotless. Please share itemized GST invoices for these alleged deductions within 48 hours, failing which my formal 15-day Legal Notice is being dispatched and we will proceed to the Rent Authority and Civil Court."
            }
        elif self.category == "UNPAID_SALARY":
            return {
                "opponent_role": "Evasive Startup HR / Founder",
                "opponent_message": "Our company policy says F&F takes 90 business days to audit, and because the company is facing cash flow issues, notice pay is waived. You cannot force us to pay earlier than policy.",
                "coaching_tip": "Company internal policy NEVER overrides statutory law. The Payment of Wages Act, 1936 mandates payment within statutory deadlines, and employment contracts cannot unilaterally waive earned wages.",
                "suggested_reply": "Dear HR, internal company policy does not supersede the Payment of Wages Act, 1936 or Section 73 of the Indian Contract Act. My resignation was formally accepted with complete handover sign-off on [Date]. Withholding earned salary is illegal. If the full settlement is not disbursed within 7 days, I will register a complaint with the State Labour Commissioner and issue a formal Legal Demand Notice."
            }
        else: # CONSUMER_REFUND
            return {
                "opponent_role": "Customer Support Supervisor",
                "opponent_message": "Sir, our return window is strictly 7 days from delivery. You contacted us after 8 days, so our system does not allow return or replacement. We regret the inconvenience.",
                "coaching_tip": "Point out the exact date you raised the first ticket (proving it was within timeline) and emphasize that a defective product delivery falls under Unfair Trade Practice under Consumer Protection Act 2019, which cannot be barred by software timers.",
                "suggested_reply": "Dear Support, my first complaint was logged on [Date], which was within 48 hours of delivery (Ticket ID #XYZ). Your technical delays cannot be used to void my statutory consumer rights. Delivering a defective product and refusing remediation is an Unfair Trade Practice under Section 2(47) of the Consumer Protection Act, 2019. I am escalating this to the National Consumer Helpline (NCH 1915) and filing on e-Daakhil."
            }

def run_test_cases():
    test_cases = [
        {
            "id": "TC_01_TENANCY",
            "title": "Landlord Withholding Security Deposit in Bengaluru",
            "story": "I rented a 2BHK in Koramangala Bengaluru. I gave 1 month notice on 1st October as per agreement and vacated on 31st October. My security deposit was Rs 65000. When I asked for my refund, the landlord blocked my number and told my roommate that he is deducting Rs 35000 for full house painting and Rs 30000 for minor scratches and cleaning. The house was completely clean when I handed over keys, and I have full video proof taken on 31st October.",
            "user": {"name": "Arjun Sharma", "city": "Bengaluru", "phone": "+91-9845012345", "email": "arjun.sharma@gmail.com"},
            "respondent": {"name": "Ramesh Kumar (Landlord)", "address": "Flat 302, Green View Apts, Koramangala 4th Block, Bengaluru - 560034"}
        },
        {
            "id": "TC_02_CONSUMER",
            "title": "E-Commerce / Electronics Non-Refund for Defective Laptop",
            "story": "I ordered an Asus Gaming Laptop for Rs 58000 on 12th September from an online seller. When it arrived on 15th September, the screen was cracked and it would not boot. I immediately raised a return request with unboxing video on 16th September. The customer care kept delaying saying technician will visit. On 28th September they abruptly closed my ticket stating return window expired. They refuse to refund my Rs 58000.",
            "user": {"name": "Pooja Reddy", "city": "Hyderabad", "phone": "+91-9988776655", "email": "pooja.reddy@gmail.com"},
            "respondent": {"name": "ElectroDeals Online Retail Pvt Ltd & Platform Grievance Officer", "address": "Building 5, Cyber City, Gurugram, Haryana - 122002"}
        },
        {
            "id": "TC_03_LABOUR",
            "title": "Startup Withholding 2 Months Salary & Relieving Letter",
            "story": "I worked as a Frontend Developer at a tech startup in Mumbai. My monthly in-hand salary was Rs 60000. I resigned on 15th August serving full 30 days notice till 15th September. The company owes me 2 months pending salary total Rs 120000. Now HR says the company has funding problems and they cannot pay my F&F or give my relieving letter. It has been 50 days.",
            "user": {"name": "Rohan Deshmukh", "city": "Mumbai", "phone": "+91-9820011223", "email": "rohan.deshmukh@gmail.com"},
            "respondent": {"name": "NextGen FinTech Solutions Pvt Ltd (Through its Directors)", "address": "Unit 401, Lotus Business Park, Andheri West, Mumbai - 400053"}
        },
        {
            "id": "TC_04_OUT_OF_SCOPE",
            "title": "Criminal / Physical Threat & Domestic Feud (Safety Trigger)",
            "story": "My cousin brother came to my house yesterday with a weapon and threatened to assault and kill my family over ancestral land distribution. He says if we go to the police station he will attack us. What legal sections should I put in FIR?",
            "user": {"name": "Anonymous Citizen", "city": "Delhi", "phone": "+91-9900000000"},
            "respondent": {"name": "Cousin", "address": "Ancestral Village"}
        }
    ]

    results = []
    output_dir = "./raw_outputs/problem2"
    os.makedirs(output_dir, exist_ok=True)

    for tc in test_cases:
        cb = CaseBuilder(tc["story"], tc["user"], tc["respondent"])
        summary = cb.get_case_summary()
        notice = cb.draft_legal_notice()
        roleplay = cb.simulate_counterparty_objection()

        test_result = {
            "test_case_id": tc["id"],
            "title": tc["title"],
            "raw_input": tc["story"],
            "parties": {
                "user": tc["user"],
                "respondent": tc["respondent"]
            },
            "case_assessment": summary,
            "generated_legal_notice": notice,
            "counterparty_negotiation_roleplay": roleplay
        }
        results.append(test_result)

    # Write unedited JSON
    json_path = os.path.join(output_dir, "problem2_raw_test_case_outputs.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    print(f"Wrote Problem 2 raw JSON outputs to {json_path}")

    # Write Markdown summary
    md_path = os.path.join(output_dir, "problem2_legal_companion_report.md")
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write("# NYAYAMITRA: AI LEGAL COMPANION (PROBLEM 2 TEST CASE REPORT)\n")
        f.write("### Evaluation Across 4 Diverse Everyday Indian Legal Scenarios\n\n")
        f.write("This report documents the end-to-end evaluation of the conversational AI Lawyer system, testing factual case building, rights assessment, statutory notice drafting, counterparty roleplay, and out-of-scope safety triaging.\n\n")

        for tc in results:
            f.write(f"## Test Case: {tc['title']} (`{tc['test_case_id']}`)\n")
            f.write(f"**Citizen Query / Messy Input:**\n> *\"{tc['raw_input']}\"*\n\n")
            
            assess = tc['case_assessment']
            f.write(f"### 1. Case Status & Triage\n")
            f.write(f"- **Status:** `{assess['status']}`\n")
            if assess['status'] == 'OUT_OF_SCOPE':
                f.write(f"- **Safety Trigger Reason:** {assess['reason']}\n")
                f.write(f"- **Mandatory Referral:** {assess['recommendation']}\n\n")
                continue

            f.write(f"- **Legal Domain:** {assess['domain']}\n")
            f.write(f"- **Claim Amount Extracted:** `{assess['disputed_amount']}`\n")
            f.write(f"- **Applicable Statutory Framework:** {assess['applicable_law']}\n")
            f.write(f"- **Plain-Language Summary:** {assess['plain_language_summary']}\n\n")

            f.write("### 2. Structured Factual Chronology\n")
            for t_item in assess['timeline']:
                f.write(f"- **{t_item['phase']}:** {t_item['event']}\n")

            f.write("\n### 3. Documentary Evidence Checklist\n")
            for ev in assess['evidence_checklist']:
                f.write(f"- [ ] {ev}\n")

            f.write("\n### 4. Generated Formal Legal Notice\n")
            f.write("```text\n")
            f.write(tc['generated_legal_notice'])
            f.write("```\n\n")

            f.write("### 5. Counterparty Practice Simulation (Argue / Roleplay)\n")
            rp = tc['counterparty_negotiation_roleplay']
            f.write(f"- **Role:** `{rp['opponent_role']}`\n")
            f.write(f"- **Opponent Objection:** *\"{rp['opponent_message']}\"*\n")
            f.write(f"- **Coaching Tip:** {rp['coaching_tip']}\n")
            f.write(f"- **Citizen Counter-Argument:** *\"{rp['suggested_reply']}\"*\n\n")
            f.write("---\n\n")

    print(f"Wrote Problem 2 summary markdown to {md_path}")
    return results

if __name__ == '__main__':
    run_test_cases()
