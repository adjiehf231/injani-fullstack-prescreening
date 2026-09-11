"""
DOCX Generator for PT Injani Systems Fullstack Developer Prescreening
Generates: docs/Adjie_Hari_Fajar_Fullstack_Developer_Prescreening_PT_Injani_Systems.docx
Source: PRESCREENING_ANSWERS.md

Features:
- Executive, human-designed layout (Calibri + Consolas typography)
- Cover page with structured metadata table & executive summary box
- Executive Table of Contents table with zebra striping
- Running header and dynamic footer with 'Page X of Y' fields (omitted on cover)
- Callout boxes with solid accent left border for Question prompts
- Beautiful syntax-styled code blocks with background shading and borders
- Formatted tables with repeating headers (tblHeader) and no row splits (cantSplit)
- Precise inline markdown parsing for bold, italic, inline code, and links
"""

import os
import re
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

OUTPUT_PATH = os.path.join("docs", "Adjie_Hari_Fajar_Fullstack_Developer_Prescreening_PT_Injani_Systems.docx")
SOURCE_MD = "PRESCREENING_ANSWERS.md"

# Color Palette (Slate + Injani Blue Accent)
COLOR_TEXT_MAIN = RGBColor(15, 23, 42)      # Slate 900
COLOR_TEXT_BODY = RGBColor(30, 41, 59)      # Slate 800
COLOR_TEXT_MUTED = RGBColor(100, 116, 139)  # Slate 500
COLOR_TEXT_QUESTION = RGBColor(51, 65, 85)  # Slate 700
COLOR_PRIMARY_BLUE = RGBColor(29, 78, 216)  # Blue 700 / Accent
COLOR_WHITE = RGBColor(255, 255, 255)

HEX_BG_LIGHT = "F8FAFC"       # Slate 50
HEX_BG_ALT = "F1F5F9"         # Slate 100
HEX_BG_CALLOUT = "EFF6FF"     # Blue 50
HEX_BORDER_MUTED = "E2E8F0"   # Slate 200
HEX_BORDER_DARK = "CBD5E1"    # Slate 300
HEX_PRIMARY_BLUE = "2563EB"   # Blue 600
HEX_HEADER_DARK = "1E293B"    # Slate 800


def set_cell_shading(cell, color_hex):
    """Applies background shading color to a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets cell padding in dxa (1 pt = 20 dxa)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)


def set_cell_borders(cell, top=None, bottom=None, left=None, right=None):
    """Sets custom borders on a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    borders = ['<w:tcBorders %s>' % nsdecls('w')]
    
    for side, border_spec in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        if border_spec:
            val = border_spec.get('val', 'single')
            sz = border_spec.get('sz', '4')
            col = border_spec.get('color', 'auto')
            borders.append(f'<w:{side} w:val="{val}" w:sz="{sz}" w:space="0" w:color="{col}"/>')
        else:
            borders.append(f'<w:{side} w:val="none"/>')
            
    borders.append('</w:tcBorders>')
    tcBorders = parse_xml(''.join(borders))
    tcPr.append(tcBorders)


def set_row_cant_split(row):
    """Ensures row doesn't break awkwardly across pages."""
    trPr = row._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))


def set_row_as_header(row):
    """Marks row as a repeating table header across pages."""
    trPr = row._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))


def add_field(p, field_str):
    """Adds a dynamic Word field like PAGE or NUMPAGES."""
    run = p.add_run()
    fldChar1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w'))
    instrText = parse_xml(r'<w:instrText %s xml:space="preserve"> %s </w:instrText>' % (nsdecls('w'), field_str))
    fldChar2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w'))
    fldChar3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w'))
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)
    return run


def add_hairline_bottom(p, color="E2E8F0", sz="4"):
    """Adds a subtle bottom border to a paragraph."""
    pPr = p._p.get_or_add_pPr()
    pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="{sz}" w:space="4" w:color="{color}"/></w:pBdr>')
    pPr.append(pBdr)


def add_hairline_top(p, color="E2E8F0", sz="4"):
    """Adds a subtle top border to a paragraph."""
    pPr = p._p.get_or_add_pPr()
    pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:top w:val="single" w:sz="{sz}" w:space="4" w:color="{color}"/></w:pBdr>')
    pPr.append(pBdr)


