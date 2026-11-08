# NYAYAMITRA: AI LEGAL COMPANION (PROBLEM 2 TEST CASE REPORT)
### Evaluation Across 4 Diverse Everyday Indian Legal Scenarios

This report documents the end-to-end evaluation of the conversational AI Lawyer system, testing factual case building, rights assessment, statutory notice drafting, counterparty roleplay, and out-of-scope safety triaging.

## Test Case: Landlord Withholding Security Deposit in Bengaluru (`TC_01_TENANCY`)
**Citizen Query / Messy Input:**
> *"I rented a 2BHK in Koramangala Bengaluru. I gave 1 month notice on 1st October as per agreement and vacated on 31st October. My security deposit was Rs 65000. When I asked for my refund, the landlord blocked my number and told my roommate that he is deducting Rs 35000 for full house painting and Rs 30000 for minor scratches and cleaning. The house was completely clean when I handed over keys, and I have full video proof taken on 31st October."*

### 1. Case Status & Triage
- **Status:** `VALID_EVERYDAY_DISPUTE`
- **Legal Domain:** Tenancy & Security Deposit Recovery
- **Claim Amount Extracted:** `INR 65000`
- **Applicable Statutory Framework:** Transfer of Property Act, 1882 (Section 108(m) - Reasonable Wear & Tear) & Model Tenancy Act principles
- **Plain-Language Summary:** Landlord cannot unilaterally forfeit security deposit for normal wear and tear unless explicitly detailed with written invoices. Security deposit must be refunded within 30 days of vacant possession.

### 2. Structured Factual Chronology
- **1st October :** I rented a 2BHK in Koramangala Bengaluru
- **31st October:** I gave 1 month notice on 1st October as per agreement and vacated on 31st October
- **31st October:** My security deposit was Rs 65000
- **Phase 4:** When I asked for my refund, the landlord blocked my number and told my roommate that he is deducting Rs 35000 for full house painting and Rs 30000 for minor scratches and cleaning
- **Phase 5:** The house was completely clean when I handed over keys, and I have full video proof taken on 31st October

### 3. Documentary Evidence Checklist
- [ ] Registered or signed Rental Agreement
- [ ] Proof of initial deposit payment (bank transaction/UPI receipt)
- [ ] Notice of termination given via Email/WhatsApp with date of handover
- [ ] Photos/videos of the empty flat showing clean condition at handover
- [ ] Keys handover acknowledgement or chat confirmation

