import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_transformed_document():
    doc = docx.Document()
    
    # Page setup - Margins 1 inch
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
        
    # Styles configuration
    styles = doc.styles
    normal_style = styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    
    # Helper functions
    def set_cell_background(cell, fill_hex):
        tcPr = cell._element.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        tcPr.append(shd)

    def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
        tcPr = cell._element.get_or_add_tcPr()
        tcMar = OxmlElement('w:tcMar')
        for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
            node = OxmlElement(f'w:{m}')
            node.set(qn('w:w'), str(val))
            node.set(qn('w:type'), 'dxa')
            tcMar.append(node)
        tcPr.append(tcMar)

    def set_table_borders(table, color="CCCCCC", sz="4", val="single"):
        tblPr = table._element.xpath('w:tblPr')
        if tblPr:
            borders = parse_xml(
                f'<w:tblBorders {nsdecls("w")}>'
                f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
                f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
                f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
                f'<w:insideV w:val="none"/>'
                f'<w:left w:val="none"/>'
                f'<w:right w:val="none"/>'
                f'</w:tblBorders>'
            )
            tblPr[0].append(borders)

    def add_callout_box(title, text, border_color="003366", bg_color="F4F6F9"):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.5)
        set_cell_background(cell, bg_color)
        set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
        
        tcPr = cell._element.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/>'
            f'<w:top w:val="none"/>'
            f'<w:right w:val="none"/>'
            f'<w:bottom w:val="none"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(4)
        run_t = p.add_run(f"💡 {title}\n")
        run_t.bold = True
        run_t.font.name = "Calibri"
        run_t.font.size = Pt(11)
        run_t.font.color.rgb = RGBColor(0x00, 0x33, 0x66)
        
        run_b = p.add_run(text)
        run_b.font.name = "Calibri"
        run_b.font.size = Pt(10)
        run_b.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
        
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    def add_concept_block(doc, concept_num, concept_name, familiar_idea, real_life_eg, mechanism, purpose, tech_term, structure, relationship, practical_meaning, source_detail):
        h = doc.add_heading(f"Concept {concept_num}: {concept_name}", level=3)
        h.paragraph_format.space_before = Pt(14)
        h.paragraph_format.space_after = Pt(6)
        
        add_callout_box(f"Step 1 & 2: Familiar Idea & Real-Life Example — {concept_name}", 
                        f"Familiar Idea: {familiar_idea}\n\nReal-Life Example: {real_life_eg}")
        
        p = doc.add_paragraph()
        r = p.add_run("Step 3 — Mechanism (How It Works): ")
        r.bold = True
        r.font.color.rgb = RGBColor(0x00, 0x40, 0x80)
        p.add_run(mechanism)
        p.paragraph_format.space_after = Pt(4)
        
        p = doc.add_paragraph()
        r = p.add_run("Step 4 — Purpose (Why It Exists & Problem Solved): ")
        r.bold = True
        r.font.color.rgb = RGBColor(0x00, 0x40, 0x80)
        p.add_run(purpose)
        p.paragraph_format.space_after = Pt(4)
        
        p = doc.add_paragraph()
        r = p.add_run("Step 5 — Formal Technical Term: ")
        r.bold = True
        r.font.color.rgb = RGBColor(0x00, 0x40, 0x80)
        r_t = p.add_run(tech_term)
        r_t.bold = True
        p.paragraph_format.space_after = Pt(4)
        
        p = doc.add_paragraph()
        r = p.add_run("Step 6 — Detailed Structure & Components: ")
        r.bold = True
        r.font.color.rgb = RGBColor(0x00, 0x40, 0x80)
        p.add_run(structure)
        p.paragraph_format.space_after = Pt(4)
        
        p = doc.add_paragraph()
        r = p.add_run("Step 7 — Relationship to Other Concepts: ")
        r.bold = True
        r.font.color.rgb = RGBColor(0x00, 0x40, 0x80)
        p.add_run(relationship)
        p.paragraph_format.space_after = Pt(4)
        
        p = doc.add_paragraph()
        r = p.add_run("Step 8 — Practical Real-World Meaning: ")
        r.bold = True
        r.font.color.rgb = RGBColor(0x00, 0x40, 0x80)
        p.add_run(practical_meaning)
        p.paragraph_format.space_after = Pt(4)
        
        add_callout_box(f"Step 9: Complete Source-Level Detail — {concept_name}", 
                        source_detail, border_color="006633", bg_color="F0F8F0")

    def format_table(table, headers, rows_data):
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        set_table_borders(table)
        
        # Header Row
        hdr_cells = table.rows[0].cells
        for i, header_text in enumerate(headers):
            cell = hdr_cells[i]
            cell.text = header_text
            set_cell_background(cell, "003366")
            set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for run in p.runs:
                run.bold = True
                run.font.name = "Calibri"
                run.font.size = Pt(9.5)
                run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                
        # Data Rows
        for r_idx, row_data in enumerate(rows_data):
            row_cells = table.rows[r_idx + 1].cells
            bg_color = "F9FAFB" if r_idx % 2 == 1 else "FFFFFF"
            for c_idx, cell_value in enumerate(row_data):
                cell = row_cells[c_idx]
                cell.text = str(cell_value)
                set_cell_background(cell, bg_color)
                set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
                p = cell.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT if c_idx > 0 and cell_value not in ["Nil", "-"] and any(char.isdigit() for char in str(cell_value)) else WD_ALIGN_PARAGRAPH.LEFT
                for run in p.runs:
                    run.font.name = "Calibri"
                    run.font.size = Pt(9)
                    run.font.color.rgb = RGBColor(0x22, 0x22, 0x22)

    # ---------------------------------------------------------
    # DOCUMENT COVER & TITLE
    # ---------------------------------------------------------
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("HDFC BANK LIMITED\n")
    r_title.bold = True
    r_title.font.size = Pt(22)
    r_title.font.color.rgb = RGBColor(0x00, 0x33, 0x66)
    
    r_sub = p_title.add_run("Comprehensive Cognitive Learning & Structural Transformation Report\n")
    r_sub.bold = True
    r_sub.font.size = Pt(15)
    r_sub.font.color.rgb = RGBColor(0x00, 0x66, 0x99)
    
    r_meta = p_title.add_run("Unaudited Standalone & Consolidated Financial Results for the Quarter Ended June 30, 2026 (Q1 FY 2026-27)\nCIN: L65920MH1994PLC080618 | Registered Office: Sandoz House, Shivsagar Estate, Worli, Mumbai 400 018\n")
    r_meta.font.size = Pt(10)
    r_meta.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(12)
    
    # Orientation Note
    add_callout_box("Document Orientation & Cognitive Transformation Architecture", 
                    "This document takes the complete original financial disclosures of HDFC Bank Limited for Q1 FY 2026-27 "
                    "and restructures them according to a 9-step cognitive progression model. Every technical term is pre-explained "
                    "with familiar real-life analogies, mechanical explanations, and clear structural breakdowns before presenting "
                    "the exact source data. Zero source information has been omitted.",
                    border_color="003366", bg_color="F0F4F8")
    
    # ---------------------------------------------------------
    # TABLE OF CONTENTS / MAP
    # ---------------------------------------------------------
    h_toc = doc.add_heading("Master Navigation & Table of Contents", level=1)
    h_toc.paragraph_format.space_before = Pt(16)
    
    toc_text = (
        "Part I: Cognitive Learning Architecture & Core Concept Modules (Concepts 1 to 24)\n"
        "  • Concept 1: Standalone vs. Consolidated Results\n"
        "  • Concept 2: Interest Earned vs. Interest Expended\n"
        "  • Concept 3: Other Income & Non-Fund Based Operations\n"
        "  • Concept 4: Operating Profit, Provisions, and Net Profit\n"
        "  • Concept 5: Discretionary Floating Provisions\n"
        "  • Concept 6: Capital Adequacy Ratio (CAR)\n"
        "  • Concept 7: Earnings Per Share (EPS) — Basic & Diluted\n"
        "  • Concept 8: Non-Performing Assets (NPAs) — Gross vs. Net\n"
        "  • Concept 9: Return on Assets (ROA)\n"
        "  • Concept 10: Financial Leverage — Debt-Equity & Total Debt to Total Assets\n"
        "  • Concept 11: Business Segment Reporting\n"
        "  • Concept 12: Limited Review vs. Full Statutory Audit\n"
        "  • Concept 13: Bonus Shares & Retrospective Earnings Adjustment\n"
        "  • Concept 14: Employee Stock Option Plan (ESOP) Allotments\n"
        "  • Concept 15: Stressed Loan Transfers & Asset Reconstruction Companies (ARCs)\n"
        "  • Concept 16: Security Receipts (SRs) & Recovery Ratings\n"
        "  • Concept 17: Infrastructure Project Finance & DCCO\n"
        "  • Concept 18: Initial Public Offering (IPO) & Offer for Sale (OFS) Divestment\n"
        "  • Concept 19: Preferential Share Allotment\n"
        "  • Concept 20: Tax Provision Write-backs & Tax Adjustments\n"
        "  • Concept 21: Corporate Governance Review of Director Resignation\n"
        "  • Concept 22: Regulatory Directives & DIFC Overseas Branch Status\n"
        "  • Concept 23: Basel III Framework & Pillar 3 Disclosures\n"
        "  • Concept 24: Actuarial Liabilities — Life Insurance Policies & Non-Life IBNR/IBNER Reserves\n\n"
        "Part II: Full Standalone Financial Statements & Detailed Disclosures (Tables 1 to 6)\n"
        "Part III: Standalone Independent Auditors' Limited Review Report\n"
        "Part IV: Full Consolidated Financial Statements & Group Disclosures (Tables 7 to 9)\n"
        "Part V: Consolidated Independent Auditors' Review Report & Annexure of Consolidated Entities (Table 10)"
    )
    p_toc = doc.add_paragraph(toc_text)
    p_toc.paragraph_format.space_after = Pt(16)
    
    # ---------------------------------------------------------
    # PART I: COGNITIVE LEARNING CONCEPTS (1 to 24)
    # ---------------------------------------------------------
    doc.add_heading("Part I: Cognitive Learning Architecture & Core Concept Modules", level=1)
    
    # Concept 1
    add_concept_block(
        doc, 1, "Standalone vs. Consolidated Results",
        familiar_idea="Think of a parent running a sole-proprietorship store vs. running a family group of businesses including a bakery, a delivery service, and an insurance agency.",
        real_life_eg="If you evaluate just the main store's sales, that is 'Standalone'. If you add up the main store plus all the family-owned businesses, eliminating transactions between each other, that is 'Consolidated'.",
        mechanism="Standalone tracks only the single legal banking entity (HDFC Bank Ltd). Consolidated combines HDFC Bank Ltd with its 17 subsidiaries (like HDFC Life, HDFC ERGO, HDFC AMC, HDB Financial Services) into a single master financial statement, stripping out internal transactions.",
        purpose="To show investors both how the core bank is performing by itself (Standalone) and how the entire corporate umbrella is performing as a whole (Consolidated).",
        tech_term="Standalone Financial Results vs. Consolidated Financial Results",
        structure="1. Parent Entity (HDFC Bank Ltd)\n2. Operating Subsidiaries (Insurance, Asset Management, Securities)\n3. Consolidation Adjustments (Inter-segment revenue elimination).",
        relationship="Establishes the boundary for every table in the report. Tables 1-6 represent Standalone; Tables 7-10 represent Consolidated.",
        practical_meaning="Allows depositors to judge the bank's core safety and allows shareholders to value the entire corporate group.",
        source_detail="Standalone Total Assets: ₹43,97,461.28 crore; Consolidated Total Assets: ₹49,71,473.66 crore (as of June 30, 2026)."
    )
    
    # Concept 2
    add_concept_block(
        doc, 2, "Interest Earned vs. Interest Expended",
        familiar_idea="Think of a fruit trader buying apples from farmers at ₹50 per kg and selling them to shoppers at ₹80 per kg.",
        real_life_eg="A bank collects money from depositors and pays them 5% interest (Interest Expended). It lends that money to home buyers at 9% interest (Interest Earned). The difference is its main profit engine.",
        mechanism="Interest Earned includes interest on loans/advances, income on government bond investments, and RBI balances. Interest Expended is the interest paid on customer deposits and wholesale bank borrowings.",
        purpose="Measures the efficiency of the bank's core money-lending engine.",
        tech_term="Interest Earned (Item 1) and Interest Expended (Item 4)",
        structure="Interest Earned: a) Advances/Bills, b) Investments, c) RBI/Inter-bank balances, d) Others.\nInterest Expended: Interest paid on deposits and borrowings.",
        relationship="Interest Earned minus Interest Expended yields Net Interest Income (NII), which feeds directly into Operating Profit.",
        practical_meaning="Shows whether the bank is effectively earning more on its loans than it pays to attract money.",
        source_detail="Standalone Q1 FY27: Interest Earned = ₹79,362.78 crore; Interest Expended = ₹45,828.83 crore.\nConsolidated Q1 FY27: Interest Earned = ₹90,575.33 crore; Interest Expended = ₹47,625.63 crore."
    )
    
    # Concept 3
    add_concept_block(
        doc, 3, "Other Income & Non-Fund Based Operations",
        familiar_idea="Think of a car dealership earning money not just from selling cars, but from processing loan applications, insurance commissions, and servicing fees.",
        real_life_eg="When HDFC Bank charges a credit card fee, converts foreign currency for a traveler, or sells insurance policies, it earns non-interest fee income.",
        mechanism="Represents revenue generated without directly lending money. Includes processing fees, foreign exchange fees, investment profits, dividend from subsidiaries, written-off loan recoveries, and insurance premiums in consolidated results.",
        purpose="Diversifies bank revenue so it does not rely solely on interest rates.",
        tech_term="Other Income (Item 2)",
        structure="1. Processing fees & commissions\n2. Forex & derivative earnings\n3. Profit/loss on investment sales\n4. Insurance premium revenue (Consolidated)\n5. Loan recoveries.",
        relationship="Added to Interest Earned to calculate Total Income (Item 3).",
        practical_meaning="A high Other Income ratio shows a strong franchise capable of generating steady fee income regardless of rate cycles.",
        source_detail="Standalone Q1 FY27 Other Income: ₹12,821.60 crore. Consolidated Q1 FY27 Other Income: ₹42,535.03 crore (includes ₹18,353.92 crore insurance premium income)."
    )

    # Concept 4
    add_concept_block(
        doc, 4, "Operating Profit, Provisions, and Net Profit",
        familiar_idea="Think of running a restaurant: Total Sales minus Food & Staff Costs gives cash generated (Operating Profit). You then set aside money for broken dishes or unpaid bills (Provisions) before calculating final profit (Net Profit).",
        real_life_eg="HDFC Bank generates ₹28,168.06 crore in raw operating surplus. It sets aside ₹3,059.76 crore for bad loan risks, pays ₹6,048.58 crore in income tax, leaving ₹19,059.72 crore as final Net Profit.",
        mechanism="Total Income minus Operating Expenses equals Operating Profit. Subtracting Provisions for bad loans and Tax Expenses yields Net Profit.",
        purpose="Separates operational performance from risk provisioning and taxation.",
        tech_term="Operating Profit before Provisions (Item 7) vs. Provisions (Item 8) vs. Net Profit (Item 12/14)",
        structure="Total Income -> Less: Operating Expenses -> Operating Profit -> Less: Provisions -> PBT -> Less: Tax -> Net Profit.",
        relationship="Connecting bridge between gross operational performance and bottom-line shareholder earnings.",
        practical_meaning="Shows whether profit growth comes from good business operations or merely changing provision levels.",
        source_detail="Standalone Q1 FY27: Operating Profit = ₹28,168.06 crore; Provisions = ₹3,059.76 crore; Tax = ₹6,048.58 crore; Net Profit = ₹19,059.72 crore."
    )

    # Concept 5
    add_concept_block(
        doc, 5, "Discretionary Floating Provisions",
        familiar_idea="Think of putting extra cash in a emergency cookie jar during good months, even if no bills are due, just in case a rainy day comes later.",
        real_life_eg="HDFC Bank's board voluntarily set aside ₹9,000.00 crore as a general safety buffer in FY26, over and above mandatory loan loss rules.",
        mechanism="Provisions made without being tied to specific bad loans. They sit on the balance sheet as an extra shock absorber that can be drawn down during economic stress with regulator/board approval.",
        purpose="Strengthens balance sheet resilience against unexpected systemic crises.",
        tech_term="Floating Provisions (Note 8)",
        structure="Board-approved discretionary reserve bucket deducted from income and held under liabilities.",
        relationship="Adjusts segment liabilities and segment results for Q1 FY26 and FY26 comparative periods.",
        practical_meaning="Indicates conservative financial management and high balance sheet fortitude.",
        source_detail="Note 8: Floating provision of ₹9,000.00 crore created during Q1 ended June 30, 2025 and year ended March 31, 2026."
    )

    # Concept 6
    add_concept_block(
        doc, 6, "Capital Adequacy Ratio (CAR)",
        familiar_idea="Think of a ship's buoyancy tank requirement: for every 100 kg of cargo carried, the ship must have at least 15 kg of airtight flotation reserves to prevent sinking in a storm.",
        real_life_eg="The RBI mandates banks to keep a minimum capital cushion against loans. HDFC Bank holds 19.57% capital relative to its risk-weighted loans, far above the regulatory minimum (~11.5%).",
        mechanism="Calculated as (Tier 1 Capital + Tier 2 Capital) divided by Risk-Weighted Assets. Higher ratios mean greater ability to absorb loan losses.",
        purpose="Prevents bank failures and protects depositor money.",
        tech_term="Capital Adequacy Ratio (Analytical Ratio 17(ii))",
        structure="1. Tier 1 Capital (Equity + Free Reserves)\n2. Tier 2 Capital (Subordinated Debt + General Provisions)\n3. Risk-Weighted Assets (Loans weighted by default risk).",
        relationship="Governs how fast the bank can expand its loan book without raising new capital.",
        practical_meaning="Confirms the bank is rock-solid and highly capable of withstanding economic shocks.",
        source_detail="Standalone CAR as of June 30, 2026: 19.57% (vs 19.71% as of March 31, 2026 and 19.88% as of June 30, 2025)."
    )

    # Concept 7
    add_concept_block(
        doc, 7, "Earnings Per Share (EPS) — Basic & Diluted",
        familiar_idea="Think of dividing a birthday cake among guests: if 10 guests are present, each gets 1/10th. If 2 more people have invitation vouchers that can be turned into plates, each potential share becomes slightly smaller.",
        real_life_eg="HDFC Bank earned ₹19,059.72 crore. Divided by existing shares, Basic EPS is ₹12.38. Accounting for pending employee stock options, Diluted EPS is ₹12.35.",
        mechanism="Basic EPS = Net Profit / Weighted Average Existing Shares. Diluted EPS = Net Profit / (Existing Shares + Potential Shares from ESOPs/Convertibles).",
        purpose="Measures how much net profit belongs to each individual equity share.",
        tech_term="Basic EPS and Diluted EPS (Analytical Ratio 17(iii) & Note 6)",
        structure="Basic EPS (Actual shares) vs. Diluted EPS (Includes ESOP options). All prior figures restated for 1:1 bonus share issue.",
        relationship="Directly drives stock valuation and price-to-earnings (P/E) ratios.",
        practical_meaning="Helps retail investors understand the exact quarterly earning power behind each share they own.",
        source_detail="Standalone Q1 FY27: Basic EPS = ₹12.38, Diluted EPS = ₹12.35 (Face Value ₹1/-). Consolidated Q1 FY27: Basic EPS = ₹12.50, Diluted EPS = ₹12.47."
    )

    # Concept 8
    add_concept_block(
        doc, 8, "Non-Performing Assets (NPAs) — Gross vs. Net",
        familiar_idea="Think of an apartment landlord: Gross NPA is the total rent overdue by 90+ days. Net NPA is overdue rent after subtracting the security deposit money you locked away to cover missing rent.",
        real_life_eg="HDFC Bank has ₹35,846.35 crore in overdue loans (Gross NPA = 1.17%). After setting aside provisions, bad loans uncovered by reserves are ₹12,357.27 crore (Net NPA = 0.41%).",
        mechanism="Loans unpaid for over 90 days become Gross NPAs. When the bank sets aside specific provisions against them, the remaining uncovered amount is Net NPA.",
        purpose="Tracks loan quality and loan loss protection strength.",
        tech_term="Gross NPAs, Net NPAs, % of Gross NPAs to Gross Advances, % of Net NPAs to Net Advances (Analytical Ratio 17(iv))",
        structure="1. Gross NPAs (Total defaulted loans)\n2. Specific Provisions (Deducted reserves)\n3. Net NPAs (Unhedged defaulted loans).",
        relationship="Determines quarterly provision costs in the P&L statement.",
        practical_meaning="HDFC Bank's Net NPA of 0.41% indicates world-class asset quality and exceptional risk management.",
        source_detail="As of June 30, 2026: Gross NPAs = ₹35,846.35 crore (1.17%); Net NPAs = ₹12,357.27 crore (0.41%)."
    )

    # Concept 9
    add_concept_block(
        doc, 9, "Return on Assets (ROA)",
        familiar_idea="Think of a taxi owner with a vehicle worth ₹10,00,000 who earns ₹20,000 net profit per month. The monthly return on that vehicle asset is 2%.",
        real_life_eg="HDFC Bank manages ₹43,97,461.28 crore in total assets and generates ₹19,059.72 crore net profit in Q1, yielding an un-annualized ROA of 0.46%.",
        mechanism="Calculated as Net Profit divided by Average Total Assets for the period.",
        purpose="Measures how efficiently bank management uses its total asset base to generate profit.",
        tech_term="Return on Assets (Average) - Not Annualized (Analytical Ratio 17(v))",
        structure="Numerator: Net Profit after tax; Denominator: Average Total Assets.",
        relationship="Combines balance sheet size with P&L profitability into a single efficiency benchmark.",
        practical_meaning="ROA above 0.45% per quarter (~1.8%-1.9% annualized) is considered elite for mega-scale global banks.",
        source_detail="Standalone Q1 FY27 ROA: 0.46% (not annualized); FY26 Full Year ROA: 1.94%."
    )

    # Concept 10
    add_concept_block(
        doc, 10, "Financial Leverage — Debt-Equity & Total Debt to Total Assets",
        familiar_idea="Think of buying a house: if you put down ₹20 lakh of your own money and borrow ₹80 lakh from a lender, your debt-to-equity ratio is 4.0, and debt-to-total-assets is 80%.",
        real_life_eg="HDFC Bank's long-term borrowings relative to equity net worth give a Debt-Equity ratio of 0.56, while total borrowings make up 10.50% of total assets.",
        mechanism="Debt-Equity = Borrowings (>1 yr maturity) / Net Worth. Total Debts to Total Assets = Total Borrowings / Total Assets.",
        purpose="Measures reliance on wholesale borrowed money versus customer deposits and owner equity.",
        tech_term="Debt Equity Ratio & Total Debts to Total Assets (Analytical Ratios 17(ix) & (x))",
        structure="Debt defined as borrowings with residual maturity > 1 year. Total debts include all bank borrowings.",
        relationship="Indicates liability structure stability and refinancing sensitivity.",
        practical_meaning="Shows HDFC Bank relies primarily on sticky customer deposits rather than risky short-term borrowings.",
        source_detail="As of June 30, 2026: Debt Equity Ratio = 0.56; Total Debts to Total Assets = 10.50%."
    )

    # Concept 11
    add_concept_block(
        doc, 11, "Business Segment Reporting",
        familiar_idea="Think of a mega department store analyzing sales separately for Clothing, Electronics, Groceries, and Financial Services.",
        real_life_eg="HDFC Bank reports its financial health across Treasury, Retail Banking (Digital vs. Non-Digital), Wholesale Banking, Other Banking Operations, and Insurance.",
        mechanism="Identifies revenue, profit, assets, and liabilities for each distinct operating division based on customer profiles and RBI guidelines.",
        purpose="Provides transparency on which business lines are driving growth or consuming capital.",
        tech_term="Segment Information (Accounting Standard 17 / RBI Guidelines)",
        structure="1. Treasury\n2. Retail Banking (Digital Units vs. Non-Digital)\n3. Wholesale Banking\n4. Other Banking\n5. Insurance Business (Consolidated).",
        relationship="Deconstructs overall P&L (Items 3 & 10) and Balance Sheet into operational engines.",
        practical_meaning="Helps analysts see that Retail and Wholesale Banking are the massive profit drivers of the bank.",
        source_detail="Standalone Q1 FY27 Segment PBT: Retail Non-Digital = ₹10,131.25 cr; Wholesale = ₹10,364.04 cr; Treasury = ₹2,406.59 cr."
    )

    # Concept 12
    add_concept_block(
        doc, 12, "Limited Review vs. Full Statutory Audit",
        familiar_idea="Think of a routine health check-up with basic blood tests (Limited Review) vs. a full 3-day comprehensive hospital diagnostic audit (Statutory Audit).",
        real_life_eg="For quarterly results, auditors conduct analytical reviews and management inquiries under SRE 2410 (Limited Review). For full-year results, they perform full audits.",
        mechanism="Limited Review provides negative assurance ('nothing came to our attention'). Audit provides positive assurance ('statements present a true and fair view').",
        purpose="Ensures quarterly regulatory compliance without incurring the enormous time cost of a full audit every 90 days.",
        tech_term="Limited Review Report pursuant to SEBI Regulation 33 & 52",
        structure="Auditor engagement under SRE 2410 by joint statutory auditors B S R & Co. LLP and Batliboi & Purohit.",
        relationship="Validates all numbers in Tables 1-10 before public submission to stock exchanges.",
        practical_meaning="Provides regulatory confidence that financial statements contain no material misstatements.",
        source_detail="Signed on July 18, 2026 with unmodified (clean) review conclusions for both Standalone and Consolidated results."
    )

    # Concept 13
    add_concept_block(
        doc, 13, "Bonus Shares & Retrospective Earnings Adjustment",
        familiar_idea="Think of slicing a 1-pound pizza into 8 slices instead of 4 slices: you have more slices, but the total pizza weight remains unchanged.",
        real_life_eg="HDFC Bank issued 1 bonus share for every 1 existing share on August 28, 2025. Total share count doubled, so historical EPS figures were halved retrospectively to make comparisons fair.",
        mechanism="7,67,70,39,761 equity shares were allotted by capitalizing Share Premium. Historical per-share metrics are restated retrospectively under AS 20.",
        purpose="Improves stock liquidity and rewards long-term shareholders without altering total equity capitalization.",
        tech_term="Bonus Shares Issuance in 1:1 Ratio (Note 6)",
        structure="Capitalization of Share Premium -> Doubling of Equity Share Count -> Retrospective EPS restatement.",
        relationship="Adjusts Share Capital (Item 15) and historical EPS metrics (Item 17(iii)).",
        practical_meaning="Explains why share capital doubled to ₹1,540.13 crore while historical EPS figures were adjusted.",
        source_detail="Note 6: Allotted 7,67,70,39,761 bonus equity shares of ₹1/- each on August 28, 2025."
    )

    # Concept 14
    add_concept_block(
        doc, 14, "Employee Stock Option Plan (ESOP) Allotments",
        familiar_idea="Think of a company rewarding star employees with discount vouchers to buy company stock after completing 3 years of service.",
        real_life_eg="During Q1 FY27, HDFC Bank employees exercised stock options, resulting in the issuance of 79,59,164 new equity shares of face value ₹1/- each.",
        mechanism="Employees exercise vested stock options at pre-agreed exercise prices, increasing share capital and share premium.",
        purpose="Aligns employee incentive with long-term shareholder value creation.",
        tech_term="Allotment of Equity Shares under ESOP Schemes (Note 7)",
        structure="Grant -> Vesting -> Exercise -> Share Allotment -> Paid-Up Capital Increase.",
        relationship="Increases Paid-up Equity Share Capital from ₹1,539.34 crore to ₹1,540.13 crore during Q1 FY27.",
        practical_meaning="Shows routine share issuance to bank workforce, causing minor share dilution reflected in Diluted EPS.",
        source_detail="Note 7: Allotted 79,59,164 equity shares of ₹1/- each during Q1 ended June 30, 2026 upon option exercises."
    )

    # Concept 15
    add_concept_block(
        doc, 15, "Stressed Loan Transfers & Asset Reconstruction Companies (ARCs)",
        familiar_idea="Think of a retail store selling unpaid overdue customer tabs to a specialized collection agency for 40 cents on the dollar to clean up its books.",
        real_life_eg="HDFC Bank transferred defaulted NPAs with ₹7.43 crore principal outstanding to ARCs to focus its energy on regular banking business.",
        mechanism="Defaulted loans are removed from bank books and assigned to licensed ARCs in exchange for cash and/or Security Receipts.",
        purpose="Cleans non-performing assets off bank balance sheets and accelerates debt recovery.",
        tech_term="Details of Non-Performing Assets Transferred (Note 9(i))",
        structure="Transfer of NPAs to ARCs / Permitted Transferees under RBI Master Directions 2025.",
        relationship="Reduces Gross NPAs and affects provisioning recoveries.",
        practical_meaning="Demonstrates proactive management in purging bad debts through institutional recovery channels.",
        source_detail="Note 9(i): Transferred NPA accounts with ₹7.43 crore aggregate principal outstanding to ARCs during Q1 FY27."
    )

    # Concept 16
    add_concept_block(
        doc, 16, "Security Receipts (SRs) & Recovery Ratings",
        familiar_idea="Think of a pawn shop ticket: when you transfer a bad loan to a recovery specialist, they give you an IOU ticket (SR) whose final cash value depends on how much money they recover.",
        real_life_eg="HDFC Bank holds ₹1,049.19 crore gross value in Security Receipts issued by ARCs, rated by credit agencies like ICRA, CRISIL, and India Ratings based on recovery prospects.",
        mechanism="SRs are financial instruments issued by ARCs representing claims on cash flows from bad loan recoveries. Independent rating agencies assign recovery grades (RR1+ to RR5).",
        purpose="Allows banks to retain economic upside in bad loan recoveries handled by specialized ARCs.",
        tech_term="Security Receipts Outstanding & Recovery Ratings (Note 9(v))",
        structure="Ratings Breakdown: RR1+ (>150% recovery), RR1 (100-150%), RR2 (75-100%), RR4 (25-50%), RR5 (<25%), Unrated.",
        relationship="Carried under Investments asset category; provisions required if recovery ratings downgrade.",
        practical_meaning="Provides transparent disclosure on the realizable value of bad debts held via recovery trusts.",
        source_detail="Note 9(v): Outstanding SRs Gross Value = ₹1,049.19 crore (RR1 = ₹111.65 cr, RR5 = ₹155.08 cr, Unrated = ₹719.85 cr)."
    )

    # Concept 17
    add_concept_block(
        doc, 17, "Infrastructure Project Finance & DCCO",
        familiar_idea="Think of building a toll bridge: no income is generated during construction. The date the first car pays a toll and commercial operations begin is the crucial DCCO milestone.",
        real_life_eg="HDFC Bank finances 440 ongoing infrastructure projects worth ₹20,785.14 crore. If a project suffers delays, extending its commercial start date (DCCO) requires formal resolution plans.",
        mechanism="Project loans are tracked against their scheduled Date of Commencement of Commercial Operations (DCCO). If DCCO is extended, RBI rules require strict monitoring or restructuring provisions.",
        purpose="Monitors high-risk, long-gestation infrastructure loans to catch construction delays early.",
        tech_term="Project Finance Disclosures & Commercial Operations Start Date (DCCO) (Note 10)",
        structure="1. Projects Under Implementation\n2. DCCO Achieved\n3. DCCO Extension Invoked\n4. Resolution Plans Implemented/Failed.",
        relationship="Governs credit risk provisioning in wholesale project lending books.",
        practical_meaning="Shows HDFC Bank's active exposure and risk oversight in major infrastructure construction projects.",
        source_detail="Note 10: 440 project accounts outstanding (₹20,785.14 crore); 75 accounts achieved DCCO in Q1 (₹4,442.26 crore); 35 accounts invoked DCCO extension."
    )

    # Concept 18
    add_concept_block(
        doc, 18, "Initial Public Offering (IPO) & Offer for Sale (OFS) Divestment",
        familiar_idea="Think of an investor selling 20% of their private company shares to public stock market buyers to unlock cash gains while remaining the majority owner.",
        real_life_eg="HDFC Bank sold 13.51 crore shares of subsidiary HDB Financial Services (HDBFS) at ₹740 per share, realizing ₹10,000 crore cash consideration and a net pre-tax gain of ₹9,128.40 crore.",
        mechanism="IPO combining Fresh Issue (cash to subsidiary) and Offer for Sale (OFS - cash to parent). P&L recognizes gain on sale of investment.",
        purpose="Unlocks value of subsidiary businesses and monetizes holdings for bank capital.",
        tech_term="Initial Public Offering (IPO) & Offer for Sale (OFS) of Subsidiary Shares (Note 12 Standalone / Note 9 Consolidated)",
        structure="13,51,35,135 shares divested at ₹740/share -> Pre-tax Gain: ₹9,128.40 cr (Standalone) / ₹6,949.27 cr (Consolidated net of asset share).",
        relationship="Boosted Q1 FY26 Other Income (Item 2) significantly in comparative historical periods.",
        practical_meaning="Demonstrates HDFC Bank's ability to incubate billion-dollar financial subsidiaries and monetize equity value.",
        source_detail="Note 12 (Standalone): OFS divestment of 13,51,35,135 shares of HDBFS at ₹740/share on June 25, 2025."
    )

    # Concept 19
    add_concept_block(
        doc, 19, "Preferential Share Allotment",
        familiar_idea="Think of buying additional shares directly from a company at a fixed negotiated price to increase your ownership control, without going through open market trading.",
        real_life_eg="On June 16, 2026, HDFC Bank invested ₹1,000.00 crore to buy 1.45 crore shares of HDFC Life Insurance on a preferential basis, maintaining a controlling 50.54% stake.",
        mechanism="Issuance of new equity shares directly to a specific strategic investor approved by shareholder resolution under Companies Act Section 62.",
        purpose="Injects capital into the insurance subsidiary while securing majority parent control.",
        tech_term="Preferential Issue Allotment of Shares (Note 13 Standalone / Note 10 Consolidated)",
        structure="Allotment of 1,45,23,906 equity shares of HDFC Life for ₹1,000.00 crore -> Stake fixed at 50.54%.",
        relationship="Increases Investments in Subsidiaries on Standalone Balance Sheet and Minority Interest on Consolidated Balance Sheet.",
        practical_meaning="Confirms HDFC Bank's strategic commitment to remaining the dominant controlling parent of HDFC Life.",
        source_detail="Note 13: Allotted 1,45,23,906 shares of HDFC Life on June 16, 2026 for ₹1,000.00 crore; Shareholding = 50.54%."
    )

    # Concept 20
    add_concept_block(
        doc, 20, "Tax Provision Write-backs & Tax Adjustments",
        familiar_idea="Think of receiving an income tax refund check from the government because an old audit appeal was decided in your favor.",
        real_life_eg="In Q1 FY26, HDFC Bank received favorable tax court orders, allowing it to write back ₹1,144.46 crore of old tax provisions no longer required.",
        mechanism="Reversal of over-provided tax liabilities from past years credited against current P&L Tax Expense under AS 12.",
        purpose="Adjusts tax reserves to match legally finalized tax liabilities.",
        tech_term="Write-back of Tax Provision Pursuant to Favourable Orders (Note 14 Standalone)",
        structure="Favourable appellate order -> Assessment of over-provision -> Credit to Tax Expense (Item 11).",
        relationship="Reduced Tax Expense and boosted Net Profit in Q1 FY26 comparative period.",
        practical_meaning="Reflects successful legal tax appeals and prudent historical tax provisioning.",
        source_detail="Note 14: Tax provision for Q1 FY26 / FY26 is net of ₹1,144.46 crore write-back following favorable orders."
    )

    # Concept 21
    add_concept_block(
        doc, 21, "Corporate Governance Review of Director Resignation",
        familiar_idea="Think of a board hiring independent external auditors to investigate allegations made in an outgoing executive's resignation letter to ensure total transparency.",
        real_life_eg="Following the resignation of former Part-time Chairman Mr. Atanu Chakraborty, external domestic and international law firms reviewed the claims and found them completely unsubstantiated.",
        mechanism="Independent legal review examining corporate records and conducting witness interviews to verify governance integrity.",
        purpose="Upholds institutional trust, stock exchange disclosures, and regulatory compliance.",
        tech_term="External Legal Review of Resignation Statements (Note 15 Standalone / Note 11 Consolidated)",
        structure="Stock exchange disclosure (Mar 24, 2026) -> External legal investigation -> Disclosure of conclusion (June 26, 2026) -> No financial impact.",
        relationship="Validates board governance integrity; zero impact on P&L or balance sheet stability.",
        practical_meaning="Reassures institutional investors that HDFC Bank maintains flawless corporate governance practices.",
        source_detail="Note 15: External law firms concluded on June 26, 2026 that statements in Mr. Chakraborty's letter were unsubstantiated by records."
    )

    # Concept 22
    add_concept_block(
        doc, 22, "Regulatory Directives & DIFC Overseas Branch Status",
        familiar_idea="Think of a restaurant branch receiving a local municipal health inspector order asking it to pause enrolling new catering clients while existing dining tables run normally.",
        real_life_eg="HDFC Bank's Dubai International Financial Centre (DIFC) branch received a notice from DFSA prohibiting new client onboarding for specified services. Existing clients remain fully serviced.",
        mechanism="Overseas financial authority enforcement directive restricting specific business activities pending compliance remediation.",
        purpose="Ensures strict adherence to international financial regulatory frameworks.",
        tech_term="Dubai Financial Services Authority (DFSA) Decision Notice (Note 16 Standalone / Note 12 Consolidated)",
        structure="DFSA Notice (Sept 25, 2025) -> Restriction on new client solicitation -> Continuation of existing client service -> Compliance actions under way.",
        relationship="Disclosed under contingent regulatory risks; financial impact rated immaterial to overall bank operations.",
        practical_meaning="Shows complete regulatory transparency regarding international branch compliance.",
        source_detail="Note 16: DIFC Branch business is immaterial to bank financial position; zero material impact expected on overall operations."
    )

    # Concept 23
    add_concept_block(
        doc, 23, "Basel III Framework & Pillar 3 Disclosures",
        familiar_idea="Think of a public health dashboard where a hospital publishes its daily ICU bed availability, oxygen reserves, and nurse-to-patient ratios for public audit.",
        real_life_eg="HDFC Bank publishes detailed quarterly Basel III metrics online—including Leverage Ratio, Liquidity Coverage Ratio (LCR), and Net Stable Funding Ratio (NSFR).",
        mechanism="International banking safety regulations requiring consolidated disclosures of liquidity buffers and leverage safety margins.",
        purpose="Ensures market discipline and lets global rating agencies verify bank liquidity resilience.",
        tech_term="Consolidated Pillar 3 Disclosures under Basel III (Note 14 Consolidated)",
        structure="1. Leverage Ratio\n2. Liquidity Coverage Ratio (LCR)\n3. Net Stable Funding Ratio (NSFR).\nAvailable at www.hdfc.bank.in.",
        relationship="Complements Capital Adequacy Ratios (CAR) by measuring short-term and long-term liquidity strength.",
        practical_meaning="Confirms HDFC Bank holds abundant liquid cash assets to survive severe financial market freezes.",
        source_detail="Note 14 (Consolidated): Pillar 3 disclosures made available on bank website pursuant to RBI directions."
    )

    # Concept 24
    add_concept_block(
        doc, 24, "Actuarial Liabilities — Life Insurance Policies & Non-Life IBNR/IBNER Reserves",
        familiar_idea="Think of a home insurance firm estimating how many un-reported storm damage claims will arrive over the next 30 days based on weather statistics, and reserving cash for them today.",
        real_life_eg="Appointed Actuaries at HDFC Life and HDFC ERGO certify mathematical models calculating policy liabilities and reserves for incurred-but-not-yet-reported accident claims (IBNR).",
        mechanism="Certified actuarial valuation estimating future policyholder payouts, claims reserves, and Premium Deficiency Reserves (PDR) under IRDAI norms.",
        purpose="Ensures insurance subsidiaries maintain 100% adequate cash reserves to pay all future insurance claims.",
        tech_term="Actuarial Valuation of Life Liabilities & Non-Life IBNR / IBNER Reserves (Consolidated Auditor Report Notes 10 & 11)",
        structure="1. HDFC Life Policy Liabilities (Certified by Appointed Actuary)\n2. HDFC ERGO IBNR & IBNER Reserves (Certified by Appointed Actuary).",
        relationship="Determines Policyholders' Funds (₹3,82,135.20 crore) and Insurance Expenses in Consolidated statements.",
        practical_meaning="Guarantees insurance policyholders that claim reserves are independently validated by statutory actuaries.",
        source_detail="Consolidated Audit Report Notes 10 & 11: Statutory auditors rely on Appointed Actuaries' certificates for life liabilities and non-life IBNR/IBNER reserves."
    )

    doc.add_page_break()

    # ---------------------------------------------------------
    # PART II: FULL STANDALONE FINANCIAL STATEMENTS (TABLES 1-6)
    # ---------------------------------------------------------
    doc.add_heading("Part II: Standalone Financial Statements & Detailed Disclosures", level=1)
    
    # Table 1: Standalone P&L
    doc.add_heading("Table 1: Unaudited Standalone Financial Results for the Quarter Ended June 30, 2026 (₹ in crore)", level=2)
    headers_t1 = ["Particulars", "30.06.2026 (Unaudited)", "31.03.2026 (Audited Note 5)", "30.06.2025 (Unaudited)", "31.03.2026 (Audited Year)"]
    rows_t1 = [
        ["1. Interest earned (a)+(b)+(c)+(d)", "79,362.78", "76,610.02", "77,470.20", "3,07,522.08"],
        ["  a) Interest/discount on advances/bills", "61,953.87", "60,351.21", "60,192.64", "2,39,762.46"],
        ["  b) Income on investments", "14,272.21", "13,923.99", "15,070.08", "58,945.38"],
        ["  c) Interest on RBI balances & inter-bank funds", "1,365.28", "879.41", "670.17", "2,674.70"],
        ["  d) Others", "1,771.42", "1,455.41", "1,537.31", "6,139.54"],
        ["2. Other Income (Refer note 12)", "12,821.60", "13,198.88", "21,729.83", "62,532.57"],
        ["3. Total Income (1)+(2)", "92,184.38", "89,808.90", "99,200.03", "3,70,054.65"],
        ["4. Interest expended", "45,828.83", "43,528.45", "46,032.23", "1,78,836.04"],
        ["5. Operating expenses (i)+(ii)", "18,187.49", "18,477.53", "17,433.84", "72,660.33"],
        ["  i) Employees cost", "6,414.83", "6,227.72", "6,157.97", "26,050.15"],
        ["  ii) Other operating expenses", "11,772.66", "12,249.81", "11,275.87", "46,610.18"],
        ["6. Total Expenditure (4)+(5) (excl. provisions)", "64,016.32", "62,005.98", "63,466.07", "2,51,496.37"],
        ["7. Operating Profit before provisions (3)-(6)", "28,168.06", "27,802.92", "35,733.96", "1,18,558.28"],
        ["8. Provisions & Contingencies (Refer note 8)", "3,059.76", "2,609.57", "14,441.63", "23,389.59"],
        ["9. Exceptional items", "-", "-", "-", "-"],
        ["10. Profit from ordinary activities before tax (7)-(8)", "25,108.30", "25,193.35", "21,292.33", "95,168.69"],
        ["11. Tax Expense (Refer note 14)", "6,048.58", "5,972.30", "3,137.12", "20,497.40"],
        ["12. Net Profit from ordinary activities after tax (10)-(11)", "19,059.72", "19,221.05", "18,155.21", "74,671.29"],
        ["13. Extraordinary items (net of tax)", "-", "-", "-", "-"],
        ["14. Net Profit for the period (12)-(13)", "19,059.72", "19,221.05", "18,155.21", "74,671.29"],
        ["15. Paid up equity share capital (Face Value ₹1/-)", "1,540.13", "1,539.34", "766.79", "1,539.34"],
        ["16. Reserves excluding revaluation reserves", "-", "5,56,816.45", "-", "5,56,816.45"],
        ["17. Analytical Ratios & Disclosures:", "", "", "", ""],
        ["  (i) Govt of India Shareholding", "Nil", "Nil", "Nil", "Nil"],
        ["  (ii) Capital Adequacy Ratio (%)", "19.57%", "19.71%", "19.88%", "19.71%"],
        ["  (iii) Earnings Per Share (EPS) (₹):", "", "", "", ""],
        ["    (a) Basic EPS (not annualized)", "12.38", "12.49", "11.86", "48.62"],
        ["    (b) Diluted EPS (not annualized)", "12.35", "12.45", "11.79", "48.40"],
        ["  (iv) NPA Ratios:", "", "", "", ""],
        ["    (a) Gross NPAs (₹ in crore)", "35,846.35", "34,061.19", "37,040.80", "34,061.19"],
        ["    (b) Net NPAs (₹ in crore)", "12,357.27", "11,169.54", "12,275.99", "11,169.54"],
        ["    (c) % Gross NPAs to Gross Advances", "1.17%", "1.15%", "1.40%", "1.15%"],
        ["    (d) % Net NPAs to Net Advances", "0.41%", "0.38%", "0.47%", "0.38%"],
        ["  (v) Return on Assets (average - not annualized)", "0.46%", "0.48%", "0.48%", "1.94%"],
        ["  (vi) Net Worth (₹ in crore)", "5,66,201.13", "5,46,325.46", "5,08,803.89", "5,46,325.46"],
        ["  (vii) Outstanding Redeemable Preference Shares", "-", "-", "-", "-"],
        ["  (viii) Capital Redemption Reserve", "-", "-", "-", "-"],
        ["  (ix) Debt Equity Ratio", "0.56", "0.53", "0.61", "0.53"],
        ["  (x) Total Debts to Total Assets (%)", "10.50%", "11.21%", "12.90%", "11.21%"]
    ]
    t1 = doc.add_table(rows=len(rows_t1)+1, cols=len(headers_t1))
    format_table(t1, headers_t1, rows_t1)
    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Table 2: Standalone Segment Information
    doc.add_heading("Table 2: Standalone Segment Information (AS-17 / RBI Guidelines) (₹ in crore)", level=2)
    headers_t2 = ["Segment Particulars", "30.06.2026 (Unaudited)", "31.03.2026 (Audited)", "30.06.2025 (Unaudited)", "31.03.2026 (Full Year)"]
    rows_t2 = [
        ["1. Segment Revenue:", "", "", "", ""],
        ["  a) Treasury", "18,192.38", "17,295.96", "28,283.34", "84,337.48"],
        ["  b) Retail Banking", "75,888.80", "74,757.59", "75,191.18", "3,01,853.51"],
        ["    (i) Digital Banking Units", "3.39", "2.76", "2.49", "10.37"],
        ["    (ii) Non-Digital Banking", "75,885.41", "74,754.83", "75,188.69", "3,01,843.14"],
        ["  c) Wholesale Banking", "48,670.85", "44,643.71", "44,790.22", "1,74,506.30"],
        ["  d) Other Banking Operations", "9,044.03", "9,265.09", "8,693.64", "36,840.96"],
        ["  Total Segment Revenue", "1,51,796.06", "1,45,962.35", "1,56,958.38", "5,97,538.25"],
        ["  Less: Inter Segment Revenue", "59,611.68", "56,153.45", "57,758.35", "2,27,483.60"],
        ["  Income from Operations", "92,184.38", "89,808.90", "99,200.03", "3,70,054.65"],
        ["2. Segment Results (Profit Before Tax):", "", "", "", ""],
        ["  a) Treasury", "2,406.59", "1,925.23", "12,776.86", "21,142.48"],
        ["  b) Retail Banking", "10,131.32", "10,897.98", "3,381.70", "32,026.72"],
        ["    (i) Digital Banking Units", "0.07", "(0.56)", "(0.20)", "(1.59)"],
        ["    (ii) Non-Digital Banking", "10,131.25", "10,898.54", "3,381.90", "32,028.31"],
        ["  c) Wholesale Banking", "10,364.04", "10,398.96", "3,698.39", "33,947.96"],
        ["  d) Other Banking Operations", "2,795.81", "2,562.40", "2,016.76", "10,415.96"],
        ["  e) Unallocated", "(589.46)", "(591.22)", "(581.38)", "(2,364.43)"],
        ["  Total Profit Before Tax", "25,108.30", "25,193.35", "21,292.33", "95,168.69"],
        ["3. Segment Assets:", "", "", "", ""],
        ["  a) Treasury", "10,86,021.85", "11,49,929.44", "10,24,344.73", "11,49,929.44"],
        ["  b) Retail Banking (incl. Digital)", "16,18,976.54", "15,80,887.11", "15,28,135.60", "15,80,887.11"],
        ["  c) Wholesale Banking", "15,59,292.84", "14,99,816.13", "12,69,139.82", "14,99,816.13"],
        ["  d) Other Banking Operations", "1,15,884.08", "1,12,867.13", "1,10,854.88", "1,12,867.13"],
        ["  e) Unallocated", "17,285.97", "21,386.51", "21,601.63", "21,386.51"],
        ["  Total Segment Assets", "43,97,461.28", "43,64,886.32", "39,54,076.66", "43,64,886.32"],
        ["4. Segment Liabilities:", "", "", "", ""],
        ["  a) Treasury", "78,998.60", "98,273.66", "84,025.64", "98,273.66"],
        ["  b) Retail Banking (incl. Digital)", "25,32,744.34", "25,28,789.64", "23,22,644.57", "25,28,789.64"],
        ["  c) Wholesale Banking", "11,59,025.98", "11,30,276.17", "9,66,071.31", "11,30,276.17"],
        ["  d) Other Banking Operations", "4,100.45", "3,997.87", "9,253.99", "3,997.87"],
        ["  e) Unallocated", "39,498.81", "40,648.08", "49,441.01", "40,648.08"],
        ["  Total Segment Liabilities", "38,14,368.18", "38,01,985.42", "34,31,436.52", "38,01,985.42"],
        ["5. Capital, ESOPs & Reserves", "5,83,093.10", "5,62,900.90", "5,22,640.14", "5,62,900.90"],
        ["6. Total Liabilities & Equity", "43,97,461.28", "43,64,886.32", "39,54,076.66", "43,64,886.32"]
    ]
    t2 = doc.add_table(rows=len(rows_t2)+1, cols=len(headers_t2))
    format_table(t2, headers_t2, rows_t2)
    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Table 3: Standalone Balance Sheet
    doc.add_heading("Table 3: Standalone Statement of Assets and Liabilities (Note 1) (₹ in crore)", level=2)
    headers_t3 = ["Particulars", "As at 30.06.2026 (Unaudited)", "As at 30.06.2025 (Unaudited)", "As at 31.03.2026 (Audited)"]
    rows_t3 = [
        ["CAPITAL AND LIABILITIES", "", "", ""],
        ["  Capital", "1,540.13", "766.79", "1,539.34"],
        ["  Employees stock options / units outstanding", "4,894.56", "4,043.72", "4,545.11"],
        ["  Reserves and surplus", "5,76,658.41", "5,17,829.63", "5,56,816.45"],
        ["  Deposits", "31,70,830.09", "27,64,089.02", "31,05,250.48"],
        ["  Borrowings", "4,61,812.65", "5,10,056.21", "4,89,394.63"],
        ["  Other liabilities and provisions", "1,81,725.44", "1,57,291.29", "2,07,340.31"],
        ["TOTAL CAPITAL AND LIABILITIES", "43,97,461.28", "39,54,076.66", "43,64,886.32"],
        ["ASSETS", "", "", ""],
        ["  Cash and balances with Reserve Bank of India", "1,50,562.42", "1,42,538.15", "2,00,679.37"],
        ["  Balances with banks & money at call / short notice", "73,002.00", "60,057.11", "97,786.99"],
        ["  Investments", "9,19,413.40", "8,96,663.53", "8,84,201.47"],
        ["  Advances", "30,37,303.31", "26,28,434.20", "29,37,166.26"],
        ["  Fixed assets", "14,566.38", "13,784.70", "14,724.64"],
        ["  Other assets", "2,02,613.77", "2,12,598.97", "2,30,327.59"],
        ["TOTAL ASSETS", "43,97,461.28", "39,54,076.66", "43,64,886.32"]
    ]
    t3 = doc.add_table(rows=len(rows_t3)+1, cols=len(headers_t3))
    format_table(t3, headers_t3, rows_t3)
    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Table 4: NPAs Transferred (Note 9(i))
    doc.add_heading("Table 4: Details of Non-Performing Assets Transferred (Note 9(i))", level=2)
    headers_t4 = ["Particulars", "To ARCs", "To Permitted Transferees", "To Other Transferees"]
    rows_t4 = [
        ["Number of accounts", "7.43*", "-", "-"],
        ["Aggregate principal outstanding of loans transferred (₹ in cr)", "7.43", "-", "-"],
        ["Weighted average residual tenor (in years)", "-", "-", "-"],
        ["Net book value of loans transferred (at time of transfer)", "-", "-", "-"],
        ["Aggregate consideration realized", "-", "-", "-"],
        ["Additional consideration realized from earlier years", "-", "-", "-"]
    ]
    t4 = doc.add_table(rows=len(rows_t4)+1, cols=len(headers_t4))
    format_table(t4, headers_t4, rows_t4)
    doc.add_paragraph("Note: The Bank has not transferred/acquired any loans not in default, stressed loans (NPAs/SMAs), or SMAs during Q1 FY27.").paragraph_format.space_after = Pt(12)

    # Table 5: Security Receipts Ratings (Note 9(v))
    doc.add_heading("Table 5: Outstanding Security Receipts (SRs) & Recovery Ratings (Note 9(v))", level=2)
    headers_t5 = ["Rating Grade", "Rating Agency", "Recovery Rating Benchmark", "Gross Value of Outstanding SRs (₹ in crore)"]
    rows_t5 = [
        ["RR1+", "India Ratings", "More than 150%", "0.15"],
        ["RR1", "ICRA", "100% - 150%", "111.65"],
        ["RR2", "India Ratings", "75% - 100%", "27.32"],
        ["RR4", "India Ratings", "25% - 50%", "35.14"],
        ["RR5", "India Ratings", "Upto 25%", "125.67"],
        ["RR5", "CRISIL", "Upto 25%", "29.41"],
        ["Unrated", "-", "-", "719.85"],
        ["TOTAL OUTSTANDING SRs", "-", "-", "1,049.19"]
    ]
    t5 = doc.add_table(rows=len(rows_t5)+1, cols=len(headers_t5))
    format_table(t5, headers_t5, rows_t5)
    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Table 6: Project Finance Disclosures (Note 10)
    doc.add_heading("Table 6: Disclosures Related to Infrastructure Project Finance (Note 10)", level=2)
    headers_t6 = ["Item Description", "Number of Accounts", "Total Outstanding Amount (₹ in crore)"]
    rows_t6 = [
        ["1. Projects under implementation at beginning of quarter", "447", "24,693.48"],
        ["2. Projects under implementation sanctioned during quarter", "85", "1,031.08"],
        ["3. Projects where DCCO was achieved during quarter", "75", "4,442.26"],
        ["4. Projects under implementation at end of quarter*", "440", "20,785.14"],
        ["5. Out of '4': Resolution process involving DCCO extension invoked", "35", "1,597.95"],
        ["  5.1. Out of '5': Resolution plan implemented", "29", "1,360.20"],
        ["  5.2. Out of '5': Resolution plan under implementation", "6", "237.75"],
        ["  5.3. Out of '5': Resolution plan failed", "2", "87.61"],
        ["6. Out of '5': Extension invoked due to change in scope/size", "-", "-"],
        ["7. Out of '5': Cost associated with DCCO extension funded", "-", "-"],
        ["  7.1. Out of '7': SBCF sanctioned during closure & renewed continuously", "-", "-"],
        ["  7.2. Out of '7': SBCF not pre-sanctioned / renewed continuously", "-", "-"],
        ["8. Out of '4': Resolution process not involving DCCO extension invoked", "-", "-"]
    ]
    t6 = doc.add_table(rows=len(rows_t6)+1, cols=len(headers_t6))
    format_table(t6, headers_t6, rows_t6)
    doc.add_paragraph("*Excludes 17 accounts where repayment was completed prior to DCCO achievement.").paragraph_format.space_after = Pt(16)

    doc.add_page_break()

    # ---------------------------------------------------------
    # PART III: STANDALONE AUDITORS' REPORT
    # ---------------------------------------------------------
    doc.add_heading("Part III: Standalone Independent Auditors' Limited Review Report", level=1)
    
    audit_standalone_text = (
        "To the Board of Directors of HDFC Bank Limited\n\n"
        "1. We have reviewed the accompanying Statement of Unaudited Standalone Financial Results of HDFC Bank Limited ('the Bank') "
        "for the quarter ended June 30, 2026 ('the Statement'), submitted pursuant to Regulation 33 and Regulation 52(4) read with Regulation 63 "
        "of the SEBI (Listing Obligations and Disclosure Requirements) Regulations, 2015, as amended.\n\n"
        "2. Management Responsibility & Compliance: This Statement is the responsibility of the Bank's Management and approved by its Board "
        "of Directors on July 18, 2026. It has been prepared in accordance with Accounting Standard 25 'Interim Financial Reporting' (AS 25) "
        "prescribed under Section 133 of the Companies Act, 2013, provisions of the Banking Regulation Act, 1949, RBI guidelines, and accepted "
        "accounting principles in India.\n\n"
        "3. Scope of Limited Review: We conducted our review in accordance with Standard on Review Engagements (SRE) 2410 'Review of Interim Financial "
        "Information Performed by the Independent Auditor of the Entity' issued by ICAI. A review is substantially less in scope than an audit conducted "
        "in accordance with Standards on Auditing and consequently does not enable us to obtain assurance that we would become aware of all significant "
        "matters. Accordingly, we do not express an audit opinion.\n\n"
        "4. Conclusion: Based on our review, nothing has come to our attention that causes us to believe that the accompanying Statement has not "
        "been prepared in accordance with applicable accounting standards and RBI guidelines, or that it contains any material misstatement.\n\n"
        "Joint Statutory Auditors Signatures:\n"
        "For B S R & Co. LLP (Firm Reg No: 101248W/W-100022)\n"
        "Sudhir Soni (Partner, Membership No: 041870 | UDIN: 26041870OATJRT2952)\n\n"
        "For Batliboi & Purohit (Firm Reg No: 101048W)\n"
        "Janak Mehta (Partner, Membership No: 116976 | UDIN: 26116976GFKHWQ9629)\n"
        "Place: Mumbai | Date: July 18, 2026"
    )
    p_audit_s = doc.add_paragraph(audit_standalone_text)
    p_audit_s.paragraph_format.space_after = Pt(16)

    doc.add_page_break()

    # ---------------------------------------------------------
    # PART IV: CONSOLIDATED FINANCIAL STATEMENTS (TABLES 7-9)
    # ---------------------------------------------------------
    doc.add_heading("Part IV: Consolidated Financial Results & Group Disclosures", level=1)
    
    # Table 7: Consolidated P&L
    doc.add_heading("Table 7: Unaudited Consolidated Financial Results for the Quarter Ended June 30, 2026 (₹ in crore)", level=2)
    headers_t7 = ["Particulars", "30.06.2026 (Unaudited)", "31.03.2026 (Audited)", "30.06.2025 (Unaudited)", "31.03.2026 (Full Year)"]
    rows_t7 = [
        ["1. Interest earned (a)+(b)+(c)+(d)", "90,575.33", "87,182.50", "87,371.87", "3,48,615.15"],
        ["  a) Interest/discount on advances/bills", "66,406.51", "64,620.88", "64,147.91", "2,56,192.47"],
        ["  b) Income on investments", "20,753.16", "19,931.22", "20,817.17", "82,656.87"],
        ["  c) Interest on RBI balances & inter-bank funds", "1,599.37", "1,118.23", "826.44", "3,457.06"],
        ["  d) Others", "1,816.29", "1,512.17", "1,580.35", "6,308.75"],
        ["2. Other Income (a)+(b)", "42,535.03", "29,737.44", "45,683.10", "1,46,847.66"],
        ["  a) Premium & operating income from insurance", "18,353.92", "27,584.74", "16,073.37", "84,160.02"],
        ["  b) Others (Refer note 9)", "24,181.11", "2,152.70", "29,609.73", "62,687.64"],
        ["3. Total Income (1)+(2)", "1,33,110.36", "1,16,919.94", "1,33,054.97", "4,95,462.81"],
        ["4. Interest expended", "47,625.63", "45,220.44", "47,708.51", "1,85,491.23"],
        ["5. Operating expenses (i)+(ii)+(iii)", "54,488.73", "40,587.82", "49,183.00", "1,81,173.91"],
        ["  i) Employees cost", "9,342.49", "9,089.30", "8,897.46", "37,604.81"],
        ["  ii) Claims, benefits & insurance expenses", "32,177.54", "18,170.74", "28,072.92", "92,340.22"],
        ["  iii) Other operating expenses", "12,968.70", "13,327.78", "12,212.62", "51,228.88"],
        ["6. Total Expenditure (4)+(5) (excl. provisions)", "1,02,114.36", "85,808.26", "96,891.51", "3,66,665.14"],
        ["7. Operating Profit before provisions (3)-(6)", "30,996.00", "31,111.68", "36,163.46", "1,28,797.67"],
        ["8. Provisions & Contingencies (Refer note 8)", "3,802.84", "3,440.05", "15,313.63", "26,656.22"],
        ["9. Exceptional items", "-", "-", "-", "-"],
        ["10. PBT & Minority Interest (7)-(8)", "27,193.16", "27,671.63", "20,849.83", "1,02,141.45"],
        ["11. Tax Expense", "6,810.47", "6,597.41", "3,759.40", "22,921.99"],
        ["12. PAT before Minority Interest (10)-(11)", "20,382.69", "21,074.22", "17,090.43", "79,219.46"],
        ["13. Extraordinary items (net of tax)", "-", "-", "-", "-"],
        ["14. Net Profit before Minority Interest (12)-(13)", "20,382.69", "21,074.22", "17,090.43", "79,219.46"],
        ["15. Less: Minority Interest", "1,137.98", "723.46", "832.52", "3,193.49"],
        ["16. Net Profit for the period (Group Share) (14)-(15)", "19,244.71", "20,350.76", "16,257.91", "76,025.97"],
        ["17. Paid up equity share capital (Face Value ₹1/-)", "1,540.13", "1,539.34", "766.79", "1,539.34"],
        ["18. Reserves excluding revaluation reserves", "-", "5,79,975.02", "-", "5,79,975.02"],
        ["19. Earnings Per Share (EPS) (₹):", "", "", "", ""],
        ["  (a) Basic EPS (not annualized)", "12.50", "13.22", "10.61", "49.50"],
        ["  (b) Diluted EPS (not annualized)", "12.47", "13.18", "10.56", "49.28"]
    ]
    t7 = doc.add_table(rows=len(rows_t7)+1, cols=len(headers_t7))
    format_table(t7, headers_t7, rows_t7)
    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Table 8: Consolidated Segment Information
    doc.add_heading("Table 8: Consolidated Segment Information (Group Level) (₹ in crore)", level=2)
    headers_t8 = ["Segment Particulars", "30.06.2026 (Unaudited)", "31.03.2026 (Audited)", "30.06.2025 (Unaudited)", "31.03.2026 (Full Year)"]
    rows_t8 = [
        ["1. Segment Revenue:", "", "", "", ""],
        ["  a) Treasury", "18,192.38", "17,295.96", "26,104.21", "82,158.35"],
        ["  b) Retail Banking (incl Digital)", "75,888.80", "74,757.59", "75,191.18", "3,01,853.51"],
        ["  c) Wholesale Banking", "48,670.85", "44,643.71", "44,790.22", "1,74,506.30"],
        ["  d) Other Banking Operations", "9,044.03", "9,265.09", "8,693.64", "36,840.96"],
        ["  e) Insurance Business**", "35,951.83", "21,980.32", "31,619.24", "1,08,079.83"],
        ["  f) Others^", "4,974.15", "5,130.72", "4,414.83", "19,507.46"],
        ["  Total Segment Revenue", "1,92,722.04", "1,73,073.39", "1,90,813.32", "7,22,946.41"],
        ["  Less: Inter Segment Revenue", "59,611.68", "56,153.45", "57,758.35", "2,27,483.60"],
        ["  Income from Operations", "1,33,110.36", "1,16,919.94", "1,33,054.97", "4,95,462.81"],
        ["2. Segment Results (Profit Before Tax & Minority Interest):", "", "", "", ""],
        ["  a) Treasury", "2,406.59", "1,925.23", "10,597.73", "18,963.35"],
        ["  b) Retail Banking (incl Digital)", "10,131.32", "10,897.98", "3,381.70", "32,026.72"],
        ["  c) Wholesale Banking", "10,364.04", "10,398.96", "3,698.39", "33,947.96"],
        ["  d) Other Banking Operations", "2,795.81", "2,562.40", "2,016.76", "10,415.96"],
        ["  e) Insurance Business**", "1,750.38", "1,778.65", "1,644.92", "7,083.51"],
        ["  f) Others", "334.48", "699.63", "91.71", "2,068.38"],
        ["  g) Unallocated", "(589.46)", "(591.22)", "(581.38)", "(2,364.43)"],
        ["  Total Profit Before Tax & Minority Interest", "27,193.16", "27,671.63", "20,849.83", "1,02,141.45"],
        ["3. Segment Assets:", "", "", "", ""],
        ["  a) Treasury", "10,86,021.85", "11,49,929.44", "10,24,344.73", "11,49,929.44"],
        ["  b) Retail Banking", "16,18,976.54", "15,80,887.11", "15,28,135.60", "15,80,887.11"],
        ["  c) Wholesale Banking", "15,59,292.84", "14,99,816.13", "12,69,139.82", "14,99,816.13"],
        ["  d) Other Banking Operations", "1,15,884.08", "1,12,867.13", "1,10,854.88", "1,12,867.13"],
        ["  e) Insurance Business**", "4,41,063.92", "4,14,400.04", "3,90,123.07", "4,14,400.04"],
        ["  f) Others", "1,32,948.46", "1,28,754.48", "1,11,848.31", "1,28,754.48"],
        ["  g) Unallocated", "17,285.97", "21,386.51", "21,601.63", "21,386.51"],
        ["  Total Segment Assets", "49,71,473.66", "49,08,040.84", "44,56,048.04", "49,08,040.84"],
        ["4. Segment Liabilities:", "", "", "", ""],
        ["  a) Treasury", "78,998.60", "98,273.66", "84,025.64", "98,273.66"],
        ["  b) Retail Banking", "25,32,744.34", "25,28,789.64", "23,22,644.57", "25,28,789.64"],
        ["  c) Wholesale Banking", "11,59,025.98", "11,30,276.17", "9,66,071.31", "11,30,276.17"],
        ["  d) Other Banking Operations", "4,100.45", "3,997.87", "9,253.99", "3,997.87"],
        ["  e) Insurance Business**", "4,21,651.63", "3,98,573.63", "3,74,712.75", "3,98,573.63"],
        ["  f) Others", "1,06,068.47", "99,037.36", "86,751.07", "99,037.36"],
        ["  g) Unallocated", "39,498.81", "40,648.08", "49,441.01", "40,648.08"],
        ["  Total Segment Liabilities", "43,42,088.28", "42,99,596.41", "38,92,900.34", "42,99,596.41"],
        ["5. Capital, ESOPs & Reserves", "6,29,385.38", "6,08,444.43", "5,63,147.70", "6,08,444.43"],
        ["6. Total Liabilities & Equity", "49,71,473.66", "49,08,040.84", "44,56,048.04", "49,08,040.84"]
    ]
    t8 = doc.add_table(rows=len(rows_t8)+1, cols=len(headers_t8))
    format_table(t8, headers_t8, rows_t8)
    doc.add_paragraph("**Includes HDFC Life and HDFC ERGO operations. ^Includes other non-banking consolidated entities.").paragraph_format.space_after = Pt(12)

    # Table 9: Consolidated Balance Sheet
    doc.add_heading("Table 9: Consolidated Statement of Assets and Liabilities (Note 1) (₹ in crore)", level=2)
    headers_t9 = ["Particulars", "As at 30.06.2026 (Unaudited)", "As at 30.06.2025 (Unaudited)", "As at 31.03.2026 (Audited)"]
    rows_t9 = [
        ["CAPITAL AND LIABILITIES", "", "", ""],
        ["  Capital", "1,540.13", "766.79", "1,539.34"],
        ["  Employees stock options / units outstanding", "4,894.56", "4,043.72", "4,545.11"],
        ["  Reserves and surplus", "5,99,871.21", "5,37,823.51", "5,79,975.02"],
        ["  Minority interest", "23,079.48", "20,513.68", "22,384.96"],
        ["  Deposits", "31,67,330.55", "27,56,487.50", "30,99,638.29"],
        ["  Borrowings", "5,65,871.38", "5,99,612.81", "5,88,484.55"],
        ["  Other liabilities and provisions", "2,26,751.15", "1,98,051.73", "2,52,977.53"],
        ["  Policyholders' funds", "3,82,135.20", "3,38,748.30", "3,58,496.04"],
        ["TOTAL CAPITAL AND LIABILITIES", "49,71,473.66", "44,56,048.04", "49,08,040.84"],
        ["ASSETS", "", "", ""],
        ["  Cash and balances with Reserve Bank of India", "1,50,579.79", "1,42,561.88", "2,00,707.11"],
        ["  Balances with banks & money at call / short notice", "87,186.84", "72,050.90", "1,11,218.94"],
        ["  Investments", "13,39,916.99", "12,65,771.54", "12,80,216.29"],
        ["  Advances", "31,56,014.45", "27,35,109.92", "30,50,783.23"],
        ["  Fixed assets", "16,333.29", "15,439.01", "16,491.59"],
        ["  Other assets", "2,21,442.30", "2,25,114.79", "2,48,623.68"],
        ["TOTAL ASSETS", "49,71,473.66", "44,56,048.04", "49,08,040.84"]
    ]
    t9 = doc.add_table(rows=len(rows_t9)+1, cols=len(headers_t9))
    format_table(t9, headers_t9, rows_t9)
    doc.add_paragraph().paragraph_format.space_after = Pt(16)

    doc.add_page_break()

    # ---------------------------------------------------------
    # PART V: CONSOLIDATED AUDITORS' REPORT & ANNEXURE I (TABLE 10)
    # ---------------------------------------------------------
    doc.add_heading("Part V: Consolidated Auditors' Report & List of Consolidated Entities", level=1)
    
    audit_cons_text = (
        "Independent Auditors' Limited Review Report on Consolidated Financial Results of HDFC Bank Limited\n\n"
        "To the Board of Directors of HDFC Bank Limited\n\n"
        "1. We have reviewed the accompanying Statement of Unaudited Consolidated Financial Results of HDFC Bank Limited ('the Parent' / 'the Bank') "
        "and its subsidiaries (together referred to as 'the Group') for the quarter ended June 30, 2026 ('the Statement'), submitted pursuant to "
        "Regulation 33 and Regulation 52(4) of SEBI Listing Regulations, except for consolidated Basel III Pillar 3 disclosures.\n\n"
        "2. Management Responsibility & Compliance: Prepared in accordance with AS 25 Interim Financial Reporting, Banking Regulation Act 1949, "
        "RBI guidelines, and IRDAI guidelines for insurance subsidiaries.\n\n"
        "3. Scope & Actuarial Reliance:\n"
        "  • Life Insurance Policy Liabilities: Relied upon Appointed Actuary's certificate of HDFC Life Insurance Company Limited.\n"
        "  • Non-Life IBNR/IBNER Reserves: Relied upon Appointed Actuary's certificate of HDFC ERGO General Insurance Company Limited.\n\n"
        "4. Conclusion: Nothing has come to our attention that causes us to believe that the Statement contains any material misstatement.\n\n"
        "Joint Statutory Auditors Signatures:\n"
        "For B S R & Co. LLP (Firm Reg No: 101248W/W-100022)\n"
        "Sudhir Soni (Partner, Mem No: 041870 | UDIN: 26041870GKNRHZ4725)\n\n"
        "For Batliboi & Purohit (Firm Reg No: 101048W)\n"
        "Janak Mehta (Partner, Mem No: 116976 | UDIN: 26116976KJDYQU8402)\n"
        "Place: Mumbai | Date: July 18, 2026"
    )
    doc.add_paragraph(audit_cons_text).paragraph_format.space_after = Pt(12)

    # Table 10: Annexure I - Consolidated Entities
    doc.add_heading("Table 10: Annexure I — List of Entities Included in Consolidated Results", level=2)
    headers_t10 = ["Sr. No.", "Name of Entity", "Relationship", "Location / Notes"]
    rows_t10 = [
        ["1", "HDFC Bank Limited", "Parent Entity", "Mumbai, India"],
        ["2", "HDFC Life Insurance Company Limited", "Subsidiary", "India (50.54% stake)"],
        ["3", "HDB Financial Services Limited", "Subsidiary", "India (Post-IPO OFS)"],
        ["4", "HDFC Securities Limited", "Subsidiary", "India"],
        ["5", "HDFC Asset Management Company Limited", "Subsidiary", "India"],
        ["6", "HDFC ERGO General Insurance Company Limited", "Subsidiary", "India"],
        ["7", "HDFC Sales Private Limited", "Subsidiary", "India"],
        ["8", "HDFC Capital Advisors Limited", "Subsidiary", "India"],
        ["9", "HDFC Trustee Company Limited", "Subsidiary", "India"],
        ["10", "Griha Pte. Limited", "Subsidiary", "Singapore"],
        ["11", "Griha Investments", "Subsidiary", "Mauritius"],
        ["12", "HDFC International Life and Re Company Limited", "Subsidiary of HDFC Life", "Dubai (DIFC)"],
        ["13", "HDFC Pension Fund Management Limited", "Subsidiary of HDFC Life", "India"],
        ["14", "HDFC AMC International (IFSC) Limited", "Subsidiary of HDFC AMC", "GIFT City, India"],
        ["15", "HDFC Securities IFSC Limited", "Subsidiary of HDFC Securities", "GIFT City, India"],
        ["16", "HDB Employee Welfare Trust", "Consolidated Entity", "Consolidated as Subsidiary"]
    ]
    t10 = doc.add_table(rows=len(rows_t10)+1, cols=len(headers_t10))
    format_table(t10, headers_t10, rows_t10)
    doc.add_paragraph().paragraph_format.space_after = Pt(16)

    # Save document
    out_dir = r"C:\Users\user\PycharmProjects\the_haldankar_method_research_laboratory\BusinessQuartelyFirst"
    out_path = os.path.join(out_dir, "Transformed_HDFC_Bank_Q1_2026_27_Financials.docx")
    doc.save(out_path)
    print(f"Document successfully created and saved at: {out_path}")

if __name__ == "__main__":
    create_transformed_document()