def append_formatted_runs(p, text, base_size_pt=10.5, base_color=COLOR_TEXT_BODY, is_italic_base=False):
    """Parses inline markdown tokens and appends formatted runs to paragraph."""
    token_pattern = re.compile(r'(\*\*\*.*?\*\*\*|\*\*.*?\*\*|\*.*?\*|`.*?`|\[.*?\]\(.*?\))')
    parts = token_pattern.split(text)
    
    for part in parts:
        if not part:
            continue
            
        # Bold Italic: ***text***
        if part.startswith('***') and part.endswith('***') and len(part) >= 6:
            r = p.add_run(part[3:-3])
            r.bold = True
            r.italic = True
            r.font.name = 'Calibri'
            r.font.size = Pt(base_size_pt)
            r.font.color.rgb = base_color
            
        # Bold: **text**
        elif part.startswith('**') and part.endswith('**') and len(part) >= 4:
            r = p.add_run(part[2:-2])
            r.bold = True
            r.italic = is_italic_base
            r.font.name = 'Calibri'
            r.font.size = Pt(base_size_pt)
            r.font.color.rgb = COLOR_TEXT_MAIN
            
        # Italic: *text*
        elif part.startswith('*') and part.endswith('*') and len(part) >= 2:
            r = p.add_run(part[1:-1])
            r.italic = True
            r.font.name = 'Calibri'
            r.font.size = Pt(base_size_pt)
            r.font.color.rgb = base_color
            
        # Inline code: `text`
        elif part.startswith('`') and part.endswith('`') and len(part) >= 2:
            r = p.add_run(part[1:-1])
            r.font.name = 'Consolas'
            r.font.size = Pt(base_size_pt * 0.9)
            r.font.color.rgb = COLOR_TEXT_MAIN
            r.bold = True
            
        # Markdown link: [text](url)
        elif part.startswith('[') and '](' in part and part.endswith(')'):
            m = re.match(r'\[(.*?)\]\((.*?)\)', part)
            if m:
                link_text = m.group(1)
                r = p.add_run(link_text)
                r.bold = True
                r.font.name = 'Calibri'
                r.font.size = Pt(base_size_pt)
                r.font.color.rgb = COLOR_PRIMARY_BLUE
            else:
                r = p.add_run(part)
                r.font.name = 'Calibri'
                r.font.size = Pt(base_size_pt)
                r.font.color.rgb = base_color
        else:
            # Plain text
            r = p.add_run(part)
            r.italic = is_italic_base
            r.font.name = 'Calibri'
            r.font.size = Pt(base_size_pt)
            r.font.color.rgb = base_color


def setup_document_styles():
    """Initializes the Word document with standard layout, margins, and headers/footers."""
    doc = docx.Document()
    
    # 0.85-inch margins (standard clean executive technical report)
    for section in doc.sections:
        section.top_margin = Inches(0.85)
        section.bottom_margin = Inches(0.85)
        section.left_margin = Inches(0.85)
        section.right_margin = Inches(0.85)
        section.different_first_page_header_footer = True
        
        # Header for page 2+
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.LEFT
        hp.paragraph_format.space_after = Pt(4)
        add_hairline_bottom(hp, color=HEX_BORDER_MUTED, sz="4")
        
        hr1 = hp.add_run("PT Injani Systems — Fullstack Developer Prescreening")
        hr1.font.name = "Calibri"
        hr1.font.size = Pt(8.5)
        hr1.font.color.rgb = COLOR_TEXT_MUTED
        
        hp.add_run("\t\t")
        
        hr2 = hp.add_run("Programmer (NextJS & Python)")
        hr2.font.name = "Calibri"
        hr2.font.size = Pt(8.5)
        hr2.font.color.rgb = COLOR_TEXT_MUTED
        hr2.bold = True
        
        # Footer for page 2+
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.LEFT
        fp.paragraph_format.space_before = Pt(6)
        add_hairline_top(fp, color=HEX_BORDER_MUTED, sz="4")
        
        fr1 = fp.add_run("Candidate: Adjie Hari Fajar")
        fr1.font.name = "Calibri"
        fr1.font.size = Pt(8.5)
        fr1.font.color.rgb = COLOR_TEXT_MUTED
        
        fp.add_run("\t\t")
        
        fr2 = fp.add_run("Page ")
        fr2.font.name = "Calibri"
        fr2.font.size = Pt(8.5)
        fr2.font.color.rgb = COLOR_TEXT_MUTED
        
        add_field(fp, "PAGE")
        
        fr3 = fp.add_run(" of ")
        fr3.font.name = "Calibri"
        fr3.font.size = Pt(8.5)
        fr3.font.color.rgb = COLOR_TEXT_MUTED
        
        add_field(fp, "NUMPAGES")
        
    return doc


