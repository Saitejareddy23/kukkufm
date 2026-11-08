"""
AI Microdrama Script Pacing & Retention Auditor (Problem 3).
Analyzes screenplay pacing, detects 15s drop-off risk, mid-episode exposition sag,
and validates paywall-converting cliffhanger strength before expensive AI video rendering.
"""

import os
import re
import json
import glob
import sys

# Local imports from problem 1 parser
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'problem1_promo_finder'))
from screenplay_parser import parse_screenplay, time_to_sec, sec_to_time

# Conflict & Emotional Intensity Lexicons
HIGH_CONFLICT_KEYWORDS = [
    r'\bslap\b', r'\bshove\b', r'\bgrab\b', r'\bchoke\b', r'\bblade\b', r'\bdagger\b',
    r'\bsword\b', r'\bblood\b', r'\bseize\b', r'\bdisown\b', r'\bworthless\b', r'\bbetray\b',
    r'\bunworthy\b', r'\blow value\b', r'\barrest\b', r'\bkill\b', r'\bdie\b', r'\bshame\b',
    r'\benough\b', r'\btolerate\b', r'\bpoison\b', r'\bcrawl\b', r'\bthief\b', r'\bfilth\b',
    r'\bgallows\b', r'\bdisgrace\b', r'\bstrike\b', r'\bweep\b', r'\bsob\b'
]

POWER_SHIFT_KEYWORDS = [
    r'\bduke\b', r'\bhis grace\b', r'\bheir\b', r'\bcommander\b', r'\bcrest\b',
    r'\bsignet\b', r'\bemerald\b', r'\bdivorce\b', r'\bcontract\b', r'\bwho i am\b',
    r'\bhow dare you\b', r'\byou will regret\b', r'\bwatch me\b', r'\bmy wife\b'
]

CLIFFHANGER_TRIGGERS = [
    r'\bcut to black\b', r'\bcliffhanger\b', r'\bdrone\b', r'\bwho\b.*\?',
    r'\bwhat\b.*\?', r'\bwhy\b.*\?', r'\bfreeze\b', r'\barrest\b', r'\braises\b.*(blade|weapon|hand)'
]

PASSIVE_WORDS = [
    r'\bsits quietly\b', r'\bwalks slowly\b', r'\bsips tea\b', r'\blight breeze\b',
    r'\blooking around\b', r'\bnodding gently\b', r'\bexamining the room\b'
]

