"""
Promo Mining & Ranking Engine for Microdrama Series.
Finds 20-60 second high-converting promos with 3s scroll-stopping hooks,
unresolved cliffhangers, and standalone narrative intelligibility.
"""

import os
import re
import json
import glob
import sys

# Ensure local dir is on sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from screenplay_parser import parse_screenplay, time_to_sec, sec_to_time

# Dictionaries of Dramatic Keywords
HOOK_VIOLENCE_KEYWORDS = [
    r'\bslap\b', r'\bshove\b', r'\bgrab\b', r'\bchoke\b', r'\bstrike\b', r'\btear\b',
    r'\brip\b', r'\bcollar\b', r'\bblade\b', r'\bdagger\b', r'\bsword\b', r'\bblood\b',
    r'\bthrust\b', r'\bthrow\b', r'\bknock\b', r'\bseize\b', r'\bsmash\b', r'\bdrag\b',
    r'\bkneel\b', r'\bclench\b', r'\bpunch\b', r'\bshatter\b', r'\bpoison\b', r'\bthorns\b'
]

HOOK_SHOCK_DIALOGUE = [
    r'\bworthless\b', r'\bdisown\b', r'\bdisgrace\b', r'\bbetray\b', r'\btrash\b',
    r'\bbeggar\b', r'\bcripple\b', r'\bnot marry\b', r'\babandon\b', r'\bturn around\b',
    r'\bunworthy\b', r'\blow value\b', r'\barrest\b', r'\bkill\b', r'\bdie\b',
    r'\bwhore\b', r'\bhow dare\b', r'\bpathetic\b', r'\bget out\b', r'\bshame\b',
    r'\benough\b', r'\bembarrass\b', r'\btolerate\b', r'\bwho do you think\b',
    r'\bnot anymore\b', r'\blook for yourself\b', r'\bafter all i did\b', r'\bshameless\b',
    r'\bdivorce\b', r'\bswindle\b', r'\bthief\b', r'\bfilth\b', r'\brubbish\b',
    r'\byou disgust me\b', r'\bshut up\b', r'\bcut ties\b', r'\btramp\b'
]

REVEAL_KEYWORDS = [
    r'\bduke\b', r'\bhis grace\b', r'\bcrest\b', r'\bsignet\b', r'\bemerald\b',
    r'\bsecret\b', r'\bidentity\b', r'\btrue heir\b', r'\bbetrothed\b', r'\bwar hero\b',
    r'\bcommander\b', r'\bcontract\b', r'\bpoison\b', r'\bblackthorn\b', r'\binnocent\b',
    r'\bmarry me\b', r'\bmy wife\b', r'\bwho i am\b', r'\bhighness\b', r'\blord\b'
]

CLIFFHANGER_KEYWORDS = [
    r'\bwho\b.*\?', r'\bwhat\b.*\?', r'\bwhy\b.*\?', r'\bhow\b.*\?',
    r'\bdraws\b.*(sword|blade|dagger)', r'\braises\b.*(hand|fist|weapon)',
    r'\barrest\b', r'\bfreeze\b', r'\bstep back\b', r'\bguards\b',
    r'\bif you want\b', r'\bcrawl\b', r'\bor else\b', r'\bnever\b',
    r'\bcut to black\b', r'\bcliffhanger\b', r'\bdrone\b', r'\bstop\b',
    r'\bdefiance\b', r'\bresolute\b', r'\bseize\b', r'\bwatch me\b',
    r'\btrembling mouth\b', r'\byou will regret\b', r'\boff with\b'
]

RESOLUTION_PENALTY_KEYWORDS = [
    r'\bsmiles warmly\b', r'\bembrace\b', r'\bhug\b', r'\bkiss tenderly\b',
    r'\ball is forgiven\b', r'\blaughed together\b', r'\bhappily\b',
    r'\bleaves peacefully\b', r'\bapologized\b', r'\bcomforted her\b',
    r'\bguests chuckle\b', r'\blighthearted\b'
]

INTENSE_TONES = [
    'furious', 'cold', 'sneering', 'venomous', 'cruel', 'commanding',
    'scornful', 'desperate', 'mocking', 'arrogant', 'hard', 'trembling',
    'pleading', 'menacing', 'icily', 'shivering', 'murderous', 'harsh',
    'defiant', 'steely', 'breathless', 'shattered'
]