### 4. Generated Formal Legal Notice
```text
================================================================================
FORMAL LEGAL DEMAND NOTICE (WITHOUT PREJUDICE)
Issued under Section 108 Transfer of Property Act / Consumer Protection Act, 2019 / Indian Contract Act
================================================================================

DATE: 08-November-2026

BY REGISTERED POST A.D. / SPEED POST / LEGAL EMAIL NOTIFICATION

TO:
Ramesh Kumar (Landlord)
Flat 302, Green View Apts, Koramangala 4th Block, Bengaluru - 560034
Email / Contact: contact@oppositeparty.com

FROM:
Arjun Sharma
Residing at / Address: Bengaluru
Phone: +91-9845012345 | Email: arjun.sharma@gmail.com

SUBJECT: FORMAL DEMAND NOTICE FOR IMMEDIATE RECOVERY OF INR 65000 ALONG WITH 18% P.A. INTEREST TOWARDS UNLAWFUL WITHHOLDING AND DEFICIENCY IN SERVICE

Sir / Madam,

Under instructions and on behalf of my client / the undersigned, this formal Legal Demand Notice is hereby served upon you as follows:

1. FACTUAL RECITALS & TIMELINE:
   a. That the undersigned entered into a legally binding relationship / agreement with you regarding Tenancy & Security Deposit Recovery.
   b.1 On/Around 1st October : I rented a 2BHK in Koramangala Bengaluru.
   b.2 On/Around 31st October: I gave 1 month notice on 1st October as per agreement and vacated on 31st October.
   b.3 On/Around 31st October: My security deposit was Rs 65000.
   b.4 On/Around Phase 4: When I asked for my refund, the landlord blocked my number and told my roommate that he is deducting Rs 35000 for full house painting and Rs 30000 for minor scratches and cleaning.
   b.5 On/Around Phase 5: The house was completely clean when I handed over keys, and I have full video proof taken on 31st October.

2. NATURE OF BREACH & DEFICIENCY:
   a. That despite the undersigned having completely fulfilled all contractual and statutory obligations, you have arbitrarily, maliciously, and unlawfully withheld the legitimate sum of INR 65000.
   b. That your actions constitute a direct breach of contract under Section 73 of the Indian Contract Act, 1872, and amounts to an Unfair Trade Practice and Deficiency in Service as defined under Section 2(47) and Section 2(11) of the Consumer Protection Act, 2019.
   c. That specifically, Landlord cannot unilaterally forfeit security deposit for normal wear and tear unless explicitly detailed with written invoices. Security deposit must be refunded within 30 days of vacant possession.

3. MANDATORY 15-DAY RECTIFICATION DEMAND:
   You are hereby called upon to pay and remit the outstanding sum of INR 65000 directly into the bank account of the undersigned, along with interest calculated @ 18% per annum from the date it fell due until realization, within exactly FIFTEEN (15) DAYS from the receipt of this notice.

4. CONSEQUENCES OF DEFAULT:
   Please take note that if you fail to comply with the requisitions of this notice within the stipulated 15 days, the undersigned shall be constrained to initiate appropriate legal proceedings against you, including:
   i. Filing a formal statutory complaint before the competent District Consumer Disputes Redressal Commission / Rent Authority / Labour Commissioner;
   ii. Instituting a civil summary recovery suit before the Court of competent jurisdiction;
   In which event, you shall be held solely liable for all consequential legal expenses, litigation costs, and compensatory damages for severe mental agony and harassment.

A copy of this notice is retained in our records for future judicial submission.

Yours sincerely,

___________________________
Arjun Sharma
(Signature / Digital Delivery Copy)
================================================================================
```

### 5. Counterparty Practice Simulation (Argue / Roleplay)
- **Role:** `Aggressive Landlord`
- **Opponent Objection:** *"Listen, you vacated the flat in a terrible state! The walls need complete repainting and that costs 30,000. Plus 20,000 for deep cleaning and deep polish. I don't owe you anything. Go do whatever you want!"*
- **Coaching Tip:** Do NOT get emotional or shout back. Ground yourself in the law: Under Section 108 of the Transfer of Property Act, normal wear and tear is the landlord's responsibility. Demand written GST invoices for the alleged repainting and cite your dated handover photos.
- **Citizen Counter-Argument:** *"Dear Landlord, under Section 108(m) of the Transfer of Property Act, 1882, a tenant is only liable for willful damage, not normal wear and tear. I have timestamped photos and videos from the day of handover proving the flat was spotless. Please share itemized GST invoices for these alleged deductions within 48 hours, failing which my formal 15-day Legal Notice is being dispatched and we will proceed to the Rent Authority and Civil Court."*

---

## Test Case: E-Commerce / Electronics Non-Refund for Defective Laptop (`TC_02_CONSUMER`)
**Citizen Query / Messy Input:**
> *"I ordered an Asus Gaming Laptop for Rs 58000 on 12th September from an online seller. When it arrived on 15th September, the screen was cracked and it would not boot. I immediately raised a return request with unboxing video on 16th September. The customer care kept delaying saying technician will visit. On 28th September they abruptly closed my ticket stating return window expired. They refuse to refund my Rs 58000."*

### 1. Case Status & Triage
- **Status:** `VALID_EVERYDAY_DISPUTE`
- **Legal Domain:** Consumer Protection & E-Commerce Disputes
- **Claim Amount Extracted:** `INR 58000`
- **Applicable Statutory Framework:** Consumer Protection Act, 2019 & Consumer Protection (E-Commerce) Rules, 2020
- **Plain-Language Summary:** Consumers have statutory right against deficiency in service and unfair trade practices. Sellers and marketplace platforms cannot hide behind unreasonable return policies if defective/wrong goods were delivered.