def build_cover_page(doc):
    """Builds an executive, professional cover page."""
    # Top spacing
    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(20)
    sp.paragraph_format.space_after = Pt(0)
    
    # Organization Super-title
    p_super = doc.add_paragraph()
    p_super.paragraph_format.space_after = Pt(4)
    r_super = p_super.add_run("PT INJANI SYSTEMS")
    r_super.font.name = "Calibri"
    r_super.font.size = Pt(11)
    r_super.font.color.rgb = COLOR_PRIMARY_BLUE
    r_super.bold = True
    
    # Document Title
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_after = Pt(6)
    r_title = p_title.add_run("Fullstack Developer Prescreening Questions")
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(24)
    r_title.font.color.rgb = COLOR_TEXT_MAIN
    r_title.bold = True
    
    # Document Subtitle
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(14)
    r_sub = p_sub.add_run("Technical Assessment Report — Programmer (NextJS & Python)")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(13)
    r_sub.font.color.rgb = COLOR_TEXT_MUTED
    
    # Divider rule
    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_before = Pt(0)
    p_div.paragraph_format.space_after = Pt(18)
    add_hairline_bottom(p_div, color=HEX_PRIMARY_BLUE, sz="12")
    
    # Metadata Table
    meta_rows = [
        ("Candidate Name", "Adjie Hari Fajar"),
        ("Target Position", "Programmer (NextJS & Python)"),
        ("Hiring Organization", "PT Injani Systems"),
        ("Submission Date", "September 2026"),
        ("Repository", "github.com/adjiehf231/injani-fullstack-prescreening"),
        ("Backend Test Status", "pytest — 26/26 Automated Tests Passed (All Passed)"),
        ("Frontend Auth Tests", "tsx — 8/8 Strict Cryptographic Tests Passed"),
        ("Frontend Build Status", "Next.js 14 App Router — Typecheck, Lint & Build Passed"),
        ("Security Verification", "Cryptographic JWT Verification (jose) & HMAC Webhooks")
    ]
    
    meta_table = doc.add_table(rows=len(meta_rows), cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False
    
    col_widths = [Inches(2.1), Inches(4.7)]
    for r_idx, (label, val) in enumerate(meta_rows):
        row = meta_table.rows[r_idx]
        set_row_cant_split(row)
        
        # Cell 0: Label
        c0 = row.cells[0]
        c0.width = col_widths[0]
        set_cell_shading(c0, HEX_BG_LIGHT)
        set_cell_margins(c0, top=100, bottom=100, left=140, right=140)
        set_cell_borders(c0,
            top={'val': 'single', 'sz': '4', 'color': HEX_BORDER_MUTED},
            bottom={'val': 'single', 'sz': '4', 'color': HEX_BORDER_MUTED},
            left={'val': 'single', 'sz': '4', 'color': HEX_BORDER_MUTED},
            right={'val': 'single', 'sz': '4', 'color': HEX_BORDER_MUTED}
        )
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(label)
        r0.font.name = "Calibri"
        r0.font.size = Pt(9.5)
        r0.font.color.rgb = COLOR_TEXT_MUTED
        r0.bold = True
        
        # Cell 1: Value
        c1 = row.cells[1]
        c1.width = col_widths[1]
        set_cell_shading(c1, "FFFFFF" if r_idx % 2 == 0 else HEX_BG_LIGHT)
        set_cell_margins(c1, top=100, bottom=100, left=140, right=140)
        set_cell_borders(c1,
            top={'val': 'single', 'sz': '4', 'color': HEX_BORDER_MUTED},
            bottom={'val': 'single', 'sz': '4', 'color': HEX_BORDER_MUTED},
            left={'val': 'single', 'sz': '4', 'color': HEX_BORDER_MUTED},
            right={'val': 'single', 'sz': '4', 'color': HEX_BORDER_MUTED}
        )
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(val)
        r1.font.name = "Calibri"
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = COLOR_TEXT_MAIN
        r1.bold = (r_idx in [0, 1, 5, 6, 7])
        
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(20)
    p_sp.paragraph_format.space_after = Pt(0)
    
    # Executive Summary Box
    summary_table = doc.add_table(rows=1, cols=1)
    summary_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    summary_cell = summary_table.cell(0, 0)
    summary_cell.width = Inches(6.8)
    set_cell_shading(summary_cell, HEX_BG_CALLOUT)
    set_cell_margins(summary_cell, top=140, bottom=140, left=180, right=160)
    set_cell_borders(summary_cell,
        left={'val': 'single', 'sz': '24', 'color': HEX_PRIMARY_BLUE},
        top={'val': 'single', 'sz': '4', 'color': 'BFDBFE'},
        right={'val': 'single', 'sz': '4', 'color': 'BFDBFE'},
        bottom={'val': 'single', 'sz': '4', 'color': 'BFDBFE'}
    )
    
    p_sum = summary_cell.paragraphs[0]
    p_sum.paragraph_format.space_after = Pt(4)
    r_sum_title = p_sum.add_run("Assessment Overview\n")
    r_sum_title.font.name = "Calibri"
    r_sum_title.font.size = Pt(10.5)
    r_sum_title.font.color.rgb = COLOR_PRIMARY_BLUE
    r_sum_title.bold = True
    
    r_sum_body = p_sum.add_run(
        "This engineering report contains verified technical solutions for the PT Injani Systems prescreening assessment. "
        "It provides rigorous, production-grade answers for candidate profile questions (P1–P5) and 7 comprehensive technical challenges "
        "spanning self-hosted Gemma 3 LLM order extraction, PostgreSQL 16 SLA analytics, Google Cloud Tasks monitoring, "
        "composite index optimization for keyset pagination, Next.js 14 edge JWT cryptographic verification, "
        "Python asyncio background job idempotency, and fullstack CI/CD cloud deployment."
    )
    r_sum_body.font.name = "Calibri"
    r_sum_body.font.size = Pt(9.5)
    r_sum_body.font.color.rgb = COLOR_TEXT_BODY
    
    doc.add_page_break()


def build_toc_page(doc):
    """Builds a structured Table of Contents."""
    p_h1 = doc.add_paragraph()
    p_h1.paragraph_format.space_before = Pt(6)
    p_h1.paragraph_format.space_after = Pt(4)
    r_h1 = p_h1.add_run("Table of Contents")
    r_h1.font.name = "Calibri"
    r_h1.font.size = Pt(16)
    r_h1.font.color.rgb = COLOR_TEXT_MAIN
    r_h1.bold = True
    
    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_after = Pt(14)
    add_hairline_bottom(p_div, color=HEX_BORDER_MUTED, sz="8")
    
    toc_data = [
        ("Section", "Topic / Question", "Domain"),
        ("Part A", "Candidate Profile (P1–P5)", "Work Style, Startup Fit, Aspirations"),
        ("P1", "Work Style & Independence (Autonomous Discovery)", "Engineering Workflow"),
        ("P2", "Startup Environment Fit & Fullstack Ownership", "Team Culture & Velocity"),
        ("P3", "2–3 Year Engineering Aspirations", "Career Growth & Architecture"),
        ("P4", "Motivation for PT Injani Systems Role", "Fullstack & Cloud Scope"),
        ("P5", "Expected Monthly Salary & Compensation", "Compensation & Take Home Pay"),
        ("Part B", "Technical Challenges (Q1–Q7)", "Next.js, Python, PostgreSQL, Cloud"),
        ("Q1", "AI-Powered WhatsApp Order Processing (Gemma 3 / Ollama)", "AI/ML, Structured Extraction"),
        ("Q2", "SLA Analytics Dashboard (PostgreSQL Generated Columns & Next.js)", "PostgreSQL, Next.js RSC"),
        ("Q3", "Testing & Monitoring Google Cloud Tasks Workflows", "Cloud Tasks, Logging, DLQ"),
        ("Q4", "PostgreSQL 10M-Row Query Optimization & Keyset Indexing", "EXPLAIN ANALYZE, Indexing"),
        ("Q5", "Next.js API Design: Cryptographic JWT, Rate Limit, Errors", "Security, Edge Middleware"),
        ("Q6", "Python Async Workers, Progress Tracking & Idempotency", "FastAPI, Background Jobs"),
        ("Q7", "Fullstack System Design, Docker & Workload Identity CI/CD", "System Design, DevOps, GCP"),
        ("Validation", "Automated Verification & Test Execution Results", "Pytest, Build, Lint, Typecheck"),
        ("Notes", "Technical Assumptions & Known Limitations", "Production Considerations"),
    ]
    
    table = doc.add_table(rows=len(toc_data), cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    col_widths = [Inches(1.0), Inches(3.8), Inches(2.0)]
    
    for r_idx, (col0, col1, col2) in enumerate(toc_data):
        row = table.rows[r_idx]
        set_row_cant_split(row)
        
        is_header = (r_idx == 0)
        is_major_part = (col0 in ["Part A", "Part B", "Validation", "Notes"])
        
        if is_header:
            set_row_as_header(row)
            
        for c_idx, val in enumerate([col0, col1, col2]):
            cell = row.cells[c_idx]
            cell.width = col_widths[c_idx]
            
            if is_header:
                set_cell_shading(cell, HEX_HEADER_DARK)
            elif is_major_part:
                set_cell_shading(cell, HEX_BG_ALT)
            else:
                set_cell_shading(cell, "FFFFFF" if r_idx % 2 == 0 else HEX_BG_LIGHT)
                
            set_cell_margins(cell, top=90, bottom=90, left=120, right=120)
            set_cell_borders(cell,
                top={'val': 'single', 'sz': '4', 'color': HEX_BORDER_MUTED},
                bottom={'val': 'single', 'sz': '4', 'color': HEX_BORDER_MUTED},
                left={'val': 'single', 'sz': '4', 'color': HEX_BORDER_MUTED},
                right={'val': 'single', 'sz': '4', 'color': HEX_BORDER_MUTED}
            )
            
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(9)
            
            if is_header:
                r.font.color.rgb = COLOR_WHITE
                r.bold = True
            elif is_major_part:
                r.font.color.rgb = COLOR_TEXT_MAIN
                r.bold = True
            else:
                r.font.color.rgb = COLOR_TEXT_MAIN if c_idx == 1 else COLOR_TEXT_MUTED
                if c_idx == 0:
                    r.bold = True
                    
    doc.add_page_break()


def render_code_block(doc, code_lines):
    """Renders a formatted monospace code block inside a shaded container."""
    code_text = "\n".join(code_lines).strip("\n")
    if not code_text:
        return
        
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.cell(0, 0)
    cell.width = Inches(6.8)
    set_cell_shading(cell, HEX_BG_LIGHT)
    set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
    set_cell_borders(cell,
        top={'val': 'single', 'sz': '4', 'color': HEX_BORDER_DARK},
        bottom={'val': 'single', 'sz': '4', 'color': HEX_BORDER_DARK},
        left={'val': 'single', 'sz': '4', 'color': HEX_BORDER_DARK},
        right={'val': 'single', 'sz': '4', 'color': HEX_BORDER_DARK}
    )
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.05
    
    r = p.add_run(code_text)
    r.font.name = "Consolas"
    r.font.size = Pt(8.5)
    r.font.color.rgb = COLOR_TEXT_MAIN
    
    # Spacing after code block
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(4)
    p_sp.paragraph_format.space_after = Pt(4)


def render_callout_box(doc, question_text):
    """Renders a Question callout box with a prominent left accent border."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.cell(0, 0)
    cell.width = Inches(6.8)
    set_cell_shading(cell, HEX_BG_ALT)
    set_cell_margins(cell, top=100, bottom=100, left=160, right=140)
    set_cell_borders(cell,
        left={'val': 'single', 'sz': '24', 'color': HEX_PRIMARY_BLUE},
        top={'val': 'none'},
        right={'val': 'none'},
        bottom={'val': 'none'}
    )
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    
    r_lbl = p.add_run("Question: ")
    r_lbl.font.name = "Calibri"
    r_lbl.font.size = Pt(10)
    r_lbl.font.color.rgb = COLOR_PRIMARY_BLUE
    r_lbl.bold = True
    
    append_formatted_runs(p, question_text, base_size_pt=10, base_color=COLOR_TEXT_QUESTION, is_italic_base=True)
    
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(4)
    p_sp.paragraph_format.space_after = Pt(4)


def render_markdown_table(doc, table_rows):
    """Renders a formatted Markdown table in Word with alternating shading."""
    if not table_rows:
        return
        
    col_count = max(len(row) for row in table_rows)
    table = doc.add_table(rows=len(table_rows), cols=col_count)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    total_w = Inches(6.8)
    col_w = total_w / col_count
    
    for r_idx, row_data in enumerate(table_rows):
        row = table.rows[r_idx]
        set_row_cant_split(row)
        
        is_header = (r_idx == 0)
        if is_header:
            set_row_as_header(row)
            
        for c_idx in range(col_count):
            cell = row.cells[c_idx]
            cell.width = col_w
            
            if is_header:
                set_cell_shading(cell, HEX_HEADER_DARK)
            else:
                set_cell_shading(cell, "FFFFFF" if r_idx % 2 == 0 else HEX_BG_LIGHT)
                
            set_cell_margins(cell, top=90, bottom=90, left=120, right=120)
            set_cell_borders(cell,
                top={'val': 'single', 'sz': '4', 'color': HEX_BORDER_DARK},
                bottom={'val': 'single', 'sz': '4', 'color': HEX_BORDER_DARK},
                left={'val': 'single', 'sz': '4', 'color': HEX_BORDER_DARK},
                right={'val': 'single', 'sz': '4', 'color': HEX_BORDER_DARK}
            )
            
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            
            val = row_data[c_idx].strip() if c_idx < len(row_data) else ""
            if is_header:
                r = p.add_run(val)
                r.font.name = "Calibri"
                r.font.size = Pt(9)
                r.font.color.rgb = COLOR_WHITE
                r.bold = True
            else:
                append_formatted_runs(p, val, base_size_pt=9, base_color=COLOR_TEXT_BODY)
                
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(4)
    p_sp.paragraph_format.space_after = Pt(6)


def build_body(doc, markdown_file):
    """Parses PRESCREENING_ANSWERS.md line-by-line and generates polished document nodes."""
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    lines = content.split('\n')
    
    # Locate Part A start
    start_idx = 0
    for idx, l in enumerate(lines):
        if l.strip().startswith("# Part A"):
            start_idx = idx
            break
            
    proc_lines = lines[start_idx:]
    
    in_code = False
    code_lines = []
    
    in_table = False
    table_rows = []
    
    for line in proc_lines:
        s_line = line.strip()
        
        # Code fence handling
        if s_line.startswith("```"):
            if in_code:
                in_code = False
                render_code_block(doc, code_lines)
                code_lines = []
            else:
                if in_table:
                    in_table = False
                    render_markdown_table(doc, table_rows)
                    table_rows = []
                in_code = True
                code_lines = []
            continue
            
        if in_code:
            code_lines.append(line)
            continue
            
        # Table handling
        if s_line.startswith("|") and s_line.endswith("|"):
            if re.match(r'^\|(\s*:?-+:?\s*\|)+$', s_line):
                continue
            cells = [c.strip() for c in s_line.split('|')[1:-1]]
            table_rows.append(cells)
            in_table = True
            continue
        else:
            if in_table:
                in_table = False
                render_markdown_table(doc, table_rows)
                table_rows = []
                
        # Empty line
        if not s_line:
            continue
            
        # Horizontal Rule
        if s_line == "---":
            p_hr = doc.add_paragraph()
            p_hr.paragraph_format.space_before = Pt(4)
            p_hr.paragraph_format.space_after = Pt(8)
            add_hairline_bottom(p_hr, color=HEX_BORDER_MUTED, sz="6")
            continue
            
        # Major Part Header (# Part B or # Verification Results)
        if s_line.startswith("# Part B") or s_line.startswith("# Verification"):
            doc.add_page_break()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.keep_with_next = True
            r = p.add_run(s_line.lstrip('#').strip())
            r.font.name = "Calibri"
            r.font.size = Pt(16)
            r.font.color.rgb = COLOR_TEXT_MAIN
            r.bold = True
            add_hairline_bottom(p, color=HEX_PRIMARY_BLUE, sz="12")
            continue
            
        if s_line.startswith("# Part A"):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.keep_with_next = True
            r = p.add_run(s_line.lstrip('#').strip())
            r.font.name = "Calibri"
            r.font.size = Pt(16)
            r.font.color.rgb = COLOR_TEXT_MAIN
            r.bold = True
            add_hairline_bottom(p, color=HEX_PRIMARY_BLUE, sz="12")
            continue
            
        # Question Heading (## P1, ## Q1, etc.)
        if s_line.startswith("## "):
            heading_text = s_line.lstrip('#').strip()
            # Clean page break before major Q challenges for clear editorial reading
            if re.match(r'^Q[1-7]\b', heading_text):
                doc.add_page_break()
                
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.keep_with_next = True
            r = p.add_run(heading_text)
            r.font.name = "Calibri"
            r.font.size = Pt(14)
            r.font.color.rgb = COLOR_TEXT_MAIN
            r.bold = True
            add_hairline_bottom(p, color=HEX_BORDER_DARK, sz="6")
            continue
            
        # Sub-heading (### Question, ### Answer, etc.)
        if s_line.startswith("### "):
            sub_text = s_line.lstrip('#').strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.keep_with_next = True
            r = p.add_run(sub_text)
            r.font.name = "Calibri"
            r.font.size = Pt(11.5)
            r.font.color.rgb = COLOR_TEXT_MAIN
            r.bold = True
            continue
            
        # Minor sub-heading (#### Step 1, etc.)
        if s_line.startswith("#### "):
            minor_text = s_line.lstrip('#').strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.keep_with_next = True
            r = p.add_run(minor_text)
            r.font.name = "Calibri"
            r.font.size = Pt(10.5)
            r.font.color.rgb = RGBColor(51, 65, 85)
            r.bold = True
            continue
            
        # Blockquote (Question prompt)
        if s_line.startswith("> "):
            q_text = s_line[2:].strip()
            render_callout_box(doc, q_text)
            continue
            
        # Bullet list item
        if s_line.startswith("- ") or s_line.startswith("* "):
            bullet_text = s_line[2:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.25)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.line_spacing = 1.15
            
            # Bullet glyph
            r_bullet = p.add_run("•  ")
            r_bullet.font.name = "Calibri"
            r_bullet.font.size = Pt(10)
            r_bullet.font.color.rgb = COLOR_PRIMARY_BLUE
            r_bullet.bold = True
            
            append_formatted_runs(p, bullet_text, base_size_pt=10, base_color=COLOR_TEXT_BODY)
            continue
            
        # Numbered list item
        m_num = re.match(r'^(\d+)\.\s+(.*)$', s_line)
        if m_num:
            num_str = m_num.group(1)
            item_text = m_num.group(2).strip()
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.25)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.line_spacing = 1.15
            
            r_num = p.add_run(f"{num_str}.  ")
            r_num.font.name = "Calibri"
            r_num.font.size = Pt(10)
            r_num.font.color.rgb = COLOR_TEXT_MAIN
            r_num.bold = True
            
            append_formatted_runs(p, item_text, base_size_pt=10, base_color=COLOR_TEXT_BODY)
            continue
            
        # Normal body paragraph
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        append_formatted_runs(p, s_line, base_size_pt=10, base_color=COLOR_TEXT_BODY)
        
    # Flush trailing blocks
    if in_code:
        render_code_block(doc, code_lines)
    if in_table:
        render_markdown_table(doc, table_rows)
        
    # ----------------------------------------------------
    # FINAL SECTION: TECHNICAL NOTES & PRODUCTION CONSIDERATIONS
    # ----------------------------------------------------
    doc.add_page_break()
    p_notes_h = doc.add_paragraph()
    p_notes_h.paragraph_format.space_before = Pt(14)
    p_notes_h.paragraph_format.space_after = Pt(4)
    p_notes_h.paragraph_format.keep_with_next = True
    r_notes_h = p_notes_h.add_run("Technical Notes & Production Considerations")
    r_notes_h.font.name = "Calibri"
    r_notes_h.font.size = Pt(16)
    r_notes_h.font.color.rgb = COLOR_TEXT_MAIN
    r_notes_h.bold = True
    add_hairline_bottom(p_notes_h, color=HEX_PRIMARY_BLUE, sz="12")
    
    notes_table = doc.add_table(rows=1, cols=1)
    notes_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    notes_cell = notes_table.cell(0, 0)
    notes_cell.width = Inches(6.8)
    set_cell_shading(notes_cell, HEX_BG_LIGHT)
    set_cell_margins(notes_cell, top=140, bottom=140, left=160, right=160)
    set_cell_borders(notes_cell,
        top={'val': 'single', 'sz': '4', 'color': HEX_BORDER_DARK},
        bottom={'val': 'single', 'sz': '4', 'color': HEX_BORDER_DARK},
        left={'val': 'single', 'sz': '4', 'color': HEX_BORDER_DARK},
        right={'val': 'single', 'sz': '4', 'color': HEX_BORDER_DARK}
    )
    
    pn = notes_cell.paragraphs[0]
    pn.paragraph_format.space_after = Pt(4)
    rn_title1 = pn.add_run("1. Architectural Assumptions:\n")
    rn_title1.font.name = "Calibri"
    rn_title1.font.size = Pt(10.5)
    rn_title1.font.color.rgb = COLOR_TEXT_MAIN
    rn_title1.bold = True
    
    rn_body1 = pn.add_run(
        "• Open-Weight LLM: The reference architecture targets Gemma 3 (4B / 12B) served via vLLM with PagedAttention "
        "on an NVIDIA GPU (L4 / A10G) or Ollama for local prototyping. The repository includes an automated deterministic "
        "evaluation harness and prompt template to ensure zero-cost testing without GPU dependencies.\n"
        "• State Persistence: For local review, rate limiting and idempotency stores are implemented as thread-safe in-memory stores. "
        "In multi-container cloud deployments (Cloud Run + Vercel), these back cleanly to Upstash Redis or AWS ElastiCache without contract changes.\n\n"
    )
    rn_body1.font.name = "Calibri"
    rn_body1.font.size = Pt(9.5)
    rn_body1.font.color.rgb = COLOR_TEXT_BODY
    
    rn_title2 = pn.add_run("2. Production Scaling Recommendations:\n")
    rn_title2.font.name = "Calibri"
    rn_title2.font.size = Pt(10.5)
    rn_title2.font.color.rgb = COLOR_TEXT_MAIN
    rn_title2.bold = True
    
    rn_body2 = pn.add_run(
        "• PostgreSQL: Use declarative monthly range partitioning on transactions to bound B-tree index depth "
        "and maintain fast cursor-based seeks as transaction volumes exceed 10M+ rows.\n"
        "• Security: Maintain strict separation between coarse-grained Edge authentication (HMAC-SHA256 signature verification via jose) "
        "and backend authorization (object-level tenant/user ownership verification).\n"
        "• DevOps: All cloud container deployments leverage Google Cloud Workload Identity Federation (WIF) to eliminate long-lived service account JSON keys."
    )
    rn_body2.font.name = "Calibri"
    rn_body2.font.size = Pt(9.5)
    rn_body2.font.color.rgb = COLOR_TEXT_BODY


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    print(f"Generating DOCX from {SOURCE_MD}...")
    doc = setup_document_styles()
    build_cover_page(doc)
    build_toc_page(doc)
    build_body(doc, SOURCE_MD)
    doc.save(OUTPUT_PATH)
    print(f"DOCX successfully generated and saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