def evaluate_hook_window(beats_slice):
    """Evaluates the opening 3-second window for scroll-stopping hooks."""
    combined_text = " ".join([(b.get('text', '') + ' ' + b.get('tone', '')).lower() for b in beats_slice])
    score = 0.0
    hook_type = "Narrative Entry"
    hook_desc = ""

    # Check violence / physical action
    for kw in HOOK_VIOLENCE_KEYWORDS:
        if re.search(kw, combined_text):
            score += 0.50
            hook_type = "Physical Shock / Confrontation"
            break

    # Shocking dialogue
    for kw in HOOK_SHOCK_DIALOGUE:
        if re.search(kw, combined_text):
            score += 0.45
            if hook_type == "Narrative Entry":
                hook_type = "Verbal Humiliation / Betrayal"
            break

    # High stakes identity / authority reveal
    for kw in REVEAL_KEYWORDS:
        if re.search(kw, combined_text):
            score += 0.40
            if hook_type == "Narrative Entry":
                hook_type = "Shock Identity / Power Reveal"
            break

    # Tone intensity
    for b in beats_slice:
        tone_str = b.get('tone', '').lower()
        if any(it in tone_str for it in INTENSE_TONES):
            score += 0.15
            break

    # Construct hook description
    diag_beats = [b for b in beats_slice if b.get('beat_type') == 'DIALOGUE']
    if diag_beats:
        b = diag_beats[0]
        hook_desc = f"{b['speaker']} ({b['tone']}): \"{b['text'][:75]}\""
    elif beats_slice:
        b = beats_slice[0]
        hook_desc = f"{b['beat_type']}: {b['text'][:75]}"

    return min(1.0, score), hook_type, hook_desc

def evaluate_cliffhanger_window(beats_slice):
    """Evaluates the final 3-second window for unresolved tension."""
    combined_text = " ".join([(b.get('text', '') + ' ' + b.get('tone', '')).lower() for b in beats_slice])
    score = 0.0
    cliff_type = "Scene Cut"
    cliff_desc = ""

    # Penalty for resolution / de-escalation
    for rkw in RESOLUTION_PENALTY_KEYWORDS:
        if re.search(rkw, combined_text):
            return 0.1, "Weak Resolution", beats_slice[-1].get('text', '')[:70]

    last_beat = beats_slice[-1]
    
    # Check if last dialogue was an open question or cutting threat
    if last_beat.get('beat_type') == 'DIALOGUE':
        diag = last_beat.get('text', '').strip()
        if diag.endswith('?') or diag.endswith('...') or diag.endswith('?!'):
            score += 0.55
            cliff_type = "Unanswered Ultimatum / Interrogation"
        for kw in CLIFFHANGER_KEYWORDS:
            if re.search(kw, combined_text):
                score += 0.40
                cliff_type = "Impending Peril / Threat"
                break
    else:
        for kw in CLIFFHANGER_KEYWORDS:
            if re.search(kw, combined_text):
                score += 0.50
                cliff_type = "Sudden Action Cut on Climax"
                break
        if 'cut to black' in combined_text or 'drone' in combined_text or 'cliffhanger' in combined_text:
            score += 0.45
            cliff_type = "Ominous Music / Cut-to-Black Cliffhanger"

    for b in beats_slice:
        tone_str = b.get('tone', '').lower()
        if any(it in tone_str for it in INTENSE_TONES):
            score += 0.15
            break

    if last_beat.get('beat_type') == 'DIALOGUE':
        cliff_desc = f"{last_beat['speaker']}: \"{last_beat['text'][:75]}\""
    else:
        cliff_desc = f"{last_beat['beat_type']}: {last_beat['text'][:75]}"

    return min(1.0, score), cliff_type, cliff_desc

