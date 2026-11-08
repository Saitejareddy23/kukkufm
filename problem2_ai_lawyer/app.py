"""
Interactive Web Application for NyayaMitra - AI Legal Companion (Problem 2).
Runs with Python standard library.
"""

import http.server
import socketserver
import json
import os
import sys

# Ensure local imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from ai_lawyer import CaseBuilder

PORT = 8502

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NyayaMitra - AI Legal Companion for Everyday India</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root { --law-navy: #0f1e36; --law-gold: #c59b27; --law-accent: #2e86de; }
        body { background-color: #f4f6f9; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        .hero-banner { background: linear-gradient(135deg, #0f1e36 0%, #1a2a47 100%); color: white; padding: 24px 0; border-bottom: 4px solid var(--law-gold); }
        .disclaimer-banner { background-color: #fff3cd; border-left: 5px solid #ffc107; padding: 10px 15px; font-size: 0.85rem; }
        .tab-content { background: white; border-radius: 0 0 8px 8px; border: 1px solid #dee2e6; border-top: none; padding: 20px; }
        .notice-paper { background: #fffcf5; border: 1px solid #e0dacf; font-family: "Courier New", Courier, monospace; font-size: 0.85rem; padding: 20px; white-space: pre-wrap; max-height: 450px; overflow-y: auto; }
        .chat-bubble-ai { background: #eef2f7; border-radius: 12px 12px 12px 0; padding: 12px 16px; margin-bottom: 12px; }
        .chat-bubble-opponent { background: #ffebee; border-left: 4px solid #d32f2f; border-radius: 4px; padding: 12px; margin-bottom: 10px; }
    </style>
</head>
<body>
    <div class="hero-banner">
        <div class="container">
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <span class="badge bg-warning text-dark mb-1"><i class="fa-solid fa-scale-balanced me-1"></i>NYAYAMITRA AI</span>
                    <h3 class="fw-bold mb-0">Everyday Legal Companion for Citizens in India</h3>
                    <p class="mb-0 text-white-50 small">Empowering citizens against deposit withholding, unpaid salary, and consumer fraud without intimidating legalese.</p>
                </div>
                <div>
                    <a href="/raw_outputs/problem2/problem2_legal_companion_report.md" download class="btn btn-outline-light btn-sm"><i class="fa-solid fa-file-lines me-1"></i>Test Report</a>
                </div>
            </div>
        </div>
    </div>

    <div class="container my-3">
        <div class="disclaimer-banner mb-3 shadow-sm rounded">
            <strong><i class="fa-solid fa-triangle-exclamation text-warning me-1"></i>Citizen Safety Notice:</strong>
            NyayaMitra provides legal information and dispute assistance under the Consumer Protection Act 2019, Model Tenancy principles, and Payment of Wages Act. It is <strong>NOT a substitute for an Advocate</strong>. We strictly refuse criminal, matrimonial, or violent matters and never hallucinate fake laws.
        </div>

        <div class="row">
            <!-- Left Input Column -->
            <div class="col-lg-5">
                <div class="card shadow-sm border-0 mb-3">
                    <div class="card-header bg-white fw-bold"><i class="fa-solid fa-pen-to-square me-2 text-primary"></i>Tell Us What Happened</div>
                    <div class="card-body">
                        <label class="form-label small fw-bold text-muted">Try a Quick Preset or Write Your Own:</label>
                        <div class="d-flex flex-wrap gap-1 mb-2">
                            <button class="btn btn-outline-secondary btn-sm" onclick="loadSample('deposit')">Rent Deposit (₹65k)</button>
                            <button class="btn btn-outline-secondary btn-sm" onclick="loadSample('consumer')">Laptop Refund (₹58k)</button>
                            <button class="btn btn-outline-secondary btn-sm" onclick="loadSample('salary')">Unpaid Salary (₹1.2L)</button>
                            <button class="btn btn-outline-danger btn-sm" onclick="loadSample('threat')">Criminal Threat (Safety Trigger)</button>
                        </div>
                        <textarea id="citizenStory" class="form-control mb-3" rows="7" placeholder="Type your problem in English or Hinglish... e.g. Landlord is not returning my 50000 deposit saying he needs to paint the flat even though flat was clean..."></textarea>
                        
                        <div class="row g-2 mb-3">
                            <div class="col-6">
                                <input type="text" id="userName" class="form-control form-control-sm" placeholder="Your Name" value="Arjun Sharma">
                            </div>
                            <div class="col-6">
                                <input type="text" id="oppName" class="form-control form-control-sm" placeholder="Opposite Party (e.g. Landlord/Company)" value="Ramesh Kumar (Landlord)">
                            </div>
                        </div>

                        <button class="btn btn-primary w-100 fw-bold" onclick="analyzeCase()"><i class="fa-solid fa-wand-magic-sparkles me-2"></i>Analyze My Case & Prepare Notice</button>
                    </div>
                </div>
            </div>

            <!-- Right Output Column -->
            <div class="col-lg-7">
                <div class="card shadow-sm border-0">
                    <ul class="nav nav-tabs bg-light px-3 pt-2" id="legalTabs">
                        <li class="nav-item">
                            <button class="nav-link active" data-bs-toggle="tab" data-bs-target="#tabCase"><i class="fa-solid fa-briefcase me-1"></i>1. Case & Rights</button>
                        </li>
                        <li class="nav-item">
                            <button class="nav-link" data-bs-toggle="tab" data-bs-target="#tabNotice"><i class="fa-solid fa-file-contract me-1"></i>2. Legal Demand Notice</button>
                        </li>
                        <li class="nav-item">
                            <button class="nav-link" data-bs-toggle="tab" data-bs-target="#tabRoleplay"><i class="fa-solid fa-comments me-1"></i>3. Practice Counter-Arguments</button>
                        </li>
                    </ul>

                    <div class="tab-content" id="myTabContent">
                        <!-- Tab 1: Case -->
                        <div class="tab-pane fade show active" id="tabCase">
                            <div id="caseOutput">
                                <p class="text-muted text-center py-5">Enter your story on the left and click "Analyze My Case" to view your statutory rights, evidence checklist, and action steps.</p>
                            </div>
                        </div>

                        <!-- Tab 2: Notice -->
                        <div class="tab-pane fade" id="tabNotice">
                            <div class="d-flex justify-content-between align-items-center mb-2">
                                <span class="small text-muted">Ready-to-dispatch 15-day formal Legal Demand Notice</span>
                                <button class="btn btn-sm btn-outline-primary" onclick="copyNotice()"><i class="fa-solid fa-copy me-1"></i>Copy Notice</button>
                            </div>
                            <div class="notice-paper" id="noticeOutput">Notice will be generated after case analysis.</div>
                        </div>

                        <!-- Tab 3: Roleplay -->
                        <div class="tab-pane fade" id="tabRoleplay">
                            <div id="roleplayOutput">
                                <p class="text-muted text-center py-5">Generate a case to practice negotiating against your counterparty.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        const samples = {
            deposit: "I rented a 2BHK in Koramangala Bengaluru. I gave 1 month notice on 1st October as per agreement and vacated on 31st October. My security deposit was Rs 65000. When I asked for my refund, the landlord blocked my number and told my roommate that he is deducting Rs 35000 for full house painting and Rs 30000 for minor scratches and cleaning. The house was completely clean when I handed over keys, and I have full video proof taken on 31st October.",
            consumer: "I ordered an Asus Gaming Laptop for Rs 58000 on 12th September from an online seller. When it arrived on 15th September, the screen was cracked and it would not boot. I immediately raised a return request with unboxing video on 16th September. The customer care kept delaying saying technician will visit. On 28th September they abruptly closed my ticket stating return window expired. They refuse to refund my Rs 58000.",
            salary: "I worked as a Frontend Developer at a tech startup in Mumbai. My monthly in-hand salary was Rs 60000. I resigned on 15th August serving full 30 days notice till 15th September. The company owes me 2 months pending salary total Rs 120000. Now HR says the company has funding problems and they cannot pay my F&F or give my relieving letter. It has been 50 days.",
            threat: "My cousin brother came to my house yesterday with a weapon and threatened to assault and kill my family over ancestral land distribution. He says if we go to the police station he will attack us. What legal sections should I put in FIR?"
        };

        function loadSample(type) {
            document.getElementById('citizenStory').value = samples[type];
            if (type === 'deposit') {
                document.getElementById('userName').value = 'Arjun Sharma';
                document.getElementById('oppName').value = 'Ramesh Kumar (Landlord)';
            } else if (type === 'consumer') {
                document.getElementById('userName').value = 'Pooja Reddy';
                document.getElementById('oppName').value = 'ElectroDeals Retail Pvt Ltd';
            } else if (type === 'salary') {
                document.getElementById('userName').value = 'Rohan Deshmukh';
                document.getElementById('oppName').value = 'NextGen FinTech Solutions Pvt Ltd';
            } else {
                document.getElementById('userName').value = 'Anonymous Citizen';
                document.getElementById('oppName').value = 'Cousin';
            }
        }

        async function analyzeCase() {
            const story = document.getElementById('citizenStory').value;
            const uName = document.getElementById('userName').value;
            const oName = document.getElementById('oppName').value;

            if (!story.trim()) {
                alert("Please enter your dispute story first.");
                return;
            }

            try {
                const res = await fetch('/api/analyze', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({story: story, user_name: uName, opp_name: oName})
                });
                const data = await res.json();
                renderResults(data);
            } catch (err) {
                console.error("Analysis error:", err);
            }
        }

        function renderResults(data) {
            const caseDiv = document.getElementById('caseOutput');
            const noticeDiv = document.getElementById('noticeOutput');
            const rpDiv = document.getElementById('roleplayOutput');

            if (data.status === 'OUT_OF_SCOPE') {
                caseDiv.innerHTML = `
                    <div class="alert alert-danger">
                        <h5><i class="fa-solid fa-ban me-2"></i>Out of Scope / Immediate Advocate Referral</h5>
                        <p><strong>Safety Reason:</strong> ${data.reason}</p>
                        <p class="mb-0">${data.recommendation}</p>
                    </div>
                `;
                noticeDiv.innerText = "Notice drafting disabled for out-of-scope matters.";
                rpDiv.innerHTML = "<p class='text-danger'>Counterparty roleplay is disabled for criminal/domestic disputes.</p>";
                return;
            }

            const c = data.case_summary;
            let timelineHtml = c.timeline.map(t => `<li><strong>${t.phase}:</strong> ${t.event}</li>`).join('');
            let evidenceHtml = c.evidence_checklist.map(e => `<li><i class="fa-regular fa-square-check text-success me-1"></i>${e}</li>`).join('');
            let provisionsHtml = c.statutory_provisions.map(p => `<li>${p}</li>`).join('');

            caseDiv.innerHTML = `
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <span class="badge bg-primary">${c.domain}</span>
                    <span class="badge bg-success fs-6">Claim: ${c.disputed_amount}</span>
                </div>
                <h6 class="fw-bold text-dark mt-2">Where You Stand (In Plain Language):</h6>
                <p class="small text-muted bg-light p-2 rounded border">${c.plain_language_summary}</p>
                
                <h6 class="fw-bold text-dark mt-3">Applicable Indian Statutes (Zero Hallucination Guarantee):</h6>
                <ul class="small text-muted mb-2">${provisionsHtml}</ul>

                <h6 class="fw-bold text-dark mt-3">Extracted Chronological Timeline:</h6>
                <ul class="small text-muted mb-2">${timelineHtml}</ul>

                <h6 class="fw-bold text-dark mt-3">Evidence Checklist to Gather:</h6>
                <ul class="list-unstyled small text-muted mb-2">${evidenceHtml}</ul>
            `;

            noticeDiv.innerText = data.legal_notice;

            const rp = data.roleplay;
            rpDiv.innerHTML = `
                <div class="alert alert-info py-2 small">
                    <strong><i class="fa-solid fa-chalkboard-user me-1"></i>Negotiation Practice:</strong> Counterparty simulator prepares you for their excuses so you stay calm and firm.
                </div>
                <div class="chat-bubble-opponent">
                    <strong><i class="fa-solid fa-user-xmark me-1"></i>${rp.opponent_role}:</strong>
                    <p class="mb-1 mt-1">"${rp.opponent_message}"</p>
                </div>
                <div class="bg-warning-subtle p-2 rounded small mb-2 border border-warning">
                    <strong><i class="fa-solid fa-lightbulb text-warning me-1"></i>Coaching Tip:</strong> ${rp.coaching_tip}
                </div>
                <div class="chat-bubble-ai border-start border-3 border-primary">
                    <strong><i class="fa-solid fa-shield-halved text-primary me-1"></i>Your Recommended Counter-Argument:</strong>
                    <p class="mb-0 mt-1 small">"${rp.suggested_reply}"</p>
                </div>
            `;
        }

        function copyNotice() {
            const txt = document.getElementById('noticeOutput').innerText;
            navigator.clipboard.writeText(txt);
            alert("Legal Demand Notice copied to clipboard!");
        }
    </script>
</body>
</html>
"""

class LawyerRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_CONTENT.encode('utf-8'))
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/api/analyze':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            req = json.loads(post_data.decode('utf-8'))
            
            story = req.get('story', '')
            u_name = req.get('user_name', 'Aggrieved Citizen')
            o_name = req.get('opp_name', 'Opposite Party')

            user_d = {"name": u_name, "city": "Bengaluru", "phone": "+91-9876543210", "email": "citizen@email.com"}
            opp_d = {"name": o_name, "address": "Registered Address / Office Location", "contact": "contact@oppositeparty.com"}

            cb = CaseBuilder(story, user_d, opp_d)
            summary = cb.get_case_summary()

            if summary["status"] == "OUT_OF_SCOPE":
                resp = {
                    "status": "OUT_OF_SCOPE",
                    "reason": summary["reason"],
                    "recommendation": summary["recommendation"]
                }
            else:
                resp = {
                    "status": "SUCCESS",
                    "case_summary": summary,
                    "legal_notice": cb.draft_legal_notice(),
                    "roleplay": cb.simulate_counterparty_objection()
                }

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(resp).encode('utf-8'))

def run_server(port=PORT):
    with socketserver.TCPServer(("", port), LawyerRequestHandler) as httpd:
        print(f"NyayaMitra AI Lawyer Server running on http://localhost:{port}")
        httpd.serve_forever()

if __name__ == '__main__':
    run_server()
