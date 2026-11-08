"""
Rich PDF Document Builder with high-level layout helpers.
Zero external dependencies.
"""

import sys
import os

class DocumentBuilder:
    def __init__(self, page_width=595.28, page_height=841.89): # A4
        self.width = page_width
        self.height = page_height
        self.pages = []
        self.current_page_commands = []
        self.current_page_num = 1
        self.total_pages = 2
        
    def new_page(self):
        if self.current_page_commands:
            self.pages.append(self.current_page_commands)
        self.current_page_commands = []
        self.current_page_num += 1
        
    def add_command(self, cmd):
        self.current_page_commands.append(cmd)
        
    def set_fill_color(self, r, g, b):
        self.add_command(f"{r:.3f} {g:.3f} {b:.3f} rg")
        
    def set_stroke_color(self, r, g, b):
        self.add_command(f"{r:.3f} {g:.3f} {b:.3f} RG")
        
    def set_line_width(self, w):
        self.add_command(f"{w:.2f} w")
        
    def draw_rect(self, x, y, w, h, fill=True, stroke=False):
        mode = "B" if (fill and stroke) else ("f" if fill else "S")
        self.add_command(f"{x:.2f} {y:.2f} {w:.2f} {h:.2f} re {mode}")
        
    def draw_line(self, x1, y1, x2, y2, stroke_color=(0.7, 0.7, 0.7), width=0.75):
        self.set_stroke_color(*stroke_color)
        self.set_line_width(width)
        self.add_command(f"{x1:.2f} {y1:.2f} m {x2:.2f} {y2:.2f} l S")

    def draw_text(self, text, x, y, font="F1", size=10, color=(0.1, 0.1, 0.1)):
        clean = str(text).replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')
        # replace smart quotes and em dashes if present
        clean = clean.replace('“', '"').replace('”', '"').replace('’', "'").replace('‘', "'").replace('—', '-').replace('–', '-')
        r, g, b = color
        cmd = f"BT /{font} {size} Tf {r:.3f} {g:.3f} {b:.3f} rg {x:.2f} {y:.2f} Td ({clean}) Tj ET"
        self.add_command(cmd)

    def wrap_text(self, text, max_width, font="F1", size=10):
        # Approximate char width
        char_w = size * (0.55 if font == "F2" else 0.50)
        max_chars = max(10, int(max_width / char_w))
        
        words = text.split()
        lines = []
        cur_line = []
        cur_len = 0
        
        for w in words:
            if cur_len + len(w) + (1 if cur_line else 0) <= max_chars:
                cur_line.append(w)
                cur_len += len(w) + (1 if len(cur_line) > 1 else 0)
            else:
                if cur_line:
                    lines.append(" ".join(cur_line))
                cur_line = [w]
                cur_len = len(w)
        if cur_line:
            lines.append(" ".join(cur_line))
        return lines

    def draw_paragraph(self, text, x, y, max_width, font="F1", size=9, line_height=11.5, color=(0.15, 0.15, 0.15)):
        lines = self.wrap_text(text, max_width, font=font, size=size)
        cur_y = y
        for line in lines:
            self.draw_text(line, x, cur_y, font=font, size=size, color=color)
            cur_y -= line_height
        return cur_y

    def draw_bullet_point(self, title, body, x, y, max_width, size=8.5, line_height=10.5):
        # Draw bullet circle or square
        self.set_fill_color(0.85, 0.25, 0.2)
        self.draw_rect(x, y + 2, 3.5, 3.5, fill=True, stroke=False)
        
        # Draw bold title
        title_w = len(title) * size * 0.55
        self.draw_text(title + ": ", x + 8, y, font="F2", size=size, color=(0.1, 0.1, 0.2))
        
        # Wrap remaining body
        lead_space = len(title + ": ") * size * 0.52
        first_line_w = max_width - 8 - lead_space
        
        words = body.split()
        first_line = []
        cur_len = 0
        max_first_chars = max(5, int(first_line_w / (size * 0.48)))
        
        rem_words = []
        for i, w in enumerate(words):
            if cur_len + len(w) + (1 if first_line else 0) <= max_first_chars:
                first_line.append(w)
                cur_len += len(w) + 1
            else:
                rem_words = words[i:]
                break
                
        if first_line:
            self.draw_text(" ".join(first_line), x + 8 + lead_space, y, font="F1", size=size, color=(0.2, 0.2, 0.2))
            cur_y = y - line_height
        else:
            cur_y = y - line_height
            rem_words = words
            
        if rem_words:
            rem_text = " ".join(rem_words)
            cur_y = self.draw_paragraph(rem_text, x + 8, cur_y, max_width - 8, font="F1", size=size, line_height=line_height, color=(0.2, 0.2, 0.2))
            
        return cur_y

    def draw_header_banner(self, problem_title, subtitle, student_name="Candidate", roll_no="ES23BTECH11021", branch="AI / CSE"):
        # Dark navy header bar
        self.set_fill_color(0.08, 0.15, 0.28) # deep corporate navy
        self.draw_rect(36, 755, 523, 58, fill=True)
        
        # Orange/Red accent bar on top
        self.set_fill_color(0.92, 0.32, 0.15) # energetic coral/orange
        self.draw_rect(36, 810, 523, 3, fill=True)
        
        # Logo / Org label
        self.draw_text("KUKU TV  |  AI GENERALIST ASSIGNMENT SUBMISSION", 48, 796, font="F2", size=8.5, color=(0.95, 0.65, 0.45))
        
        # Problem Title
        self.draw_text(problem_title, 48, 776, font="F2", size=14, color=(1.0, 1.0, 1.0))
        
        # Subtitle
        self.draw_text(subtitle, 48, 762, font="F3", size=8.5, color=(0.85, 0.9, 0.98))
        
        # Student info right box
        self.set_fill_color(0.14, 0.22, 0.38)
        self.draw_rect(410, 758, 142, 50, fill=True)
        self.draw_text(f"Applicant: {student_name}", 416, 795, font="F2", size=7.5, color=(1.0, 1.0, 1.0))
        self.draw_text(f"Roll No: {roll_no}", 416, 783, font="F1", size=7.5, color=(0.85, 0.9, 0.98))
        self.draw_text(f"Branch: {branch}", 416, 772, font="F1", size=7.5, color=(0.85, 0.9, 0.98))
        self.draw_text("Date: November 2026", 416, 762, font="F3", size=7.0, color=(0.7, 0.8, 0.9))

    def draw_footer(self, page_num, total_pages=2):
        self.draw_line(36, 32, 559, 32, stroke_color=(0.8, 0.8, 0.8), width=0.5)
        self.draw_text("Confidential & Proprietary  *  Kuku AI Generalist Assignment Submission", 36, 22, font="F3", size=7.0, color=(0.45, 0.45, 0.45))
        self.draw_text(f"Page {page_num} of {total_pages}", 515, 22, font="F2", size=7.5, color=(0.2, 0.2, 0.2))

    def draw_section_header(self, title, y, icon="*"):
        # Section title with accent background and line
        self.set_fill_color(0.94, 0.96, 0.99)
        self.draw_rect(36, y - 3, 523, 16, fill=True)
        self.set_fill_color(0.08, 0.22, 0.45)
        self.draw_rect(36, y - 3, 3, 16, fill=True)
        self.draw_text(f"{icon}  {title.upper()}", 44, y + 2, font="F2", size=9.0, color=(0.08, 0.22, 0.45))
        return y - 18

    def draw_card(self, title, body_lines, x, y, w, h, bg=(0.97, 0.98, 1.0), border=(0.82, 0.86, 0.92)):
        self.set_fill_color(*bg)
        self.draw_rect(x, y - h, w, h, fill=True)
        self.set_stroke_color(*border)
        self.set_line_width(0.75)
        self.draw_rect(x, y - h, w, h, fill=False, stroke=True)
        
        self.draw_text(title, x + 8, y - 12, font="F2", size=8.5, color=(0.1, 0.2, 0.4))
        cur_y = y - 24
        for line in body_lines:
            self.draw_text(line, x + 8, cur_y, font="F1", size=7.5, color=(0.2, 0.2, 0.2))
            cur_y -= 10
        return y - h - 6

    def draw_table(self, x, y, col_widths, headers, rows, header_bg=(0.12, 0.24, 0.45)):
        table_w = sum(col_widths)
        cur_y = y
        
        # Header Row
        self.set_fill_color(*header_bg)
        self.draw_rect(x, cur_y - 14, table_w, 14, fill=True)
        
        col_x = x
        for i, h in enumerate(headers):
            self.draw_text(h, col_x + 4, cur_y - 10, font="F2", size=7.5, color=(1.0, 1.0, 1.0))
            col_x += col_widths[i]
        cur_y -= 15
        
        # Data Rows
        for r_idx, row in enumerate(rows):
            row_h = 13.5
            bg = (0.97, 0.98, 0.99) if r_idx % 2 == 0 else (1.0, 1.0, 1.0)
            self.set_fill_color(*bg)
            self.draw_rect(x, cur_y - row_h, table_w, row_h, fill=True)
            self.set_stroke_color(0.88, 0.88, 0.90)
            self.draw_rect(x, cur_y - row_h, table_w, row_h, fill=False, stroke=True)
            
            col_x = x
            for c_idx, val in enumerate(row):
                self.draw_text(str(val), col_x + 4, cur_y - 9.5, font="F1", size=7.0, color=(0.15, 0.15, 0.15))
                col_x += col_widths[c_idx]
            cur_y -= row_h
            
        return cur_y - 5

    def finish(self):
        if self.current_page_commands:
            self.pages.append(self.current_page_commands)
            self.current_page_commands = []

    def to_pdf_bytes(self):
        self.finish()
        num_pages = len(self.pages)
        cat_id = 1
        pages_id = 2
        f1_id = 3
        f2_id = 4
        f3_id = 5
        
        curr_id = 6
        page_ids = []
        content_ids = []
        
        for _ in range(num_pages):
            page_ids.append(curr_id)
            curr_id += 1
            content_ids.append(curr_id)
            curr_id += 1
            
        objs = {}
        objs[cat_id] = f"<< /Type /Catalog /Pages {pages_id} 0 R >>"
        kids_str = " ".join([f"{pid} 0 R" for pid in page_ids])
        objs[pages_id] = f"<< /Type /Pages /Kids [{kids_str}] /Count {num_pages} >>"
        objs[f1_id] = f"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>"
        objs[f2_id] = f"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>"
        objs[f3_id] = f"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Oblique /Encoding /WinAnsiEncoding >>"
        
        for idx in range(num_pages):
            pid = page_ids[idx]
            cid = content_ids[idx]
            objs[pid] = (
                f"<< /Type /Page /Parent {pages_id} 0 R "
                f"/MediaBox [0 0 {self.width:.2f} {self.height:.2f}] "
                f"/Resources << /Font << /F1 {f1_id} 0 R /F2 {f2_id} 0 R /F3 {f3_id} 0 R >> >> "
                f"/Contents {cid} 0 R >>"
            )
            stream_body = "\n".join(self.pages[idx])
            stream_bytes = stream_body.encode('latin1', errors='replace')
            objs[cid] = f"<< /Length {len(stream_bytes)} >>\nstream\n{stream_body}\nendstream"
            
        out = bytearray()
        out.extend(b"%PDF-1.4\n")
        
        offsets = {}
        max_id = curr_id - 1
        for i in range(1, max_id + 1):
            offsets[i] = len(out)
            val = objs[i]
            out.extend(f"{i} 0 obj\n{val}\nendobj\n".encode('latin1', errors='replace'))
            
        xref_offset = len(out)
        out.extend(b"xref\n")
        out.extend(f"0 {max_id + 1}\n".encode('latin1'))
        out.extend(b"0000000000 65535 f \n")
        for i in range(1, max_id + 1):
            out.extend(f"{offsets[i]:010d} 00000 n \n".encode('latin1'))
            
        out.extend(f"trailer\n<< /Size {max_id + 1} /Root {cat_id} 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode('latin1'))
        return bytes(out)

    def save(self, filepath):
        data = self.to_pdf_bytes()
        with open(filepath, 'wb') as f:
            f.write(data)
        print(f"Generated PDF: {filepath} ({len(data)} bytes, {len(self.pages)} pages)")