def compute_standalone_clarity(beats_slice):
    """Measures narrative intelligibility and conflict density."""
    conflict_beats = 0
    total_beats = len(beats_slice)
    if total_beats == 0:
        return 0.0

    speakers = set()
    has_villain_tone = False
    has_victim_or_hero = False

    for b in beats_slice:
        t = (b.get('text', '') + ' ' + b.get('tone', '')).lower()
        if b.get('beat_type') == 'DIALOGUE':
            speakers.add(b.get('speaker', ''))
            tone = b.get('tone', '').lower()
            if any(vt in tone for vt in ['cold', 'cruel', 'arrogant', 'sneering', 'mocking', 'furious']):
                has_villain_tone = True
            if any(ht in tone for ht in ['trembling', 'defiance', 'solemn', 'dignified', 'desperate']):
                has_victim_or_hero = True
        for kw in HOOK_VIOLENCE_KEYWORDS + HOOK_SHOCK_DIALOGUE + REVEAL_KEYWORDS:
            if re.search(kw, t):
                conflict_beats += 1
                break

    density = conflict_beats / max(1, total_beats)
    clarity_score = 0.35 + 0.35 * min(1.0, density * 1.5)
    if has_villain_tone and has_victim_or_hero:
        clarity_score += 0.20
    if len(speakers) >= 2:
        clarity_score += 0.10
    return min(1.0, clarity_score)

def find_promos_for_episode(ep_data, min_duration=20.0, max_duration=60.0):
    beats = ep_data['beats']
    num_beats = len(beats)
    candidates = []

    for i in range(num_beats):
        b_start = beats[i]
        t_start = b_start['start_sec']
        
        # Check first 3.5s window
        hook_window = [b for b in beats[i:] if b['start_sec'] <= t_start + 3.5]
        h_score, h_type, h_desc = evaluate_hook_window(hook_window)
        if h_score < 0.35:
            continue

        for j in range(i + 1, num_beats):
            b_end = beats[j]
            t_end = b_end['end_sec']
            dur = t_end - t_start

            if dur < min_duration:
                continue
            if dur > max_duration:
                break

            # Check last 3.5s window
            cliff_window = [b for b in beats[i:j+1] if b['end_sec'] >= t_end - 3.5]
            c_score, c_type, c_desc = evaluate_cliffhanger_window(cliff_window)
            if c_score < 0.35:
                continue

            slice_beats = beats[i:j+1]
            clarity_score = compute_standalone_clarity(slice_beats)

            # Sweet spot duration: 32s - 48s
            if 30.0 <= dur <= 50.0:
                dur_factor = 1.0
            elif dur < 30.0:
                dur_factor = 0.85 + 0.15 * ((dur - 20.0) / 10.0)
            else:
                dur_factor = 1.0 - 0.20 * ((dur - 50.0) / 10.0)

            overall_score = (
                0.35 * h_score +
                0.35 * c_score +
                0.20 * clarity_score +
                0.10 * dur_factor
            )

            rationale = (
                f"Opens on a sharp {h_type.lower()} within 3s; "
                f"builds high archetypal conflict across {int(dur)}s and cuts on a {c_type.lower()}."
            )

            candidates.append({
                'episode_num': ep_data['episode_num'],
                'segments': [
                    {
                        'start_sec': t_start,
                        'end_sec': t_end,
                        'start_time': sec_to_time(t_start),
                        'end_time': sec_to_time(t_end),
                        'duration': round(dur, 2)
                    }
                ],
                'total_duration': round(dur, 2),
                'score': round(overall_score, 3),
                'hook_score': round(h_score, 2),
                'hook_type': h_type,
                'hook_description': h_desc.replace('\n', ' '),
                'cliffhanger_score': round(c_score, 2),
                'cliffhanger_type': c_type,
                'cliffhanger_description': c_desc.replace('\n', ' '),
                'clarity_score': round(clarity_score, 2),
                'why_it_works': rationale
            })

    candidates.sort(key=lambda x: x['score'], reverse=True)

    # Non-maximal suppression
    deduped = []
    for cand in candidates:
        overlap = False
        c_start = cand['segments'][0]['start_sec']
        c_end = cand['segments'][0]['end_sec']
        for existing in deduped:
            e_start = existing['segments'][0]['start_sec']
            e_end = existing['segments'][0]['end_sec']
            inter = max(0, min(c_end, e_end) - max(c_start, e_start))
            if inter > 12.0:
                overlap = True
                break
        if not overlap:
            deduped.append(cand)
        if len(deduped) >= 3:
            break

    return deduped

def run_all_episodes(episodes_dir):
    files = sorted(glob.glob(os.path.join(episodes_dir, '*.txt')))
    print(f"Mining promos from {len(files)} screenplay files in '{episodes_dir}'...")
    
    all_episode_promos = []
    all_top_candidates = []

    for f in files:
        ep_data = parse_screenplay(f)
        promos = find_promos_for_episode(ep_data)
        all_episode_promos.append({
            'episode_num': ep_data['episode_num'],
            'logline': ep_data['logline'],
            'promos_found': len(promos),
            'promos': promos
        })
        all_top_candidates.extend(promos)

    all_top_candidates.sort(key=lambda x: x['score'], reverse=True)

    return all_episode_promos, all_top_candidates