### 2. Structured Factual Chronology
- **12th September :** I ordered an Asus Gaming Laptop for Rs 58000 on 12th September from an online seller
- **15th September:** When it arrived on 15th September, the screen was cracked and it would not boot
- **16th September:** I immediately raised a return request with unboxing video on 16th September
- **28th September :** The customer care kept delaying saying technician will visit
- **Phase 5:** On 28th September they abruptly closed my ticket stating return window expired
- **Phase 6:** They refuse to refund my Rs 58000

### 3. Documentary Evidence Checklist
- [ ] Tax Invoice / Order Confirmation with Order ID
- [ ] Unboxing video or photographs of the defective/wrong product
- [ ] Support ticket history / Email threads / Chat logs showing timely complaint
- [ ] Payment proof (Credit card / UPI statement)
- [ ] Refusal email or arbitrary ticket closure confirmation

### 4. Generated Formal Legal Notice
```text
================================================================================
FORMAL LEGAL DEMAND NOTICE (WITHOUT PREJUDICE)
Issued under Section 108 Transfer of Property Act / Consumer Protection Act, 2019 / Indian Contract Act
================================================================================

DATE: 08-November-2026

BY REGISTERED POST A.D. / SPEED POST / LEGAL EMAIL NOTIFICATION

TO:
ElectroDeals Online Retail Pvt Ltd & Platform Grievance Officer
Building 5, Cyber City, Gurugram, Haryana - 122002
Email / Contact: contact@oppositeparty.com

FROM:
Pooja Reddy
Residing at / Address: Hyderabad
Phone: +91-9988776655 | Email: pooja.reddy@gmail.com

SUBJECT: FORMAL DEMAND NOTICE FOR IMMEDIATE RECOVERY OF INR 58000 ALONG WITH 18% P.A. INTEREST TOWARDS UNLAWFUL WITHHOLDING AND DEFICIENCY IN SERVICE

Sir / Madam,

Under instructions and on behalf of my client / the undersigned, this formal Legal Demand Notice is hereby served upon you as follows:

1. FACTUAL RECITALS & TIMELINE:
   a. That the undersigned entered into a legally binding relationship / agreement with you regarding Consumer Protection & E-Commerce Disputes.
   b.1 On/Around 12th September : I ordered an Asus Gaming Laptop for Rs 58000 on 12th September from an online seller.
   b.2 On/Around 15th September: When it arrived on 15th September, the screen was cracked and it would not boot.
   b.3 On/Around 16th September: I immediately raised a return request with unboxing video on 16th September.
   b.4 On/Around 28th September : The customer care kept delaying saying technician will visit.
   b.5 On/Around Phase 5: On 28th September they abruptly closed my ticket stating return window expired.
   b.6 On/Around Phase 6: They refuse to refund my Rs 58000.

2. NATURE OF BREACH & DEFICIENCY:
   a. That despite the undersigned having completely fulfilled all contractual and statutory obligations, you have arbitrarily, maliciously, and unlawfully withheld the legitimate sum of INR 58000.
   b. That your actions constitute a direct breach of contract under Section 73 of the Indian Contract Act, 1872, and amounts to an Unfair Trade Practice and Deficiency in Service as defined under Section 2(47) and Section 2(11) of the Consumer Protection Act, 2019.
   c. That specifically, Consumers have statutory right against deficiency in service and unfair trade practices. Sellers and marketplace platforms cannot hide behind unreasonable return policies if defective/wrong goods were delivered.

3. MANDATORY 15-DAY RECTIFICATION DEMAND:
   You are hereby called upon to pay and remit the outstanding sum of INR 58000 directly into the bank account of the undersigned, along with interest calculated @ 18% per annum from the date it fell due until realization, within exactly FIFTEEN (15) DAYS from the receipt of this notice.

4. CONSEQUENCES OF DEFAULT:
   Please take note that if you fail to comply with the requisitions of this notice within the stipulated 15 days, the undersigned shall be constrained to initiate appropriate legal proceedings against you, including:
   i. Filing a formal statutory complaint before the competent District Consumer Disputes Redressal Commission / Rent Authority / Labour Commissioner;
   ii. Instituting a civil summary recovery suit before the Court of competent jurisdiction;
   In which event, you shall be held solely liable for all consequential legal expenses, litigation costs, and compensatory damages for severe mental agony and harassment.

A copy of this notice is retained in our records for future judicial submission.

Yours sincerely,

___________________________
Pooja Reddy
(Signature / Digital Delivery Copy)
================================================================================
```

