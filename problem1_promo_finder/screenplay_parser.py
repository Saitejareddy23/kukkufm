"""
Screenplay Parser for Kuku Microdrama Episodes.
"""

import re
import os
import glob

def time_to_sec(ts_str):
    if not ts_str:
        return 0.0
    ts_str = ts_str.strip('() ')
    parts = ts_str.split(':')
    if len(parts) == 2:
        try:
            return int(parts[0]) * 60 + float(parts[1])
        except ValueError:
            return 0.0
    return 0.0

def sec_to_time(secs):
    m = int(secs // 60)
    s = secs % 60
    return f"{m:02d}:{s:05.2f}"

def parse_screenplay(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Episode Number & Logline
    ep_num_match = re.search(r'EPISODE NUMBER:\s*Episode\s*(\d+)', content, re.IGNORECASE)
    ep_num = int(ep_num_match.group(1)) if ep_num_match else 0
    if ep_num == 0:
        fn_match = re.search(r'episode-(\d+)', os.path.basename(file_path))
        if fn_match:
            ep_num = int(fn_match.group(1))

    logline_match = re.search(r'EPISODE LOGLINE:\s*(.*?)(?=\n[A-Z0-9\s_-]+:|\n---)', content, re.DOTALL)
    logline = logline_match.group(1).strip() if logline_match else ""

    # Split into scenes
    scene_blocks = re.split(r'\n(?=SCENE\s+\d+)', content)
    
    beats = []
    
    time_pat = re.compile(r'Start:\s*\(([0-9:.]+)\)\s*\|\s*End:\s*\(([0-9:.]+)\)')
    
    for s_block in scene_blocks:
        if not s_block.strip() or 'SCENE' not in s_block:
            continue
            
        s_head_match = re.search(r'Scene heading:\s*(.*?)\n', s_block)
        scene_heading = s_head_match.group(1).strip() if s_head_match else ""
        
        # Regex to split beat blocks: **TYPE or **SPEAKER (TONE):**
        # Pattern captures:
        # **CAMERA:**
        # **ACTION:**
        # **SOUND FX:**
        # **CHARACTER (Tone):**
        # With colon inside the asterisks!
        pattern = re.compile(r'\*\*([^*]+?):\*\*\s*\nStart:\s*\(([0-9:.]+)\)\s*\|\s*End:\s*\(([0-9:.]+)\)\s*\n(.*?)(?=\n\*\*|\n---|\Z)', re.DOTALL)
        
        for m in pattern.finditer(s_block):
            header = m.group(1).strip()
            start_str = m.group(2).strip()
            end_str = m.group(3).strip()
            body_text = m.group(4).strip()
            
            start_sec = time_to_sec(start_str)
            end_sec = time_to_sec(end_str)
            
            beat_type = "ACTION"
            speaker = ""
            tone = ""
            
            if header.upper() == "CAMERA":
                beat_type = "CAMERA"
            elif header.upper() == "ACTION":
                beat_type = "ACTION"
            elif "SOUND" in header.upper():
                beat_type = "SOUND"
            else:
                beat_type = "DIALOGUE"
                # Parse speaker and tone: e.g. MATRIARCH (Cold, Commanding)
                sp_match = re.match(r'^(.*?)\s*\((.*?)\)$', header)
                if sp_match:
                    speaker = sp_match.group(1).strip()
                    tone = sp_match.group(2).strip()
                else:
                    speaker = header
                    tone = "Neutral"
                    
            beats.append({
                'episode_num': ep_num,
                'scene_heading': scene_heading,
                'beat_type': beat_type,
                'speaker': speaker,
                'tone': tone,
                'start_sec': start_sec,
                'end_sec': end_sec,
                'start_str': start_str,
                'end_str': end_str,
                'text': body_text
            })
            
    return {
        'episode_num': ep_num,
        'logline': logline,
        'file_path': file_path,
        'beats': beats
    }

if __name__ == '__main__':
    ep1 = parse_screenplay('./kuku_assignment_pack/I Married a Broken Soldier. He was a Duke/episode-001-Episode 1671703.txt')
    print(f"Parsed Episode {ep1['episode_num']} with {len(ep1['beats'])} beats.")
    for b in ep1['beats'][:8]:
        print(f"[{b['start_str']} -> {b['end_str']}] {b['beat_type']} ({b['speaker']}): {b['text'][:50]}...")