class MicrodramaRetentionAuditor:
    def __init__(self, screenplay_data):
        self.ep_num = screenplay_data['episode_num']
        self.logline = screenplay_data['logline']
        self.beats = screenplay_data['beats']
        self.total_duration = self.beats[-1]['end_sec'] if self.beats else 0.0
        self.analysis = {}

    def audit_episode(self):
        if not self.beats:
            return {"error": "No parsed beats found."}

        # 1. First 15-Second Hook Check
        first_15s_beats = [b for b in self.beats if b['start_sec'] <= 15.0]
        hook_text = " ".join([(b.get('text', '') + ' ' + b.get('tone', '')).lower() for b in first_15s_beats])
        
        has_early_conflict = any(re.search(kw, hook_text) for kw in HIGH_CONFLICT_KEYWORDS + POWER_SHIFT_KEYWORDS)
        first_15s_status = "PASS - High Immediate Stakes" if has_early_conflict else "FAIL - High Drop-off Risk"
        first_15s_critique = (
            "First 15s hooks viewer with immediate conflict/shock dialogue." if has_early_conflict
            else "First 15s contains passive exposition or establishing shots without tension. >50% viewers will swipe away before 00:15."
        )

        # 2. Tension Curve & Exposition Sag Detection
        # Slice into 15-second rolling windows across the episode
        window_size = 20.0
        sag_zones = []
        tension_points = []
        
        t = 0.0
        while t < self.total_duration:
            w_beats = [b for b in self.beats if t <= b['start_sec'] < t + window_size]
            w_text = " ".join([(b.get('text', '') + ' ' + b.get('tone', '')).lower() for b in w_beats])
            
            conflict_count = sum(1 for kw in HIGH_CONFLICT_KEYWORDS if re.search(kw, w_text))
            power_count = sum(1 for kw in POWER_SHIFT_KEYWORDS if re.search(kw, w_text))
            
            # Tension index: 0 to 10
            tension = min(10.0, conflict_count * 2.5 + power_count * 2.0 + (len(w_beats) * 0.4))
            tension_points.append({
                "time_window": f"{sec_to_time(t)} - {sec_to_time(min(self.total_duration, t + window_size))}",
                "start_sec": t,
                "tension_score": round(tension, 1)
            })
            
            # Sag detected if tension is under 2.5 in mid-episode (between 25s and total - 20s)
            if 25.0 <= t <= self.total_duration - 25.0 and tension < 2.5:
                sag_zones.append({
                    "start_time": sec_to_time(t),
                    "end_time": sec_to_time(min(self.total_duration, t + window_size)),
                    "duration": round(min(self.total_duration, t + window_size) - t, 1),
                    "tension": round(tension, 1),
                    "critique": "Dialogue lull or passive staging detected. Cut or inject sudden revelation/confrontation here."
                })
            t += 15.0

        # 3. Cliffhanger & Coin-Unlock Strength
        last_beats = [b for b in self.beats if b['end_sec'] >= self.total_duration - 10.0]
        end_text = " ".join([(b.get('text', '') + ' ' + b.get('tone', '')).lower() for b in last_beats])
        
        cliff_score = 0.0
        cliff_type = "Flat Exit / Weak Paywall"
        if any(re.search(kw, end_text) for kw in CLIFFHANGER_TRIGGERS):
            cliff_score += 4.0
            cliff_type = "Standard Microdrama Cut"
        if any(re.search(kw, end_text) for kw in HIGH_CONFLICT_KEYWORDS):
            cliff_score += 3.5
            cliff_type = "High-Stakes Peril / Ultimatum"
        if any(re.search(kw, end_text) for kw in POWER_SHIFT_KEYWORDS):
            cliff_score += 3.5
            cliff_type = "Shock Identity / Power Reveal"

        if cliff_score >= 6.5:
            cliff_rating = "TIER-1 WALLET OPENER (High Coin Unlock Rate)"
        elif cliff_score >= 4.0:
            cliff_rating = "TIER-2 MODERATE CLIFFHANGER"
        else:
            cliff_rating = "TIER-3 FLAT ENDING (Paywall Failure Risk)"

        # 4. Overall Retention Risk Score (0-100, where 100 is perfect viral pacing)
        base_score = 70.0
        if has_early_conflict:
            base_score += 15.0
        else:
            base_score -= 25.0

        base_score -= (len(sag_zones) * 10.0)
        
        if cliff_score >= 6.5:
            base_score += 15.0
        elif cliff_score < 4.0:
            base_score -= 20.0

        final_retention_score = max(10.0, min(100.0, base_score))

        # Actionable prescriptions for writer
        prescriptions = []
        if not has_early_conflict:
            prescriptions.append("HOOK FIX: Move the core argument or visual shock into 00:00 - 00:08. Eliminate establishing hallway/door walking.")
        if sag_zones:
            for sz in sag_zones[:2]:
                prescriptions.append(f"SAG FIX at {sz['start_time']}-{sz['end_time']}: Insert an emotional provocation, a veiled threat, or physical power move to maintain dialogue velocity.")
        if cliff_score < 6.5:
            prescriptions.append("CLIFFHANGER FIX: End episode 3 seconds EARLIER, right as the weapon/question is leveled, before anyone replies.")
        if not prescriptions:
            prescriptions.append("EXCELLENT PACING: Script is primed for viral retention and coin unlocks. Approved for AI video render.")

        self.analysis = {
            "episode_num": self.ep_num,
            "total_duration": round(self.total_duration, 2),
            "retention_score": round(final_retention_score, 1),
            "first_15s_check": {
                "status": first_15s_status,
                "critique": first_15s_critique
            },
            "exposition_sag_zones": sag_zones,
            "cliffhanger_audit": {
                "rating": cliff_rating,
                "cliffhanger_type": cliff_type,
                "raw_score": round(cliff_score, 1)
            },
            "writer_prescriptions": prescriptions,
            "tension_curve": tension_points
        }
        return self.analysis