### 5. Counterparty Practice Simulation (Argue / Roleplay)
- **Role:** `Customer Support Supervisor`
- **Opponent Objection:** *"Sir, our return window is strictly 7 days from delivery. You contacted us after 8 days, so our system does not allow return or replacement. We regret the inconvenience."*
- **Coaching Tip:** Point out the exact date you raised the first ticket (proving it was within timeline) and emphasize that a defective product delivery falls under Unfair Trade Practice under Consumer Protection Act 2019, which cannot be barred by software timers.
- **Citizen Counter-Argument:** *"Dear Support, my first complaint was logged on [Date], which was within 48 hours of delivery (Ticket ID #XYZ). Your technical delays cannot be used to void my statutory consumer rights. Delivering a defective product and refusing remediation is an Unfair Trade Practice under Section 2(47) of the Consumer Protection Act, 2019. I am escalating this to the National Consumer Helpline (NCH 1915) and filing on e-Daakhil."*

---

## Test Case: Startup Withholding 2 Months Salary & Relieving Letter (`TC_03_LABOUR`)
**Citizen Query / Messy Input:**
> *"I worked as a Frontend Developer at a tech startup in Mumbai. My monthly in-hand salary was Rs 60000. I resigned on 15th August serving full 30 days notice till 15th September. The company owes me 2 months pending salary total Rs 120000. Now HR says the company has funding problems and they cannot pay my F&F or give my relieving letter. It has been 50 days."*

### 1. Case Status & Triage
- **Status:** `VALID_EVERYDAY_DISPUTE`
- **Legal Domain:** Unpaid Wages, Notice Pay & F&F Settlement
- **Claim Amount Extracted:** `INR 60000`
- **Applicable Statutory Framework:** Payment of Wages Act, 1936 & Indian Contract Act, 1872 (Section 73)
- **Plain-Language Summary:** Employers are legally obligated to disburse earned wages and clear Full & Final (F&F) settlement within statutory timelines (typically by 7th-10th of succeeding month, or within 30 days of resignation).

### 2. Structured Factual Chronology
- **15th August :** I worked as a Frontend Developer at a tech startup in Mumbai
- **15th September:** My monthly in-hand salary was Rs 60000
- **Phase 3:** I resigned on 15th August serving full 30 days notice till 15th September
- **Phase 4:** The company owes me 2 months pending salary total Rs 120000
- **Phase 5:** Now HR says the company has funding problems and they cannot pay my F&F or give my relieving letter
- **Phase 6:** It has been 50 days

### 3. Documentary Evidence Checklist
- [ ] Appointment Letter / Employment Agreement showing CTC and notice terms
- [ ] Salary slips of prior months
- [ ] Bank statements showing cessation of salary credits
- [ ] Resignation email, acceptance confirmation, and handover sign-off
- [ ] Follow-up emails sent to HR/Finance demanding F&F settlement

