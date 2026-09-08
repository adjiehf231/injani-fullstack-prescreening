"""
PDF Generator for PT Injani Systems Fullstack Developer Prescreening
Generates: docs/Adjie_Hari_Fajar_Fullstack_Developer_Prescreening_PT_Injani_Systems.pdf
"""

import os
import re
import html
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Preformatted
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas

OUTPUT_PATH = os.path.join("docs", "Adjie_Hari_Fajar_Fullstack_Developer_Prescreening_PT_Injani_Systems.pdf")

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        # Skip header and footer on cover page (Page 1)
        if self._pageNumber == 1:
            return

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))

        # Running Header
        self.drawString(54, 842 - 36, "PT Injani Systems - Fullstack Developer Prescreening")
        self.drawRightString(595 - 54, 842 - 36, "Programmer (NextJS & Python)")
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.75)
        self.line(54, 842 - 42, 595 - 54, 842 - 42)

        # Running Footer
        self.line(54, 44, 595 - 54, 44)
        self.drawString(54, 32, "Candidate: Adjie Hari Fajar")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(595 - 54, 32, page_text)
        self.restoreState()


def get_styles():
    base = getSampleStyleSheet()
    
    styles = {
        'CoverSuper': ParagraphStyle(
            'CoverSuper',
            parent=base['Normal'],
            fontName='Helvetica-Bold',
            fontSize=11,
            leading=14,
            textColor=colors.HexColor('#2563EB'),
            textTransform='uppercase',
            spaceAfter=6
        ),
        'CoverTitle': ParagraphStyle(
            'CoverTitle',
            parent=base['Title'],
            fontName='Helvetica-Bold',
            fontSize=24,
            leading=30,
            textColor=colors.HexColor('#0F172A'),
            alignment=TA_LEFT,
            spaceAfter=10
        ),
        'CoverSubtitle': ParagraphStyle(
            'CoverSubtitle',
            parent=base['Normal'],
            fontName='Helvetica',
            fontSize=13,
            leading=18,
            textColor=colors.HexColor('#475569'),
            spaceAfter=25
        ),
        'H1': ParagraphStyle(
            'H1',
            parent=base['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=16,
            leading=20,
            textColor=colors.HexColor('#0F172A'),
            spaceBefore=16,
            spaceAfter=8,
            keepWithNext=True
        ),
        'H2': ParagraphStyle(
            'H2',
            parent=base['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=12,
            leading=16,
            textColor=colors.HexColor('#1E293B'),
            spaceBefore=12,
            spaceAfter=6,
            keepWithNext=True
        ),
        'H3': ParagraphStyle(
            'H3',
            parent=base['Heading3'],
            fontName='Helvetica-Bold',
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#334155'),
            spaceBefore=8,
            spaceAfter=4,
            keepWithNext=True
        ),
        'Body': ParagraphStyle(
            'Body',
            parent=base['Normal'],
            fontName='Helvetica',
            fontSize=9,
            leading=13,
            textColor=colors.HexColor('#1E293B'),
            spaceAfter=6
        ),
        'BodyBold': ParagraphStyle(
            'BodyBold',
            parent=base['Normal'],
            fontName='Helvetica-Bold',
            fontSize=9,
            leading=13,
            textColor=colors.HexColor('#0F172A'),
            spaceAfter=6
        ),
        'Bullet': ParagraphStyle(
            'Bullet',
            parent=base['Normal'],
            fontName='Helvetica',
            fontSize=9,
            leading=13,
            textColor=colors.HexColor('#1E293B'),
            leftIndent=14,
            firstLineIndent=-10,
            spaceAfter=3
        ),
        'QuestionBox': ParagraphStyle(
            'QuestionBox',
            parent=base['Normal'],
            fontName='Helvetica-Oblique',
            fontSize=9,
            leading=13,
            textColor=colors.HexColor('#334155'),
            leftIndent=12,
            spaceBefore=4,
            spaceAfter=8
        ),
        'CodeBlock': ParagraphStyle(
            'CodeBlock',
            parent=base['Code'],
            fontName='Courier',
            fontSize=7.5,
            leading=10,
            textColor=colors.HexColor('#0F172A')
        ),
        'CandidateInput': ParagraphStyle(
            'CandidateInput',
            parent=base['Normal'],
            fontName='Courier',
            fontSize=8,
            leading=11,
            textColor=colors.HexColor('#B45309'),
            leftIndent=10,
            spaceAfter=4
        ),
        'TableHeader': ParagraphStyle(
            'TableHeader',
            parent=base['Normal'],
            fontName='Helvetica-Bold',
            fontSize=8,
            leading=10,
            textColor=colors.white,
            alignment=TA_LEFT
        ),
        'TableCell': ParagraphStyle(
            'TableCell',
            parent=base['Normal'],
            fontName='Helvetica',
            fontSize=8,
            leading=11,
            textColor=colors.HexColor('#1E293B')
        ),
        'TableCellBold': ParagraphStyle(
            'TableCellBold',
            parent=base['Normal'],
            fontName='Helvetica-Bold',
            fontSize=8,
            leading=11,
            textColor=colors.HexColor('#0F172A')
        )
    }
    return styles


def format_markdown_inline(text):
    """Inline markdown formatter converting bold, italics, code, and linebreaks for ReportLab Paragraphs."""
    # Normalize typography to clean standard ASCII (prevents broken glyphs in PDF engines)
    text = text.replace('—', ' - ').replace('–', '-').replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    # Convert <br> variants to placeholder
    text = re.sub(r'<br\s*/?>', '__BR_TAG__', text, flags=re.IGNORECASE)
    # Escape XML chars
    text = html.escape(text)
    # Restore <br/>
    text = text.replace('__BR_TAG__', '<br/>')
    # Bold italic
    text = re.sub(r'\*\*\*(.*?)\*\*\*', r'<b><i>\1</i></b>', text)
    # Bold
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # Italic
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    # Inline code
    text = re.sub(r'`(.*?)`', r'<font name="Courier" color="#1E293B"><b>\1</b></font>', text)
    # Markdown links: [text](url) -> <b>text</b>
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'<b>\1</b>', text)
    return text


def sanitize_ascii_art(text):
    """Replaces Unicode box-drawing and arrow characters with standard ASCII for Courier font."""
    char_map = {
        '│': '|',
        '┃': '|',
        '─': '-',
        '━': '-',
        '┌': '+',
        '┏': '+',
        '┐': '+',
        '┓': '+',
        '└': '+',
        '┗': '+',
        '┘': '+',
        '┛': '+',
        '├': '+',
        '┣': '+',
        '┤': '+',
        '┫': '+',
        '┬': '+',
        '┳': '+',
        '┴': '+',
        '┻': '+',
        '┼': '+',
        '╋': '+',
        '►': '>',
        '◄': '<',
        '▼': 'v',
        '▲': '^',
        '↓': 'v',
        '↑': '^',
        '→': '->',
        '←': '<-',
        '↔': '<->',
        '—': '-',
        '–': '-',
        '•': '*',
        '·': '*'
    }
    for k, v in char_map.items():
        text = text.replace(k, v)
    return text


def build_pdf():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = get_styles()
    story = []
    
    # ----------------------------------------------------
    # COVER PAGE
    # ----------------------------------------------------
    story.append(Spacer(1, 40))
    story.append(Paragraph("PT Injani Systems", styles['CoverSuper']))
    story.append(Paragraph("Fullstack Developer Prescreening Questions", styles['CoverTitle']))
    story.append(Paragraph("Technical Assessment Report - Programmer (NextJS & Python)", styles['CoverSubtitle']))
    
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#2563EB"), spaceBefore=0, spaceAfter=25))
    
    meta_data = [
        [Paragraph("<b>Candidate Name</b>", styles['TableCell']), Paragraph("Adjie Hari Fajar", styles['TableCellBold'])],
        [Paragraph("<b>Target Position</b>", styles['TableCell']), Paragraph("Programmer (NextJS & Python)", styles['TableCellBold'])],
        [Paragraph("<b>Hiring Organization</b>", styles['TableCell']), Paragraph("PT Injani Systems", styles['TableCellBold'])],
        [Paragraph("<b>Submission Date</b>", styles['TableCell']), Paragraph("September 2026", styles['TableCellBold'])],
        [Paragraph("<b>Repository</b>", styles['TableCell']), Paragraph("github.com/adjiehf231/injani-fullstack-prescreening", styles['TableCellBold'])],
        [Paragraph("<b>Backend Test Status</b>", styles['TableCell']), Paragraph("pytest - 26/26 Automated Tests Passed (All Passed)", styles['TableCellBold'])],
        [Paragraph("<b>Frontend Auth Tests</b>", styles['TableCell']), Paragraph("tsx - 8/8 Strict Cryptographic Tests Passed", styles['TableCellBold'])],
        [Paragraph("<b>Frontend Build Status</b>", styles['TableCell']), Paragraph("Next.js 14 App Router - Typecheck, Lint & Build Passed", styles['TableCellBold'])],
        [Paragraph("<b>Security Verification</b>", styles['TableCell']), Paragraph("Cryptographic JWT Verification (jose) & HMAC Webhooks", styles['TableCellBold'])],
    ]
    t_meta = Table(meta_data, colWidths=[150, 337])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#E2E8F0")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t_meta)
    
    story.append(Spacer(1, 40))
    
    # Executive Summary Box
    summary_html = (
        "<b>Assessment Overview:</b><br/>"
        "This engineering report contains verified technical solutions for PT Injani Systems prescreening assessment. "
        "It provides rigorous, production-grade answers for candidate personal profile (P1-P5) and 7 comprehensive "
        "technical challenges spanning self-hosted Gemma 3 LLM order extraction, PostgreSQL 16 SLA analytics, "
        "Google Cloud Tasks monitoring, composite index optimization for keyset pagination, Next.js 14 edge JWT "
        "cryptographic verification, Python asyncio background job idempotency, and fullstack CI/CD cloud deployment."
    )
    t_summary = Table([[Paragraph(summary_html, styles['Body'])]], colWidths=[487])
    t_summary.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EFF6FF")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#BFDBFE")),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(t_summary)
    
    story.append(PageBreak())
    
    # ----------------------------------------------------
    # TABLE OF CONTENTS / INDEX
    # ----------------------------------------------------
    story.append(Paragraph("Table of Contents", styles['H1']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#E2E8F0"), spaceBefore=2, spaceAfter=12))
    
    toc_data = [
        [Paragraph("<b>Section</b>", styles['TableHeader']), Paragraph("<b>Topic / Question</b>", styles['TableHeader']), Paragraph("<b>Domain</b>", styles['TableHeader'])],
        [Paragraph("<b>Part A</b>", styles['TableCell']), Paragraph("<b>Candidate Profile (P1-P5)</b>", styles['TableCellBold']), Paragraph("Work Style, Startup Fit, Aspirations", styles['TableCell'])],
        [Paragraph("P1", styles['TableCell']), Paragraph("Work Style & Independence (Autonomous Discovery)", styles['TableCell']), Paragraph("Engineering Workflow", styles['TableCell'])],
        [Paragraph("P2", styles['TableCell']), Paragraph("Startup Environment Fit & Fullstack Ownership", styles['TableCell']), Paragraph("Team Culture & Velocity", styles['TableCell'])],
        [Paragraph("P3", styles['TableCell']), Paragraph("2-3 Year Engineering Aspirations", styles['TableCell']), Paragraph("Career Growth & Architecture", styles['TableCell'])],
        [Paragraph("P4", styles['TableCell']), Paragraph("Motivation for PT Injani Systems Role", styles['TableCell']), Paragraph("Fullstack & Cloud Scope", styles['TableCell'])],
        [Paragraph("P5", styles['TableCell']), Paragraph("Expected Monthly Salary", styles['TableCell']), Paragraph("Compensation", styles['TableCell'])],
        [Paragraph("<b>Part B</b>", styles['TableCell']), Paragraph("<b>Technical Challenges (Q1-Q7)</b>", styles['TableCellBold']), Paragraph("Next.js, Python, PostgreSQL, Cloud", styles['TableCell'])],
        [Paragraph("Q1", styles['TableCell']), Paragraph("AI-Powered WhatsApp Order Processing (Gemma 3 / Ollama)", styles['TableCell']), Paragraph("AI/ML, Intent Extraction", styles['TableCell'])],
        [Paragraph("Q2", styles['TableCell']), Paragraph("SLA Analytics Dashboard (PostgreSQL Generated Columns & Next.js)", styles['TableCell']), Paragraph("PostgreSQL, Next.js RSC", styles['TableCell'])],
        [Paragraph("Q3", styles['TableCell']), Paragraph("Testing & Monitoring Google Cloud Tasks Workflows", styles['TableCell']), Paragraph("Cloud Tasks, Logging, DLQ", styles['TableCell'])],
        [Paragraph("Q4", styles['TableCell']), Paragraph("PostgreSQL 10M-Row Query Optimization & Keyset Indexing", styles['TableCell']), Paragraph("EXPLAIN ANALYZE, Indexing", styles['TableCell'])],
        [Paragraph("Q5", styles['TableCell']), Paragraph("Next.js API Design: Cryptographic JWT, Rate Limit, Errors", styles['TableCell']), Paragraph("Security, Edge Middleware", styles['TableCell'])],
        [Paragraph("Q6", styles['TableCell']), Paragraph("Python Async Workers, Progress Tracking & Idempotency", styles['TableCell']), Paragraph("FastAPI, Background Jobs", styles['TableCell'])],
        [Paragraph("Q7", styles['TableCell']), Paragraph("Fullstack System Design, Docker & Workload Identity CI/CD", styles['TableCell']), Paragraph("System Design, DevOps, GCP", styles['TableCell'])],
        [Paragraph("<b>Validation</b>", styles['TableCell']), Paragraph("<b>Automated Verification & Test Execution Results</b>", styles['TableCellBold']), Paragraph("Pytest, Build, Lint, Typecheck", styles['TableCell'])],
        [Paragraph("<b>Notes</b>", styles['TableCell']), Paragraph("<b>Technical Assumptions & Known Limitations</b>", styles['TableCellBold']), Paragraph("Production Considerations", styles['TableCell'])],
    ]
    t_toc = Table(toc_data, colWidths=[60, 277, 150])
    t_toc.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E293B")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_toc)
    
    story.append(PageBreak())
    
    # ----------------------------------------------------
    # READ PRESCREENING_ANSWERS.md AND PARSE CONTENT
    # ----------------------------------------------------
    with open("PRESCREENING_ANSWERS.md", "r", encoding="utf-8") as f:
        content = f.read()
        
    # Split into sections based on markdown headings
    lines = content.split('\n')
    
    i = 0
    in_code_block = False
    code_lines = []
    
    def flush_code():
        nonlocal code_lines
        if code_lines:
            raw_code = sanitize_ascii_art("\n".join(code_lines))
            all_lines = raw_code.split('\n')
            chunk_size = 28
            for start_idx in range(0, len(all_lines), chunk_size):
                chunk = all_lines[start_idx:start_idx + chunk_size]
                wrapped_lines = []
                for cline in chunk:
                    while len(cline) > 80:
                        wrapped_lines.append(cline[:80])
                        cline = "    " + cline[80:]
                    wrapped_lines.append(cline)
                clean_code = "\n".join(wrapped_lines)
                
                p_code = Preformatted(clean_code, styles['CodeBlock'])
                t_box = Table([[p_code]], colWidths=[475])
                t_box.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
                    ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor("#CBD5E1")),
                    ('TOPPADDING', (0, 0), (-1, -1), 4),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                    ('LEFTPADDING', (0, 0), (-1, -1), 6),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ]))
                story.append(t_box)
                story.append(Spacer(1, 2))
            story.append(Spacer(1, 4))
            code_lines = []

    in_table = False
    table_rows = []

    def flush_table():
        nonlocal table_rows
        if table_rows:
            col_count = max(len(r) for r in table_rows)
            # Calculate widths dynamically
            total_w = 487
            w_per_col = total_w / col_count
            col_widths = [w_per_col] * col_count
            
            # Format cells
            formatted_table = []
            for r_idx, row in enumerate(table_rows):
                formatted_row = []
                for c_idx, cell in enumerate(row):
                    cell_text = format_markdown_inline(cell.strip())
                    if r_idx == 0:
                        formatted_row.append(Paragraph(cell_text, styles['TableHeader']))
                    else:
                        formatted_row.append(Paragraph(cell_text, styles['TableCell']))
                while len(formatted_row) < col_count:
                    formatted_row.append(Paragraph("", styles['TableCell']))
                formatted_table.append(formatted_row)
                
            t = Table(formatted_table, colWidths=col_widths)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E293B")),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ]))
            story.append(t)
            story.append(Spacer(1, 6))
            table_rows = []

    # Skip document header until Part A
    start_idx = 0
    for idx, l in enumerate(lines):
        if l.strip().startswith("# Part A"):
            start_idx = idx
            break
            
    proc_lines = lines[start_idx:]
    
    for line in proc_lines:
        s_line = line.strip()
        
        # Code fence handling
        if s_line.startswith("```"):
            if in_code_block:
                in_code_block = False
                flush_code()
            else:
                if in_table:
                    in_table = False
                    flush_table()
                in_code_block = True
                code_lines = []
            continue
            
        if in_code_block:
            code_lines.append(line)
            continue
            
        # Table handling
        if s_line.startswith("|") and s_line.endswith("|"):
            # Check if separator row
            if re.match(r'^\|(\s*:?-+:?\s*\|)+$', s_line):
                continue
            cells = [c for c in s_line.split('|')[1:-1]]
            table_rows.append(cells)
            in_table = True
            continue
        else:
            if in_table:
                in_table = False
                flush_table()
                
        # Empty line
        if not s_line:
            continue
            
        # Horizontal Rule
        if s_line == "---":
            story.append(HRFlowable(width="100%", thickness=0.75, color=colors.HexColor("#E2E8F0"), spaceBefore=8, spaceAfter=8))
            continue
            
        # Major Section Headings
        if s_line.startswith("# Part B") or s_line.startswith("# Verification"):
            story.append(PageBreak())
            h_text = format_markdown_inline(s_line.lstrip('#').strip())
            story.append(Paragraph(h_text, styles['H1']))
            story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2563EB"), spaceBefore=2, spaceAfter=10))
            continue
            
        if s_line.startswith("# Part A"):
            # No extra PageBreak, starts directly on page after TOC
            h_text = format_markdown_inline(s_line.lstrip('#').strip())
            story.append(Paragraph(h_text, styles['H1']))
            story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2563EB"), spaceBefore=2, spaceAfter=10))
            continue
            
        if s_line.startswith("## "):
            # Sub-question heading (P1, P2, Q1, Q2, etc.)
            raw_h = s_line.lstrip('#').strip()
            # Give a page break before major Q questions to ensure clean layout
            if re.match(r'^Q[1-7]\b', raw_h):
                story.append(PageBreak())
            h_text = format_markdown_inline(raw_h)
            story.append(Paragraph(h_text, styles['H1']))
            story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceBefore=2, spaceAfter=8))
            continue
            
        if s_line.startswith("### "):
            h_text = format_markdown_inline(s_line.lstrip('#').strip())
            story.append(Paragraph(h_text, styles['H2']))
            continue
            
        if s_line.startswith("#### "):
            h_text = format_markdown_inline(s_line.lstrip('#').strip())
            story.append(Paragraph(h_text, styles['H3']))
            continue
            
        # Blockquote (Question prompt)
        if s_line.startswith("> "):
            q_text = format_markdown_inline(s_line[2:].strip())
            p_q = Paragraph(f"<b>Question:</b> <i>{q_text}</i>", styles['QuestionBox'])
            t_q = Table([[p_q]], colWidths=[487])
            t_q.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
                ('LINELEFT', (0, 0), (-1, -1), 3, colors.HexColor("#3B82F6")),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ]))
            story.append(t_q)
            story.append(Spacer(1, 4))
            continue
            
        # Bullet list item
        if s_line.startswith("- ") or s_line.startswith("* "):
            b_text = format_markdown_inline(s_line[2:].strip())
            story.append(Paragraph(f"&bull; {b_text}", styles['Bullet']))
            continue
            
        # Numbered list item
        m_num = re.match(r'^(\d+)\.\s+(.*)$', s_line)
        if m_num:
            num = m_num.group(1)
            n_text = format_markdown_inline(m_num.group(2).strip())
            story.append(Paragraph(f"<b>{num}.</b> {n_text}", styles['Bullet']))
            continue
            
        # Normal body paragraph
        p_text = format_markdown_inline(s_line)
        story.append(Paragraph(p_text, styles['Body']))
        
    # Flush any remaining table/code
    if in_code_block:
        flush_code()
    if in_table:
        flush_table()
        
    # ----------------------------------------------------
    # FINAL SECTION: TECHNICAL NOTES
    # ----------------------------------------------------
    story.append(PageBreak())
    story.append(Paragraph("Technical Notes & Production Considerations", styles['H1']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2563EB"), spaceBefore=2, spaceAfter=10))
    
    notes_html = (
        "<b>1. Architectural Assumptions:</b><br/>"
        "• <i>Open-Weight LLM:</i> The reference architecture targets Gemma 3 (4B / 12B) served via vLLM with PagedAttention on an NVIDIA GPU (L4 / A10G) or Ollama for local prototyping. The repository includes an automated deterministic evaluation harness and prompt template to ensure zero-cost testing without GPU dependencies.<br/>"
        "• <i>State Persistence:</i> For local review, rate limiting and idempotency stores are implemented as thread-safe in-memory stores. In multi-container cloud deployments (Cloud Run + Vercel), these back cleanly to Upstash Redis or AWS ElastiCache without contract changes.<br/><br/>"
        "<b>2. Production Scaling Recommendations:</b><br/>"
        "• <i>PostgreSQL:</i> Use declarative monthly range partitioning on <code>transactions</code> to maintain constant-time B-tree indexes as transaction volumes exceed 10M+ rows.<br/>"
        "• <i>Security:</i> Maintain strict separation between coarse-grained Edge authentication (HMAC-SHA256 signature verification via <code>jose</code>) and backend authorization (object-level tenant/user ownership verification).<br/>"
        "• <i>DevOps:</i> All cloud container deployments leverage Google Cloud Workload Identity Federation (WIF) to eliminate long-lived service account JSON keys."
    )
    t_notes = Table([[Paragraph(notes_html, styles['Body'])]], colWidths=[487])
    t_notes.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(t_notes)
    
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF generated successfully at: {OUTPUT_PATH}")

if __name__ == "__main__":
    build_pdf()
