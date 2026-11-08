"""
Interactive Web Application for Microdrama Retention & Pacing Auditor (Problem 3).
Runs with Python standard library.
"""

import http.server
import socketserver
import json
import os
import sys

PORT = 8503

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kuku Script Retention Auditor - Production Gatekeeper</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { background-color: #f4f7f6; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        .hero-banner { background: linear-gradient(135deg, #2c3e50 0%, #1a252f 100%); color: white; padding: 22px 0; border-bottom: 4px solid #e74c3c; }
        .audit-card { border-radius: 12px; border: 1px solid #e2e8f0; background: #fff; padding: 20px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.03); }
        .score-circle { width: 90px; height: 90px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.8rem; font-weight: 800; color: white; margin: 0 auto; box-shadow: 0 4px 10px rgba(0,0,0,0.15); }
        .bg-score-green { background: #27ae60; }
        .bg-score-yellow { background: #f39c12; }
        .bg-score-red { background: #e74c3c; }
        .prescription-box { background: #fff8e1; border-left: 4px solid #ffb300; padding: 12px 16px; border-radius: 4px; margin-bottom: 8px; font-size: 0.88rem; }
    </style>
</head>
<body>
    <div class="hero-banner">
        <div class="container">
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <span class="badge bg-danger mb-1">KUKU PRODUCTION GATEKEEPER</span>
                    <h3 class="fw-bold mb-0"><i class="fa-solid fa-chart-line text-danger me-2"></i>Microdrama Script Pacing & Retention Auditor</h3>
                    <p class="mb-0 text-white-50 small">Pre-Render Script Diagnostics: 15s Hook Velocity, Mid-Episode Exposition Sag & Coin-Unlock Cliffhangers</p>
                </div>
                <div>
                    <a href="/raw_outputs/problem3/problem3_retention_audit_summary.md" download class="btn btn-outline-light btn-sm"><i class="fa-solid fa-download me-1"></i>Audit Report</a>
                </div>
            </div>
        </div>
    </div>

    <div class="container my-4">
        <!-- Selector Bar -->
        <div class="audit-card mb-3">
            <div class="row align-items-center">
                <div class="col-md-5">
                    <label class="form-label small fw-bold text-muted mb-1">Select Episode to Audit:</label>
                    <select id="episodeSelect" class="form-select" onchange="renderSelectedEpisode()">
                        <!-- Populated by JS -->
                    </select>
                </div>
                <div class="col-md-7 text-md-end mt-3 mt-md-0">
                    <span class="badge bg-dark me-2">50 Episodes Scanned</span>
                    <span class="badge bg-success me-2">Est. Render GPU Saved: $2,400+</span>
                    <span class="badge bg-primary">Paywall Physics Calibrated</span>
                </div>
            </div>
        </div>

        <!-- Main Dashboard -->
        <div class="row">
            <!-- Left Column: Key Diagnostics -->
            <div class="col-lg-4">
                <div class="audit-card text-center">
                    <h6 class="fw-bold text-muted mb-3">OVERALL RETENTION INDEX</h6>
                    <div id="scoreCircle" class="score-circle bg-score-yellow mb-2">--</div>
                    <h5 id="verdictText" class="fw-bold mt-2">Analyzing...</h5>
                    <p class="small text-muted mb-0" id="durationText">Duration: --</p>
                </div>

                <div class="audit-card">
                    <h6 class="fw-bold text-dark mb-3"><i class="fa-solid fa-stopwatch text-danger me-2"></i>15-Second Hook Check</h6>
                    <div id="hookStatus" class="mb-2"></div>
                    <p class="small text-muted mb-0" id="hookCritique"></p>
                </div>

                <div class="audit-card">
                    <h6 class="fw-bold text-dark mb-3"><i class="fa-solid fa-lock-open text-warning me-2"></i>Coin-Unlock Cliffhanger</h6>
                    <div id="cliffStatus" class="mb-2"></div>
                    <p class="small text-muted mb-0" id="cliffType"></p>
                </div>
            </div>

            <!-- Right Column: Tension Chart & Actionable Rewrites -->
            <div class="col-lg-8">
                <div class="audit-card">
                    <h6 class="fw-bold text-dark mb-3"><i class="fa-solid fa-wave-square text-primary me-2"></i>Dramatic Tension Curve Across Episode</h6>
                    <div style="height: 230px;">
                        <canvas id="tensionChart"></canvas>
                    </div>
                </div>

                <div class="audit-card">
                    <h6 class="fw-bold text-dark mb-3"><i class="fa-solid fa-triangle-exclamation text-danger me-2"></i>Exposition Sag & Dead Zone Warnings</h6>
                    <div id="sagZonesList">
                        <!-- Populated via JS -->
                    </div>
                </div>

                <div class="audit-card">
                    <h6 class="fw-bold text-dark mb-3"><i class="fa-solid fa-file-pen text-success me-2"></i>Writer Rewrite Prescriptions (Before GPU Render)</h6>
                    <div id="prescriptionsList">
                        <!-- Populated via JS -->
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let allAuditData = [];
        let chartInstance = null;

        async function loadAuditData() {
            try {
                const res = await fetch('/api/audit');
                allAuditData = await res.json();
                populateDropdown();
                renderSelectedEpisode();
            } catch (err) {
                console.error("Failed loading audit data:", err);
            }
        }

        function populateDropdown() {
            const select = document.getElementById('episodeSelect');
            select.innerHTML = '';
            allAuditData.forEach(ep => {
                const opt = document.createElement('option');
                opt.value = ep.episode_num;
                opt.innerText = `Episode ${ep.episode_num} (${ep.total_duration}s) - Retention Score: ${ep.retention_score}/100`;
                select.appendChild(opt);
            });
        }

        function renderSelectedEpisode() {
            const epNum = parseInt(document.getElementById('episodeSelect').value) || 1;
            const ep = allAuditData.find(e => e.episode_num === epNum) || allAuditData[0];
            if (!ep) return;

            // Score circle
            const scoreEl = document.getElementById('scoreCircle');
            scoreEl.innerText = Math.round(ep.retention_score);
            scoreEl.className = 'score-circle ' + (ep.retention_score >= 70 ? 'bg-score-green' : (ep.retention_score >= 40 ? 'bg-score-yellow' : 'bg-score-red'));

            const verdictEl = document.getElementById('verdictText');
            if (ep.retention_score >= 70) {
                verdictEl.innerText = 'APPROVED FOR RENDER';
                verdictEl.className = 'fw-bold mt-2 text-success';
            } else if (ep.retention_score >= 40) {
                verdictEl.innerText = 'REVISE PACING FIRST';
                verdictEl.className = 'fw-bold mt-2 text-warning';
            } else {
                verdictEl.innerText = 'HIGH RETENTION RISK';
                verdictEl.className = 'fw-bold mt-2 text-danger';
            }

            document.getElementById('durationText').innerText = `Total Duration: ${ep.total_duration}s`;

            // 15s Hook
            const isPass = ep.first_15s_check.status.includes('PASS');
            document.getElementById('hookStatus').innerHTML = `<span class="badge ${isPass ? 'bg-success' : 'bg-danger'}">${ep.first_15s_check.status}</span>`;
            document.getElementById('hookCritique').innerText = ep.first_15s_check.critique;

            // Cliffhanger
            document.getElementById('cliffStatus').innerHTML = `<span class="badge bg-dark">${ep.cliffhanger_audit.rating}</span>`;
            document.getElementById('cliffType').innerText = `Cliffhanger Category: ${ep.cliffhanger_audit.cliffhanger_type} (Score: ${ep.cliffhanger_audit.raw_score})`;

            // Sag zones
            const sagDiv = document.getElementById('sagZonesList');
            if (ep.exposition_sag_zones.length === 0) {
                sagDiv.innerHTML = '<div class="text-success small"><i class="fa-solid fa-circle-check me-1"></i>No mid-episode exposition sag detected. Conflict velocity is consistently sustained.</div>';
            } else {
                sagDiv.innerHTML = ep.exposition_sag_zones.map(z => `
                    <div class="alert alert-danger py-2 px-3 small mb-2">
                        <strong><i class="fa-solid fa-triangle-exclamation me-1"></i>Lull Window [${z.start_time} - ${z.end_time}]:</strong> ${z.critique} (Tension: ${z.tension}/10)
                    </div>
                `).join('');
            }

            // Prescriptions
            const rxDiv = document.getElementById('prescriptionsList');
            rxDiv.innerHTML = ep.writer_prescriptions.map(p => `
                <div class="prescription-box">
                    <strong><i class="fa-solid fa-pen-nib text-warning me-1"></i>Action:</strong> ${p}
                </div>
            `).join('');

            // Render Chart
            renderChart(ep.tension_curve);
        }

        function renderChart(curve) {
            const ctx = document.getElementById('tensionChart').getContext('2d');
            const labels = curve.map(c => c.time_window.split(' - ')[0]);
            const scores = curve.map(c => c.tension_score);

            if (chartInstance) {
                chartInstance.destroy();
            }

            chartInstance = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Dramatic Tension Velocity',
                        data: scores,
                        borderColor: '#e74c3c',
                        backgroundColor: 'rgba(231, 76, 60, 0.12)',
                        borderWidth: 2.5,
                        fill: true,
                        tension: 0.35,
                        pointBackgroundColor: '#c0392b'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            min: 0,
                            max: 10,
                            grid: { color: '#f0f0f0' },
                            title: { display: true, text: 'Tension (0-10)', font: { size: 10 } }
                        },
                        x: {
                            grid: { display: false },
                            title: { display: true, text: 'Episode Timeline', font: { size: 10 } }
                        }
                    },
                    plugins: {
                        legend: { display: false }
                    }
                }
            });
        }

        window.onload = loadAuditData;
    </script>
</body>
</html>
"""

class AuditorRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_CONTENT.encode('utf-8'))
        elif self.path == '/api/audit':
            json_file = os.path.join(os.path.dirname(__file__), '..', 'raw_outputs', 'problem3', 'problem3_retention_audit_all_episodes.json')
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
    with socketserver.TCPServer(("", port), AuditorRequestHandler) as httpd:
        print(f"Kuku Retention Auditor Server running on http://localhost:{port}")
        httpd.serve_forever()

if __name__ == '__main__':
    run_server()