def run_retention_audit(episodes_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    files = sorted(glob.glob(os.path.join(episodes_dir, '*.txt')))
    
    # Audit all 50 episodes
    print(f"Auditing pacing and retention for {len(files)} episodes...")
    all_reports = []
    
    for f in files:
        ep_data = parse_screenplay(f)
        auditor = MicrodramaRetentionAuditor(ep_data)
        rep = auditor.audit_episode()
        all_reports.append(rep)

    # Write raw unedited JSON
    json_path = os.path.join(output_dir, "problem3_retention_audit_all_episodes.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(all_reports, f, indent=2)
    print(f"Wrote raw JSON audit to {json_path}")

    # Write detailed markdown summary
    md_path = os.path.join(output_dir, "problem3_retention_audit_summary.md")
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write("# KUKU MICRODRAMA RETENTION & PACING AUDIT REPORT (PROBLEM 3)\n")
        f.write("### Production Gatekeeper: 15-Second Retention Drop & Paywall Cliffhanger Auditor\n\n")
        f.write(f"- **Total Episodes Evaluated:** {len(all_reports)}\n")
        f.write("- **Primary Objective:** Prevent thousands of dollars in wasted GPU video rendering by diagnosing script pacing flaws BEFORE production.\n\n")

        f.write("## 1. Episode Retention Scoreboard (Summary)\n\n")
        f.write("| Ep | Duration | Retention Score | 15s Hook Status | Mid-Episode Sag Zones | Cliffhanger Paywall Strength |\n")
        f.write("|:--:|:--------:|:---------------:|:---------------:|:---------------------:|:----------------------------|\n")
        
        for r in all_reports:
            hook_badge = "PASS" if "PASS" in r['first_15s_check']['status'] else "FAIL"
            sag_count = len(r['exposition_sag_zones'])
            sag_str = f"{sag_count} zone(s)" if sag_count > 0 else "None (Clean)"
            f.write(f"| Ep {r['episode_num']} | {r['total_duration']}s | **{r['retention_score']} / 100** | `{hook_badge}` | {sag_str} | {r['cliffhanger_audit']['rating'].split('(')[0].strip()} |\n")

        f.write("\n\n## 2. Deep Dive: High-Retention vs. At-Risk Episodes\n\n")
        
        # Sort best and worst
        sorted_by_score = sorted(all_reports, key=lambda x: x['retention_score'], reverse=True)
        top_eps = sorted_by_score[:3]
        bottom_eps = sorted_by_score[-3:]

        f.write("### Top Benchmark Episodes (Ready for Render Pipeline)\n")
        for ep in top_eps:
            f.write(f"#### Episode {ep['episode_num']} (Score: {ep['retention_score']} / 100)\n")
            f.write(f"- **15s Hook:** {ep['first_15s_check']['critique']}\n")
            f.write(f"- **Cliffhanger Quality:** {ep['cliffhanger_audit']['rating']}\n")
            f.write(f"- **Writer Feedback:** {ep['writer_prescriptions'][0]}\n\n")

        f.write("### At-Risk Episodes (Requires Script Rewrite Before GPU Render)\n")
        for ep in bottom_eps:
            f.write(f"#### Episode {ep['episode_num']} (Score: {ep['retention_score']} / 100)\n")
            f.write(f"- **15s Hook Failure:** {ep['first_15s_check']['critique']}\n")
            if ep['exposition_sag_zones']:
                for sz in ep['exposition_sag_zones']:
                    f.write(f"- **Exposition Sag detected at `{sz['start_time']} - {sz['end_time']}`**: {sz['critique']}\n")
            f.write(f"- **Cliffhanger Status:** {ep['cliffhanger_audit']['rating']}\n")
            f.write(f"- **Actionable Rewrite Prescriptions:**\n")
            for p in ep['writer_prescriptions']:
                f.write(f"  * {p}\n")
            f.write("\n")

    print(f"Wrote retention audit summary markdown to {md_path}")
    return all_reports

if __name__ == '__main__':
    episodes_dir = './kuku_assignment_pack/I Married a Broken Soldier. He was a Duke'
    output_dir = './raw_outputs/problem3'
    run_retention_audit(episodes_dir, output_dir)
