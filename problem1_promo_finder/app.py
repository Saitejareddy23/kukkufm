"""
Interactive Web Application for Kuku Microdrama Promo Miner.
Runs with standard library (no external dependencies needed) or can be deployed to HuggingFace / Vercel / Streamlit.
"""

import http.server
import socketserver
import json
import os
import sys

PORT = 8501

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kuku TV - Microdrama Promo Miner</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root { --brand-primary: #ff4757; --brand-dark: #1e272e; --brand-light: #f1f2f6; }
        body { background-color: #f8f9fa; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        .hero-banner { background: linear-gradient(135deg, #1e272e 0%, #2f3542 100%); color: white; padding: 28px 0; margin-bottom: 25px; border-bottom: 4px solid #ff4757; }
        .promo-card { transition: transform 0.15s ease, box-shadow 0.15s ease; border-radius: 12px; border: 1px solid #e1e2e6; overflow: hidden; margin-bottom: 16px; }
        .promo-card:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(0,0,0,0.08); }
        .score-badge { font-size: 1.1rem; font-weight: 700; background: #ff4757; color: white; padding: 6px 12px; border-radius: 20px; }
        .phone-mockup { width: 280px; height: 500px; border: 8px solid #2f3542; border-radius: 36px; background: #000; color: #fff; padding: 15px; position: relative; box-shadow: 0 15px 35px rgba(0,0,0,0.3); }
        .tag-pill { font-size: 0.75rem; font-weight: 600; padding: 3px 8px; border-radius: 12px; }
    </style>
</head>
<body>
    <div class="hero-banner">
        <div class="container">
            <div class="row align-items-center">
                <div class="col-md-8">
                    <span class="badge bg-danger mb-2">KUKU AI GENERALIST ASSIGNMENT</span>
                    <h2 class="fw-bold mb-1"><i class="fa-solid fa-film text-danger me-2"></i>Microdrama Promo Miner & Ranker</h2>
                    <p class="mb-0 text-white-50">Automated 20–60s Viral Hook & Cliffhanger Discovery across 50 Episodes of <i>'I Married a Broken Soldier. He was a Duke'</i></p>
                </div>
                <div class="col-md-4 text-md-end mt-3 mt-md-0">
                    <button class="btn btn-outline-light btn-sm me-2" onclick="filterType('ALL')"><i class="fa-solid fa-arrows-rotate me-1"></i>Reset</button>
                    <a href="/raw_outputs/problem1/problem1_all_promos_raw.json" download class="btn btn-danger btn-sm"><i class="fa-solid fa-download me-1"></i>Raw JSON</a>
                </div>
            </div>
        </div>
    </div>

    <div class="container">
        <!-- Control Bar -->
        <div class="card p-3 mb-4 shadow-sm border-0">
            <div class="row g-2 align-items-center">
                <div class="col-md-3">
                    <label class="form-label small fw-bold text-muted mb-1">Filter by Hook Category</label>
                    <select id="categoryFilter" class="form-select form-select-sm" onchange="applyFilters()">
                        <option value="ALL">All Hook Categories</option>
                        <option value="Physical">Physical Shock / Confrontation</option>
                        <option value="Humiliation">Verbal Humiliation / Betrayal</option>
                        <option value="Identity">Shock Identity / Power Reveal</option>
                    </select>
                </div>
                <div class="col-md-3">
                    <label class="form-label small fw-bold text-muted mb-1">Max Duration</label>
                    <select id="durationFilter" class="form-select form-select-sm" onchange="applyFilters()">
                        <option value="60">All Durations (20s - 60s)</option>
                        <option value="35">Short & Punchy (&le; 35s)</option>
                        <option value="50">Sweet Spot (35s - 50s)</option>
                    </select>
                </div>
                <div class="col-md-3">
                    <label class="form-label small fw-bold text-muted mb-1">Sort By</label>
                    <select id="sortFilter" class="form-select form-select-sm" onchange="applyFilters()">
                        <option value="score">Composite Promo Score (High to Low)</option>
                        <option value="duration_asc">Duration (Shortest First)</option>
                        <option value="duration_desc">Duration (Longest First)</option>
                        <option value="episode">Episode Number</option>
                    </select>
                </div>
                <div class="col-md-3 text-end pt-3">
                    <span class="text-muted small">Showing: <strong id="promoCount" class="text-danger">0</strong> promos</span>
                </div>
            </div>
        </div>

        <!-- Promos Grid -->
        <div class="row" id="promosContainer">
            <!-- Dynamically populated via JS -->
        </div>
    </div>

    <!-- Modal Detail View -->
    <div class="modal fade" id="promoModal" tabindex="-1">
        <div class="modal-dialog modal-lg modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header bg-dark text-white">
                    <h5 class="modal-title" id="modalTitle">Promo Details</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body" id="modalBody">
                    <!-- Populated via JS -->
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        let allPromos = [];

        async function loadData() {
            try {
                const res = await fetch('/api/promos');
                const data = await res.json();
                allPromos = data.top_ranked_promos;
                applyFilters();
            } catch (err) {
                console.error("Failed loading promos:", err);
            }
        }

        function applyFilters() {
            const cat = document.getElementById('categoryFilter').value;
            const maxDur = parseFloat(document.getElementById('durationFilter').value);
            const sortBy = document.getElementById('sortFilter').value;

            let filtered = allPromos.filter(p => {
                if (cat !== 'ALL' && !p.hook_type.includes(cat)) return false;
                if (p.total_duration > maxDur) return false;
                return true;
            });

            if (sortBy === 'score') filtered.sort((a,b) => b.score - a.score);
            else if (sortBy === 'duration_asc') filtered.sort((a,b) => a.total_duration - b.total_duration);
            else if (sortBy === 'duration_desc') filtered.sort((a,b) => b.total_duration - a.total_duration);
            else if (sortBy === 'episode') filtered.sort((a,b) => a.episode_num - b.episode_num);

            renderPromos(filtered);
        }

        function renderPromos(promos) {
            const container = document.getElementById('promosContainer');
            document.getElementById('promoCount').innerText = promos.length;
            container.innerHTML = '';

            if (promos.length === 0) {
                container.innerHTML = '<div class="col-12 text-center py-5 text-muted">No promos match your filter criteria.</div>';
                return;
            }

            promos.forEach((p, idx) => {
                const seg = p.segments[0];
                const card = document.createElement('div');
                card.className = 'col-lg-6';
                card.innerHTML = `
                    <div class="card promo-card bg-white p-3">
                        <div class="d-flex justify-content-between align-items-start mb-2">
                            <div>
                                <span class="badge bg-dark me-1">Rank #${idx + 1}</span>
                                <span class="badge bg-secondary me-1">Episode ${p.episode_num}</span>
                                <span class="badge bg-light text-dark border"><i class="fa-regular fa-clock me-1"></i>${seg.start_time} - ${seg.end_time} (${p.total_duration}s)</span>
                            </div>
                            <span class="score-badge shadow-sm">${p.score}</span>
                        </div>
                        <div class="mb-2">
                            <span class="badge bg-danger-subtle text-danger tag-pill me-1"><i class="fa-solid fa-bolt me-1"></i>${p.hook_type}</span>
                            <span class="badge bg-warning-subtle text-dark tag-pill"><i class="fa-solid fa-question me-1"></i>${p.cliffhanger_type}</span>
                        </div>
                        <div class="p-2 rounded bg-light border-start border-3 border-danger mb-2 small">
                            <strong><i class="fa-solid fa-play text-danger me-1"></i>Hook:</strong> ${p.hook_description}
                        </div>
                        <div class="p-2 rounded bg-light border-start border-3 border-warning mb-2 small">
                            <strong><i class="fa-solid fa-circle-pause text-warning me-1"></i>Cliffhanger:</strong> ${p.cliffhanger_description}
                        </div>
                        <p class="text-muted small mb-2"><em>"${p.why_it_works}"</em></p>
                        <div class="d-flex justify-content-between align-items-center pt-2 border-top">
                            <span class="small text-muted"><i class="fa-solid fa-chart-line text-success me-1"></i>Clarity: ${p.clarity_score}</span>
                            <button class="btn btn-outline-danger btn-sm" onclick='viewDetails(${JSON.stringify(p).replace(/'/g, "&apos;")})'>
                                <i class="fa-solid fa-mobile-screen me-1"></i>View Ad Cut
                            </button>
                        </div>
                    </div>
                `;
                container.appendChild(card);
            });
        }

        function viewDetails(promo) {
            const seg = promo.segments[0];
            document.getElementById('modalTitle').innerHTML = `Episode ${promo.episode_num} Ad Candidate (Score: ${promo.score})`;
            document.getElementById('modalBody').innerHTML = `
                <div class="row">
                    <div class="col-md-5 text-center">
                        <div class="phone-mockup mx-auto">
                            <div class="small text-danger fw-bold mb-2">TIKTOK / REELS PREVIEW</div>
                            <div class="bg-dark rounded p-2 text-start small text-white-50" style="height: 380px; overflow-y: auto;">
                                <div class="text-danger fw-bold">[00:00 - 00:03] HOOK</div>
                                <div class="text-white mb-3">${promo.hook_description}</div>
                                <div class="text-warning fw-bold">[00:03 - ${promo.total_duration - 3}s] TENSION ESCALATION</div>
                                <div class="text-white-50 mb-3">Conflict builds between protagonist and antagonist...</div>
                                <div class="text-danger fw-bold">[CUT TO BLACK] CLIFFHANGER</div>
                                <div class="text-white">${promo.cliffhanger_description}</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-7">
                        <h6 class="fw-bold text-danger">Ad Cut Breakdown</h6>
                        <table class="table table-sm small">
                            <tr><th>Episode</th><td>${promo.episode_num}</td></tr>
                            <tr><th>Start Timestamp</th><td><code>${seg.start_time}</code></td></tr>
                            <tr><th>End Timestamp</th><td><code>${seg.end_time}</code></td></tr>
                            <tr><th>Clip Duration</th><td><strong>${promo.total_duration} seconds</strong></td></tr>
                            <tr><th>Hook Type</th><td><span class="badge bg-danger">${promo.hook_type}</span></td></tr>
                            <tr><th>Cliffhanger Type</th><td><span class="badge bg-warning text-dark">${promo.cliffhanger_type}</span></td></tr>
                            <tr><th>Algorithmic Score</th><td><span class="badge bg-success">${promo.score}</span></td></tr>
                        </table>
                        <h6 class="fw-bold mt-3">Why This Converts:</h6>
                        <p class="small text-muted">${promo.why_it_works}</p>
                        <h6 class="fw-bold mt-2">Recommended Campaign Phase:</h6>
                        <p class="small text-muted">Direct Top-of-Funnel User Acquisition (TikTok / Instagram Reels ad formats). No editing needed; cut directly at timestamps.</p>
                    </div>
                </div>
            `;
            new bootstrap.Modal(document.getElementById('promoModal')).show();
        }

        window.onload = loadData;
    </script>
</body>
</html>
"""

class PromoRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_CONTENT.encode('utf-8'))
        elif self.path == '/api/promos':
            json_file = os.path.join(os.path.dirname(__file__), '..', 'raw_outputs', 'problem1', 'problem1_all_promos_raw.json')
            if os.path.exists(json_file):
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                with open(json_file, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
        else:
            super().do_GET()

def run_server(port=PORT):
    with socketserver.TCPServer(("", port), PromoRequestHandler) as httpd:
        print(f"Kuku Promo Miner Server running on http://localhost:{port}")
        httpd.serve_forever()

if __name__ == '__main__':
    run_server()
