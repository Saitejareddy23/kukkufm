"""
Generates the exact 2-Page Executive Solution Document for Problem 2.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from shared_utils.pdf_generator import DocumentBuilder

def generate_pdf():
    doc = DocumentBuilder()
    
    # ------------------ PAGE 1 ------------------
    doc.draw_header_banner(
        problem_title="PROBLEM 2: NYAYAMITRA - AI CITIZEN LEGAL COMPANION",
        subtitle="Conversational Case Building, Plain-Language Rights, Notice Drafting & Hallucination Prevention",
        student_name="Candidate (AI Generalist)",
        roll_no="ES23BTECH11021",
        branch="AI & Data Engineering"
    )
    
    y = 745
    
    # Section 1: Problem Choice, Scope & Framing
    y = doc.draw_section_header("1. Problem Choice, Framing & Strict Scope Boundaries", y)
    y = doc.draw_paragraph(
        "In India, over 90% of everyday legal grievances - withheld tenant deposits (INR 20k-1.5L), unpaid startup salaries/F&F, and refused e-commerce refunds - never reach an advocate. The process is intimidating, lawyers charge INR 3,000-15,000 just for an initial notice, and citizens simply give up. NyayaMitra is built to bridge this 'justice gap' for everyday disputes by converting messy stories into structured claims, plain-language options, and formal 15-day legal notices.",
        42, y, 510, font="F1", size=8.0, line_height=10.0
    )
    y -= 3
    
    # Scope Matrix Card
    doc.draw_card(
        "What NyayaMitra Covers (High-Frequency Everyday Injustices)",
        [
            "- Tenancy & Security Deposits: Withholding without damage proof (Transfer of Property Act Sec 108(m))",
            "- Consumer Protection: E-commerce refunds, defective electronics, ticket cancellations (CPA 2019)",
            "- Employment Dues: Unpaid salary, notice pay, withheld F&F settlement (Payment of Wages Act 1936)"
        ],
        42, y, 250, 48, bg=(0.95, 0.98, 0.95), border=(0.75, 0.88, 0.75)
    )
    doc.draw_card(
        "Strict Non-Scope & Mandatory Advocate Referral",
        [
            "- Criminal offenses: BNS / IPC, assault, domestic violence, bail, police FIRs, NDPS",
            "- Matrimonial & Family: Contested divorce, child custody, maintenance",
            "- Complex Property: Ancestral land partition, revenue title disputes -> Redirects to NALSA (15100)"
        ],
        302, y, 250, 48, bg=(1.0, 0.96, 0.96), border=(0.92, 0.80, 0.80)
    )
    y -= 56

    # Section 2: Technical Architecture & Hallucination Defense
    y = doc.draw_section_header("2. System Architecture & Anti-Hallucination Ground-Truth Engine", y)
    y = doc.draw_paragraph(
        "The single greatest risk in legal AI is hallucination: models confidently inventing fictitious sections (e.g. 'Section 420A of Consumer Protection Act') or fake Supreme Court precedents. NyayaMitra enforces a zero-hallucination constraint via a hybrid architecture:",
        42, y, 510, font="F1", size=8.0, line_height=10.0
    )
    y -= 3
    
    doc.draw_card(
        "Layer 1: Scope & Safety Classifier",
        [
            "- Real-time regex & keyword safety barrier",
            "- Scans for criminal/violence triggers",
            "- Halts prompt if out-of-scope; dispatches",
            "  formal advocate/NALSA helpline referral"
        ],
        42, y, 165, 52, bg=(0.96, 0.97, 1.0), border=(0.82, 0.86, 0.94)
    )
    doc.draw_card(
        "Layer 2: Curated Statutory KB (Anchor)",
        [
            "- Restricted knowledge base of verified statutes",
            "- TPA 1882, CPA 2019, Payment of Wages 1936",
            "- NO open-ended legal generation by LLM",
            "- Fallback disclaimer if no verified rule exists"
        ],
        215, y, 165, 52, bg=(0.96, 0.97, 1.0), border=(0.82, 0.86, 0.94)
    )
    doc.draw_card(
        "Layer 3: Template Notice & Roleplay",
        [
            "- Programmatic Indian legal notice generator",
            "- Standard 15-day cure clause & forum warnings",
            "- Interactive Counterparty negotiation simulator",
            "- Empowers citizen with calm, firm replies"
        ],
        388, y, 165, 52, bg=(0.96, 0.97, 1.0), border=(0.82, 0.86, 0.94)
    )
    y -= 60

    # Section 3: Test Case Evaluations (Raw Run Summaries)
    y = doc.draw_section_header("3. Evaluation on Realistic Indian Test Cases", y)
    y = doc.draw_paragraph(
        "We tested the system across four representative scenarios to validate fact extraction, timeline generation, statutory citations, and out-of-scope safety triaging:",
        42, y, 510, font="F1", size=8.0, line_height=9.5
    )
    y -= 2

    table_headers = ["Case ID", "Scenario", "Claim", "Statutory Framework Applied", "Outcome & Artifacts"]
    table_rows = [
        ["TC_01", "Tenant Deposit (Bengaluru)", "INR 65,000", "TPA 1882 Sec 108(m) (Wear & Tear)", "Generated 15-Day Demand Notice & Roleplay"],
        ["TC_02", "Defective Laptop / E-Commerce", "INR 58,000", "CPA 2019 Sec 2(47) (Unfair Trade Practice)", "Generated Notice + e-Daakhil filing guidance"],
        ["TC_03", "Unpaid Startup Wages (Mumbai)", "INR 1,20,000", "Payment of Wages Act 1936 / Sec 73 Contract", "Drafted Employer Demand + Labour Comm. steps"],
        ["TC_04", "Armed Family Threat & Land Feud", "N/A", "Criminal / Land Title Trigger Activated", "Strictly refused advice; NALSA 15100 referral"]
    ]
    y = doc.draw_table(42, y, [36, 125, 60, 160, 129], table_headers, table_rows)
    
    doc.draw_footer(1, 2)
    
    # ------------------ PAGE 2 ------------------
    doc.new_page()
    doc.draw_header_banner(
        problem_title="PROBLEM 2: CITIZEN EMPOWERMENT, ECONOMICS & QUALITY CHECKS",
        subtitle="Roleplay Argument Simulator, Real-World Scaling, Failure Boundaries & AI Audit",
        student_name="Candidate (AI Generalist)",
        roll_no="ES23BTECH11021",
        branch="AI & Data Engineering"
    )
    
    y = 745
    
    # Section 4: Helping Citizens Argue (Counterparty Simulation)
    y = doc.draw_section_header("4. Helping the Citizen Argue: Counterparty Negotiation Practice", y)
    y = doc.draw_paragraph(
        "Drafting a notice is only half the battle; ordinary people crumble when an aggressive landlord or corporate HR intimidates them on WhatsApp. NyayaMitra includes an interactive negotiation simulator that roleplays common excuses and coaches the user to respond firmly:",
        42, y, 510, font="F1", size=8.0, line_height=10.0
    )
    y -= 3
    
    y = doc.draw_bullet_point(
        "Landlord Excuse ('I had to repaint the whole house for Rs 30,000')",
        "Coaching: Do not shout. Cite Section 108 of Transfer of Property Act (tenant not liable for normal wear/tear) and demand itemized GST invoices and handover photos within 48h.",
        42, y, 510, size=7.5, line_height=9.5
    )
    y = doc.draw_bullet_point(
        "HR Excuse ('Internal policy says F&F takes 90 days and notice pay is waived')",
        "Coaching: Remind them company policy does not supersede the Payment of Wages Act 1936 or Indian Contract Act. State that non-payment triggers a complaint to the Labour Commissioner.",
        42, y, 510, size=7.5, line_height=9.5
    )
    y = doc.draw_bullet_point(
        "E-Commerce Support ('7-day app return window has expired')",
        "Coaching: Reference the initial support ticket date raised within 48h. Emphasize that technical app delays do not extinguish statutory rights against Unfair Trade Practices under CPA 2019.",
        42, y, 510, size=7.5, line_height=9.5
    )
    y -= 6

    # Section 5: Real-World Economics, Human-in-the-Loop & Scale
    y = doc.draw_section_header("5. Production Economics, Human-in-the-Loop & Scalability", y)
    
    doc.draw_card(
        "What We Kept as Code vs. AI",
        [
            "- Code: Verified Statutory Knowledge Base, timeline regex parser, demand notice templates, safety filter",
            "- AI: Multilingual conversational intake (English, Hindi, Hinglish), tone conversion, argument roleplay",
            "- Why: The legal provisions MUST be deterministic; natural conversation MUST be adaptable"
        ],
        42, y, 250, 48, bg=(0.98, 0.98, 0.99), border=(0.85, 0.88, 0.92)
    )
    
    doc.draw_card(
        "Human-in-the-Loop & Cost Scaling",
        [
            "- Citizen in the Loop: User reviews, verifies extracted dates and sums, and signs the notice",
            "- Advocate Referral: Seamless 1-click export of structured case brief to partner legal aid advocates",
            "- Economics: <$0.01 API cost per intake (100x cheaper than INR 5,000 standard advocate notice fee)"
        ],
        302, y, 250, 48, bg=(0.98, 0.98, 0.99), border=(0.85, 0.88, 0.92)
    )
    y -= 56

    # Section 6: Quality Checking - Where Does NyayaMitra Fail?
    y = doc.draw_section_header("6. Honest Quality Check: Where Does NyayaMitra Fail?", y)
    y = doc.draw_paragraph(
        "Every AI system has limits. Transparently documenting failure modes prevents harm to citizens:",
        42, y, 510, font="F1", size=8.0, line_height=10.0
    )
    y -= 3
    
    y = doc.draw_bullet_point(
        "1. Nuanced Local Municipal Tenancy Laws",
        "Rent laws vary by state (e.g. Maharashtra Rent Control Act vs. Karnataka vs. Delhi). While Model Tenancy Act principles and TPA apply generally, hyper-local statutory variations require human lawyer verification.",
        42, y, 510, size=7.5, line_height=9.5
    )
    y = doc.draw_bullet_point(
        "2. Counterparty Hostile Reply Analysis",
        "If the counterparty hires a seasoned litigator who replies with complex jurisdictional objections or counter-claims (e.g. alleging extortion or property damage), the AI cannot litigate in court and must pass the file to a lawyer.",
        42, y, 510, size=7.5, line_height=9.5
    )
    y = doc.draw_bullet_point(
        "3. Evidentiary Weight Assessment",
        "The AI can verify if a document exists (e.g. a WhatsApp screenshot), but cannot independently verify if the screenshot is legally admissible under Section 65B of the Indian Evidence Act (BSA 2023).",
        42, y, 510, size=7.5, line_height=9.5
    )
    y -= 6

    # Section 7: AI Tools Used & One Place They Got It Wrong
    y = doc.draw_section_header("7. AI Tools Used & One Place They Got It Wrong", y)
    y = doc.draw_paragraph(
        "Tools Used: ChatGPT-4o and Gemini 1.5 Flash were evaluated during conversational prototype testing for extracting dates and drafting notices.",
        42, y, 510, font="F1", size=8.0, line_height=9.5
    )
    y -= 2
    y = doc.draw_paragraph(
        "Where AI Got It Wrong: When asked to draft a tenancy notice, raw GPT-4o confidently cited 'Section 13 of the Indian Tenancy Act, 1988' - a completely fictional statute (there is no central Indian Tenancy Act; tenancy is governed by State Rent Acts and Transfer of Property Act 1882). It also fabricated a citation 'Ramesh Kumar v. State of Karnataka 2019'. This critical failure proved that pure LLMs CANNOT be trusted with open-ended statutory citation. We solved this by locking the system to a Curated Verified Statutory Knowledge Base.",
        42, y, 510, font="F3", size=7.5, line_height=9.5, color=(0.2, 0.2, 0.2)
    )
    
    doc.draw_footer(2, 2)
    
    output_pdf = os.path.join(os.path.dirname(__file__), '..', 'solution_docs', 'Problem2_Solution_Doc.pdf')
    doc.save(output_pdf)
    return output_pdf

if __name__ == '__main__':
    generate_pdf()
