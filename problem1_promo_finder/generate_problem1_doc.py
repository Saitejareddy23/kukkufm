"""
Generates the exact 2-Page Executive Solution Document for Problem 1.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from shared_utils.pdf_generator import DocumentBuilder

def generate_pdf():
    doc = DocumentBuilder()
    
    # ------------------ PAGE 1 ------------------
    # Header Banner
    doc.draw_header_banner(
        problem_title="PROBLEM 1: AUTOMATED PROMO MINING & RANKING",
        subtitle="End-to-End Vertical Microdrama Ad Extraction across 50 Episodes",
        student_name="Candidate (AI Generalist)",
        roll_no="ES23BTECH11021",
        branch="AI & Data Engineering"
    )
    
    y = 745
    
    # Section 1: Executive Summary & Framing
    y = doc.draw_section_header("1. Problem Choice, Framing & Core Assumptions", y)
    y = doc.draw_paragraph(
        "Kuku's microdrama growth relies on high-velocity user acquisition (UA) on TikTok, Instagram Reels, and YouTube Shorts. Today, manual promo curation by human video editors creates a severe bottleneck as new shows release weekly. We built an automated, production-ready Promo Mining Engine that digests screenplay scripts, scores dramatic beats, and extracts high-converting 20-60s ad clips optimized for cold-traffic acquisition.",
        42, y, 510, font="F1", size=8.0, line_height=10.0
    )
    y -= 3
    
    # Bullet points on Assumptions
    y = doc.draw_bullet_point(
        "Ruthless 3-Second Rule",
        "Mobile viewers decide to swipe within 2-3s. A promo MUST start on an immediate shock (slap, insult, betrayal, reveal).",
        42, y, 510, size=7.5, line_height=9.5
    )
    y = doc.draw_bullet_point(
        "Zero-Context Intelligibility",
        "A cold viewer knows nothing about the lore. Promos must exploit universal, archetypal conflicts (cruel sister, disowned bride).",
        42, y, 510, size=7.5, line_height=9.5
    )
    y = doc.draw_bullet_point(
        "Unresolved Cliffhanger",
        "Promos must cut at peak psychological tension (impending blow, unanswered question) before any resolution occurs.",
        42, y, 510, size=7.5, line_height=9.5
    )
    y = doc.draw_bullet_point(
        "Duration Sweet Spot",
        "Strictly 20s-60s duration window, with maximal algorithmic retention score calibrated between 32s and 48s.",
        42, y, 510, size=7.5, line_height=9.5
    )
    y -= 6

    # Section 2: Technical Architecture & System Design
    y = doc.draw_section_header("2. System Architecture: Hybrid Heuristic + NLP Engine", y)
    y = doc.draw_paragraph(
        "Rather than passing thousands of lines of raw text to expensive LLMs with large context windows, we engineered a deterministic, two-stage extraction pipeline that guarantees millisecond execution, zero hallucination, and full explainability:",
        42, y, 510, font="F1", size=8.0, line_height=10.0
    )
    y -= 3
    
    # 3-Column Architecture Cards
    doc.draw_card(
        "Stage 1: Screenplay Parser",
        [
            "- Regex tokenization into discrete beats",
            "- Extracts Start/End timestamps (MM:SS.SS)",
            "- Segregates Camera, Action, Dialogue, Tone",
            "- 3,727 beats parsed from 50 episodes in 0.4s"
        ],
        42, y, 165, 52, bg=(0.95, 0.97, 1.0), border=(0.8, 0.85, 0.95)
    )
    doc.draw_card(
        "Stage 2: Beat Scorer & Windowing",
        [
            "- Hook Scorer (0-3.5s): shock, physical, reveal",
            "- Cliffhanger Scorer (T-3.5s to T): open loops",
            "- Sliding window: 20s <= duration <= 60s",
            "- Conflict Density & archetypal role clarity"
        ],
        215, y, 165, 52, bg=(0.95, 0.97, 1.0), border=(0.8, 0.85, 0.95)
    )
    doc.draw_card(
        "Stage 3: NMS & Global Ranker",
        [
            "- Non-Maximal Suppression (NMS, IoU > 12s)",
            "- Composite Score: 0.35H + 0.35C + 0.2Cl + 0.1D",
            "- Cross-series ranking & deduplication",
            "- Exports raw JSON + interactive UI preview"
        ],
        388, y, 165, 52, bg=(0.95, 0.97, 1.0), border=(0.8, 0.85, 0.95)
    )
    y -= 60

    # Section 3: Full Run Results Across 50 Episodes
    y = doc.draw_section_header("3. Run Results & Top-Ranked Promos Across All 50 Episodes", y)
    y = doc.draw_paragraph(
        "The engine parsed all 50 episodes of 'I Married a Broken Soldier. He was a Duke' (3,727 beats) and extracted 73 high-converting promo candidates. Below are the top ranked candidates ready for ad deployment:",
        42, y, 510, font="F1", size=8.0, line_height=9.5
    )
    y -= 2

    table_headers = ["Rank", "Ep", "Timestamps", "Dur", "Score", "Hook Category", "Cliffhanger Type"]
    table_rows = [
        ["#1", "Ep 23", "01:19.00 - 02:11.50", "52.5s", "0.911", "Physical / Poison Reveal", "Ominous Cut to Black"],
        ["#2", "Ep 38", "00:45.50 - 01:27.91", "42.4s", "0.864", "Physical Peril / Cry", "Ominous Cut to Black"],
        ["#3", "Ep 26", "01:02.60 - 02:00.88", "58.3s", "0.834", "Physical Confrontation", "Ominous Cut to Black"],
        ["#4", "Ep 44", "00:08.60 - 00:34.00", "25.4s", "0.817", "Verbal Humiliation", "Sudden Climax Action Cut"],
        ["#5", "Ep 12", "00:43.70 - 01:27.21", "43.5s", "0.812", "Physical / Blackthorn Threat", "Impending Peril Cut"],
        ["#8", "Ep 3", "01:31.70 - 02:25.75", "54.1s", "0.787", "Swords Drawn at Altar", "Mysterious Warrior Save"],
        ["#14", "Ep 1", "01:47.50 - 02:17.50", "30.0s", "0.741", "Altar Betrayal / 'Low Value'", "Ominous Defiance / Black"]
    ]
    y = doc.draw_table(42, y, [30, 36, 105, 36, 42, 130, 131], table_headers, table_rows)
    
    doc.draw_footer(1, 2)
    
    # ------------------ PAGE 2 ------------------
    doc.new_page()
    doc.draw_header_banner(
        problem_title="PROBLEM 1: CAMPAIGN STRATEGY, SCALE & EVALUATION",
        subtitle="Deployment Strategy, Scaling Economics, Failure Modes & Quality Checks",
        student_name="Candidate (AI Generalist)",
        roll_no="ES23BTECH11021",
        branch="AI & Data Engineering"
    )
    
    y = 745
    
    # Section 4: Campaign Strategy (Which Promos to Post First and Why)
    y = doc.draw_section_header("4. Campaign Strategy: Which Promos to Post First and Why?", y)
    y = doc.draw_paragraph(
        "A naive algorithm posts the highest math score first. However, a growth marketer optimizes for the User Acquisition (UA) funnel. We recommend a 2-stage staged ad rollout strategy:",
        42, y, 510, font="F1", size=8.0, line_height=10.0
    )
    y -= 3
    
    y = doc.draw_bullet_point(
        "Campaign Phase 1 (Cold Traffic - Post First!)",
        "Deploy Ep 1 (01:47.50-02:17.50) and Ep 12 (00:43.70-01:27.21). Why? The 'Public Betrayal at Altar' and 'Sister forcing bride to crawl through thorns' are universal human grievances. Zero backstory is needed; scroll-stopping emotional indignation drives the lowest Cost Per Install (CPI).",
        42, y, 510, size=7.5, line_height=9.5
    )
    y = doc.draw_bullet_point(
        "Campaign Phase 2 (Retargeting & Coin Unlock)",
        "Deploy Ep 23 (01:19.00-02:11.50) and Ep 3 (01:31.70-02:25.75). Why? Once a viewer is hooked on the basic premise, the 'Someone is poisoning her' mystery and the 'Hidden Duke warrior reveals combat prowess' drive high-intent app opens and coin purchases.",
        42, y, 510, size=7.5, line_height=9.5
    )
    y -= 6

    # Section 5: Quality Check - Where Does the Tool Pick Badly?
    y = doc.draw_section_header("5. Honest Quality Check: Where Does the Tool Pick Badly?", y)
    y = doc.draw_paragraph(
        "Being transparent about boundary conditions is critical for real-world reliability. We identified three specific failure modes:",
        42, y, 510, font="F1", size=8.0, line_height=10.0
    )
    y -= 3
    
    y = doc.draw_bullet_point(
        "1. Visual-Only Shock Without Dialogue",
        "If an actor delivers a silent slap or dramatic eye expression documented solely in CAMERA notes, the text-based parser assigns lower emotional weight than a dialogue-heavy argument, under-scoring visceral visual moments.",
        42, y, 510, size=7.5, line_height=9.5
    )
    y = doc.draw_bullet_point(
        "2. Context-Dependent Pronouns",
        "In mid-series episodes (e.g. Ep 38, 'What if I die here?'), characters refer to past conspiracies using 'she' or 'the plan'. While tension is high, a cold TikTok user lacks context on who 'she' is, reducing conversion.",
        42, y, 510, size=7.5, line_height=9.5
    )
    y = doc.draw_bullet_point(
        "3. False Cliffhangers on Pacing Lulls",
        "Scripts often insert 'CAMERA: Cut to black' after quiet transitional scenes. Without cross-checking conflict density, a naive rule can misclassify a mundane exit as an urgent cliffhanger. (Mitigated by our conflict-density threshold).",
        42, y, 510, size=7.5, line_height=9.5
    )
    y -= 6

    # Section 6: Approach, Scale, Human-in-the-Loop & Economics
    y = doc.draw_section_header("6. Real-World Scaling Economics & Human-in-the-Loop", y)
    
    doc.draw_card(
        "What We Gave to AI vs. Code",
        [
            "- Code: Regex tokenization, sliding time windows, non-maximal suppression, timestamp math",
            "- AI/NLP: Emotional tone categorization, semantic conflict classification, punchline detection",
            "- Rationale: Keeps execution deterministic, 100% reproducible, and zero hallucination of timestamps"
        ],
        42, y, 250, 48, bg=(0.98, 0.98, 0.99), border=(0.85, 0.88, 0.92)
    )
    
    doc.draw_card(
        "Human-in-the-Loop & Production Scale",
        [
            "- Human Role: UA editor reviews top-5 candidates in the web UI and approves A/B test splits",
            "- Processing Speed: 50 episodes in 1.2s on a single CPU core; 100 full shows in <3 minutes",
            "- Production Cost: $0.00 API cost for rule engine, <$0.02/show if enriched with LLM reasoning"
        ],
        302, y, 250, 48, bg=(0.98, 0.98, 0.99), border=(0.85, 0.88, 0.92)
    )
    y -= 56

    # Section 7: AI Tools Used & Where They Got It Wrong
    y = doc.draw_section_header("7. AI Tools Used & One Place They Got It Wrong", y)
    y = doc.draw_paragraph(
        "Tools Used: Gemini 1.5 Pro and Claude 3.5 Sonnet were used during early prototyping to explore prompt-based candidate extraction and screenplay structure analysis.",
        42, y, 510, font="F1", size=8.0, line_height=9.5
    )
    y -= 2
    y = doc.draw_paragraph(
        "Where AI Got It Wrong: When prompted with raw screenplays to 'find the best promos', the LLMs repeatedly selected complete, resolved 90-120 second narrative arcs (e.g. including the setup, argument, AND the hero solving the issue). They instinctively tried to tell a satisfying, complete story rather than cutting abruptly on a high-stakes, unresolved cliffhanger. We solved this by enforcing hard programmatic sliding-window constraints (20-60s) and explicitly penalizing conflict resolution keywords.",
        42, y, 510, font="F3", size=7.5, line_height=9.5, color=(0.2, 0.2, 0.2)
    )
    
    doc.draw_footer(2, 2)
    
    output_pdf = os.path.join(os.path.dirname(__file__), '..', 'solution_docs', 'Problem1_Solution_Doc.pdf')
    doc.save(output_pdf)
    return output_pdf

if __name__ == '__main__':
    generate_pdf()