def generate_output_files(episodes_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    all_episodes, top_cands = run_all_episodes(episodes_dir)

    # 1. Full unedited JSON output
    json_path = os.path.join(output_dir, "problem1_all_promos_raw.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump({
            'total_episodes_analyzed': len(all_episodes),
            'total_promos_extracted': len(top_cands),
            'top_ranked_promos': top_cands,
            'by_episode': all_episodes
        }, f, indent=2)
    print(f"Wrote full raw JSON to {json_path}")

    # 2. Human-readable Markdown summary report
    md_path = os.path.join(output_dir, "problem1_promos_ranked_summary.md")
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write("# KUKU MICRODRAMA PROMO MINING REPORT\n")
        f.write("### Series: *I Married a Broken Soldier. He was a Duke* (Episodes 1 - 50)\n\n")
        f.write(f"- **Total Episodes Analyzed:** {len(all_episodes)}\n")
        f.write(f"- **Total Qualified Promos Identified:** {len(top_cands)}\n")
        f.write(f"- **Optimal Duration Target:** 20.0s – 60.0s (Sweet Spot: 30.0s – 50.0s)\n\n")
        
        f.write("## 1. Top Ranked Promos Across All 50 Episodes\n\n")
        f.write("| Rank | Ep | Timestamps | Duration | Score | Hook Type | Cliffhanger Type | Why It Works |\n")
        f.write("|:----:|:--:|:----------:|:--------:|:-----:|:---------:|:----------------:|:-------------|\n")
        
        for idx, p in enumerate(top_cands[:20], 1):
            seg = p['segments'][0]
            f.write(f"| **#{idx}** | Ep {p['episode_num']} | `{seg['start_time']} - {seg['end_time']}` | {p['total_duration']}s | **{p['score']}** | {p['hook_type']} | {p['cliffhanger_type']} | {p['why_it_works']} |\n")

        f.write("\n\n## 2. In-Depth Breakdown of Top Campaign Launches (Which to Post First & Why)\n\n")
        for idx, p in enumerate(top_cands[:5], 1):
            seg = p['segments'][0]
            f.write(f"### Campaign Pick #{idx}: Episode {p['episode_num']} ({seg['start_time']} -> {seg['end_time']}, {p['total_duration']}s)\n")
            f.write(f"- **Overall Promo Score:** `{p['score']}`\n")
            f.write(f"- **Opening Hook (First 3s):** {p['hook_description']}\n")
            f.write(f"- **Ending Cliffhanger (Last 3s):** {p['cliffhanger_description']}\n")
            f.write(f"- **Narrative Rationale:** {p['why_it_works']}\n")
            f.write(f"- **Platform Strategy:** Ideal for TikTok / IG Reels Organic & Paid UA campaigns. Establishes visceral archetype immediately.\n\n")

        f.write("## 3. Episode-by-Episode Promo Directory (Episodes 1 - 50)\n\n")
        for ep in all_episodes:
            f.write(f"### Episode {ep['episode_num']}\n")
            f.write(f"**Logline:** *{ep['logline']}*\n\n")
            if ep['promos']:
                for p_idx, p in enumerate(ep['promos'], 1):
                    seg = p['segments'][0]
                    f.write(f"- **Promo Candidate {p_idx}** (`{seg['start_time']} - {seg['end_time']}`, {p['total_duration']}s | Score: {p['score']}):\n")
                    f.write(f"  - **Hook:** {p['hook_description']}\n")
                    f.write(f"  - **Cliffhanger:** {p['cliffhanger_description']}\n")
                    f.write(f"  - **Why It Works:** {p['why_it_works']}\n")
            else:
                f.write("- *No high-retention promo meeting the strict 20-60s hook/cliffhanger threshold in this transition episode.*\n")
            f.write("\n")

    print(f"Wrote ranked summary Markdown to {md_path}")
    return top_cands

if __name__ == '__main__':
    episodes_dir = './kuku_assignment_pack/I Married a Broken Soldier. He was a Duke'
    output_dir = './raw_outputs/problem1'
    generate_output_files(episodes_dir, output_dir)