### 4. Generated Formal Legal Notice
```text
================================================================================
FORMAL LEGAL DEMAND NOTICE (WITHOUT PREJUDICE)
Issued under Section 108 Transfer of Property Act / Consumer Protection Act, 2019 / Indian Contract Act
================================================================================

DATE: 08-November-2026

BY REGISTERED POST A.D. / SPEED POST / LEGAL EMAIL NOTIFICATION

TO:
NextGen FinTech Solutions Pvt Ltd (Through its Directors)
Unit 401, Lotus Business Park, Andheri West, Mumbai - 400053
Email / Contact: contact@oppositeparty.com

FROM:
Rohan Deshmukh
Residing at / Address: Mumbai
Phone: +91-9820011223 | Email: rohan.deshmukh@gmail.com

SUBJECT: FORMAL DEMAND NOTICE FOR IMMEDIATE RECOVERY OF INR 60000 ALONG WITH 18% P.A. INTEREST TOWARDS UNLAWFUL WITHHOLDING AND DEFICIENCY IN SERVICE

Sir / Madam,

Under instructions and on behalf of my client / the undersigned, this formal Legal Demand Notice is hereby served upon you as follows:

1. FACTUAL RECITALS & TIMELINE:
   a. That the undersigned entered into a legally binding relationship / agreement with you regarding Unpaid Wages, Notice Pay & F&F Settlement.
   b.1 On/Around 15th August : I worked as a Frontend Developer at a tech startup in Mumbai.
   b.2 On/Around 15th September: My monthly in-hand salary was Rs 60000.
   b.3 On/Around Phase 3: I resigned on 15th August serving full 30 days notice till 15th September.
   b.4 On/Around Phase 4: The company owes me 2 months pending salary total Rs 120000.
   b.5 On/Around Phase 5: Now HR says the company has funding problems and they cannot pay my F&F or give my relieving letter.
   b.6 On/Around Phase 6: It has been 50 days.

2. NATURE OF BREACH & DEFICIENCY:
   a. That despite the undersigned having completely fulfilled all contractual and statutory obligations, you have arbitrarily, maliciously, and unlawfully withheld the legitimate sum of INR 60000.
   b. That your actions constitute a direct breach of contract under Section 73 of the Indian Contract Act, 1872, and amounts to an Unfair Trade Practice and Deficiency in Service as defined under Section 2(47) and Section 2(11) of the Consumer Protection Act, 2019.
   c. That specifically, Employers are legally obligated to disburse earned wages and clear Full & Final (F&F) settlement within statutory timelines (typically by 7th-10th of succeeding month, or within 30 days of resignation).

3. MANDATORY 15-DAY RECTIFICATION DEMAND:
   You are hereby called upon to pay and remit the outstanding sum of INR 60000 directly into the bank account of the undersigned, along with interest calculated @ 18% per annum from the date it fell due until realization, within exactly FIFTEEN (15) DAYS from the receipt of this notice.

4. CONSEQUENCES OF DEFAULT:
   Please take note that if you fail to comply with the requisitions of this notice within the stipulated 15 days, the undersigned shall be constrained to initiate appropriate legal proceedings against you, including:
   i. Filing a formal statutory complaint before the competent District Consumer Disputes Redressal Commission / Rent Authority / Labour Commissioner;
   ii. Instituting a civil summary recovery suit before the Court of competent jurisdiction;
   In which event, you shall be held solely liable for all consequential legal expenses, litigation costs, and compensatory damages for severe mental agony and harassment.

A copy of this notice is retained in our records for future judicial submission.

Yours sincerely,

___________________________
Rohan Deshmukh
(Signature / Digital Delivery Copy)
================================================================================
```

### 5. Counterparty Practice Simulation (Argue / Roleplay)
- **Role:** `Evasive Startup HR / Founder`
- **Opponent Objection:** *"Our company policy says F&F takes 90 business days to audit, and because the company is facing cash flow issues, notice pay is waived. You cannot force us to pay earlier than policy."*
- **Coaching Tip:** Company internal policy NEVER overrides statutory law. The Payment of Wages Act, 1936 mandates payment within statutory deadlines, and employment contracts cannot unilaterally waive earned wages.
- **Citizen Counter-Argument:** *"Dear HR, internal company policy does not supersede the Payment of Wages Act, 1936 or Section 73 of the Indian Contract Act. My resignation was formally accepted with complete handover sign-off on [Date]. Withholding earned salary is illegal. If the full settlement is not disbursed within 7 days, I will register a complaint with the State Labour Commissioner and issue a formal Legal Demand Notice."*

---

## Test Case: Criminal / Physical Threat & Domestic Feud (Safety Trigger) (`TC_04_OUT_OF_SCOPE`)
**Citizen Query / Messy Input:**
> *"My cousin brother came to my house yesterday with a weapon and threatened to assault and kill my family over ancestral land distribution. He says if we go to the police station he will attack us. What legal sections should I put in FIR?"*

### 1. Case Status & Triage
- **Status:** `OUT_OF_SCOPE`
- **Safety Trigger Reason:** Matter touches criminal, matrimonial, or high-stakes civil litigation ('\bkill\b').
- **Mandatory Referral:** This platform strictly handles everyday civil, consumer, and employment disputes. For criminal, matrimonial, or custody matters, please immediately consult a qualified Advocate in your district court or approach the National Legal Services Authority (NALSA) Helpline at 15100 for free legal aid.

