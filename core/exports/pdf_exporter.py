"""
Enhanced PDF report generation with professional styling
"""
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from core.config import EXPORT_DIR

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, 
        TableStyle, PageBreak, Image, KeepTogether
    )
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


def export_trust_report_pdf(report: dict) -> str:
    """
    Generate enhanced PDF trust report with professional styling.
    
    Args:
        report: Trust report dictionary
        
    Returns:
        str: Path to generated PDF
    """
    if not REPORTLAB_AVAILABLE:
        raise ImportError(
            "reportlab is required for PDF export. "
            "Install it with: pip install reportlab"
        )
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    narrative_id = report.get('narrative_id', 'unknown')
    filename = f"trust_report_{narrative_id}_{timestamp}.pdf"
    filepath = EXPORT_DIR / filename
    
    # Create PDF document
    doc = SimpleDocTemplate(
        str(filepath), 
        pagesize=letter,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch,
        leftMargin=0.75*inch,
        rightMargin=0.75*inch
    )
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#64748b'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold'
    )
    
    subheading_style = ParagraphStyle(
        'Subheading',
        parent=styles['Heading3'],
        fontSize=13,
        textColor=colors.HexColor('#475569'),
        spaceAfter=10,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#334155'),
        alignment=TA_JUSTIFY,
        leading=14
    )
    
    # Header Section
    story.append(Paragraph("🧠 SatyaAI Trust Report", title_style))
    story.append(Paragraph(
        f"Narrative Intelligence Analysis • Generated {datetime.now().strftime('%B %d, %Y')}", 
        subtitle_style
    ))
    
    # Divider line
    story.append(Spacer(1, 0.1*inch))
    story.append(Table([['']], colWidths=[7*inch], style=[
        ('LINEABOVE', (0,0), (-1,0), 2, colors.HexColor('#1e40af'))
    ]))
    story.append(Spacer(1, 0.2*inch))
    
    # Executive Summary Box
    story.append(Paragraph("Executive Summary", heading_style))
    
    threat_level = report.get('threat_level', 'UNKNOWN')
    threat_colors_map = {
        'CRITICAL': colors.HexColor('#dc2626'),
        'HIGH': colors.HexColor('#ea580c'),
        'MEDIUM': colors.HexColor('#ca8a04'),
        'LOW': colors.HexColor('#16a34a')
    }
    threat_color = threat_colors_map.get(threat_level, colors.grey)
    
    summary_data = [
        ['Narrative ID', narrative_id],
        ['Threat Level', threat_level],
        ['Total Occurrences', str(report.get('occurrence_count', 0))],
        ['Narrative Status', report.get('narrative_state', 'Unknown')],
    ]
    
    summary_table = Table(summary_data, colWidths=[2*inch, 4.5*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f1f5f9')),
        ('BACKGROUND', (1, 1), (1, 1), colors.HexColor('#fef2f2') if threat_level in ['CRITICAL', 'HIGH'] else colors.HexColor('#f0fdf4')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#334155')),
        ('TEXTCOLOR', (1, 1), (1, 1), threat_color),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    story.append(summary_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Key Metrics Section
    story.append(Paragraph("Key Metrics", heading_style))
    
    metrics_data = [
        ['Metric', 'Value', 'Indicator'],
        ['Risk Level', report.get('risk_level', 'Unknown'), '⚠️'],
        ['First Observed', str(report.get('first_seen', 'Unknown')), '📅'],
        ['Last Observed', str(report.get('last_seen', 'Unknown')), '📅'],
        ['Lifespan', f"{report.get('lifespan', 0)} years", '⏳'],
        ['Platform Spread', str(len(report.get('sources_seen', []))), '🌐'],
        ['Resurfacing Pattern', 'Yes' if report.get('resurfacing') else 'No', '🔄'],
        ['Memory Strength', str(report.get('memory_strength', 0)), '💪'],
    ]
    
    metrics_table = Table(metrics_data, colWidths=[2.2*inch, 2.8*inch, 1.5*inch])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (2, 0), (2, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    story.append(metrics_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Platforms Section
    story.append(Paragraph("Platform Distribution", heading_style))
    platforms = report.get('sources_seen', [])
    if platforms:
        platforms_text = ' • '.join([p.upper() for p in platforms])
        story.append(Paragraph(
            f"<b>Detected on:</b> {platforms_text}", 
            body_style
        ))
    else:
        story.append(Paragraph("No platform data available", body_style))
    
    story.append(Spacer(1, 0.3*inch))
    
    # Intelligence Assessment
    story.append(Paragraph("Intelligence Assessment", heading_style))
    insight = report.get('insight', 'No assessment available.')
    
    # Create insight box
    insight_data = [[Paragraph(insight, body_style)]]
    insight_table = Table(insight_data, colWidths=[6.5*inch])
    insight_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#eff6ff')),
        ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ('RIGHTPADDING', (0, 0), (-1, -1), 15),
        ('TOPPADDING', (0, 0), (-1, -1), 15),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#3b82f6')),
    ]))
    
    story.append(insight_table)
    story.append(Spacer(1, 0.4*inch))
    
    # Historical Timeline
    story.append(Paragraph("Historical Timeline", heading_style))
    timeline = report.get('timeline', [])
    
    if timeline:
        story.append(Paragraph(
            f"<i>Showing {min(len(timeline), 10)} most relevant occurrences</i>", 
            ParagraphStyle('italic', parent=body_style, fontSize=9, textColor=colors.HexColor('#64748b'))
        ))
        story.append(Spacer(1, 0.1*inch))
        
        timeline_data = [['#', 'Year', 'Platform', 'Description', 'Score']]
        
        for idx, item in enumerate(timeline[:10], 1):
            year = str(item.get('year', 'N/A'))
            source = str(item.get('source', 'Unknown')).upper()
            claim = str(item.get('claim', 'Visual content'))[:80]
            if len(claim) > 77:
                claim = claim[:77] + "..."
            score = f"{item.get('score', 0):.2f}"
            
            timeline_data.append([str(idx), year, source, claim, score])
        
        timeline_table = Table(
            timeline_data, 
            colWidths=[0.3*inch, 0.6*inch, 1*inch, 3.8*inch, 0.8*inch]
        )
        timeline_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('ALIGN', (2, 0), (2, -1), 'LEFT'),
            ('ALIGN', (3, 0), (3, -1), 'LEFT'),
            ('ALIGN', (4, 0), (4, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))
        
        story.append(timeline_table)
    else:
        story.append(Paragraph("No timeline data available", body_style))
    
    story.append(Spacer(1, 0.5*inch))
    
    # Footer
    footer_data = [[
        Paragraph(
            "<b>SatyaAI</b> - Digital Trust Memory System<br/>"
            "This report provides analytical insights for decision support purposes.<br/>"
            "<i>Generated using narrative intelligence and vector memory analysis.</i>",
            ParagraphStyle(
                'Footer',
                parent=body_style,
                fontSize=8,
                textColor=colors.HexColor('#64748b'),
                alignment=TA_CENTER,
                leading=10
            )
        )
    ]]
    
    footer_table = Table(footer_data, colWidths=[6.5*inch])
    footer_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f1f5f9')),
        ('TOPPADDING', (0, 0), (-1, -1), 15),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
    ]))
    
    story.append(footer_table)
    
    # Build PDF
    doc.build(story)
    
    return str(filepath)


def export_narrative_report_pdf(narrative_id: str, memories: list, stats: dict) -> str:
    """
    Generate enhanced comprehensive narrative report PDF.
    
    Args:
        narrative_id: Narrative ID
        memories: List of memories
        stats: Narrative statistics
        
    Returns:
        str: Path to generated PDF
    """
    if not REPORTLAB_AVAILABLE:
        raise ImportError(
            "reportlab is required for PDF export. "
            "Install it with: pip install reportlab"
        )
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"narrative_{narrative_id}_{timestamp}.pdf"
    filepath = EXPORT_DIR / filename
    
    doc = SimpleDocTemplate(
        str(filepath), 
        pagesize=letter,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch
    )
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e40af'),
        alignment=TA_CENTER,
        spaceAfter=10,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.HexColor('#64748b'),
        alignment=TA_CENTER,
        spaceAfter=30
    )
    
    heading_style = ParagraphStyle(
        'Heading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold'
    )
    
    # Title Section
    story.append(Paragraph("Narrative Analysis Report", title_style))
    story.append(Paragraph(f"ID: {narrative_id}", subtitle_style))
    
    # Divider
    story.append(Table([['']], colWidths=[7*inch], style=[
        ('LINEABOVE', (0,0), (-1,0), 2, colors.HexColor('#1e40af'))
    ]))
    story.append(Spacer(1, 0.3*inch))
    
    # Statistics
    story.append(Paragraph("Narrative Statistics", heading_style))
    
    stats_data = [
        ['Metric', 'Value'],
        ['Total Occurrences', str(len(memories))],
        ['First Seen', str(stats.get('first_seen', 'Unknown'))],
        ['Last Seen', str(stats.get('last_seen', 'Unknown'))],
        ['Lifespan', f"{stats.get('lifespan', 0)} years"],
        ['Unique Sources', str(len(stats.get('sources', [])))],
        ['Content Types', ', '.join(stats.get('modalities', []))],
        ['Resurfacing', 'Yes' if stats.get('resurfacing') else 'No'],
        ['Memory Strength', str(stats.get('memory_strength', 0))],
        ['State', stats.get('state', 'Unknown')],
        ['Threat Level', stats.get('threat_level', 'Unknown')],
    ]
    
    stats_table = Table(stats_data, colWidths=[2.5*inch, 4*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
    ]))
    
    story.append(stats_table)
    story.append(PageBreak())
    
    # Memory timeline
    story.append(Paragraph("Complete Memory Timeline", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    for i, memory in enumerate(memories, 1):
        # Memory header
        story.append(Paragraph(
            f"<b>Memory {i}</b>", 
            ParagraphStyle('MemHeader', parent=styles['Normal'], fontSize=11, textColor=colors.HexColor('#1e40af'))
        ))
        
        # Memory details
        details = f"Year: {memory.get('year', 'Unknown')} | Source: {memory.get('source', 'Unknown')} | Type: {memory.get('type', 'Unknown')}"
        story.append(Paragraph(details, styles['Normal']))
        
        if memory.get('claim'):
            story.append(Paragraph(f"<i>Claim:</i> {memory['claim']}", styles['Normal']))
        
        story.append(Spacer(1, 0.15*inch))
    
    # Footer
    story.append(Spacer(1, 0.3*inch))
    story.append(Table([['']], colWidths=[7*inch], style=[
        ('LINEABOVE', (0,0), (-1,0), 1, colors.HexColor('#cbd5e1'))
    ]))
    story.append(Spacer(1, 0.1*inch))
    
    footer_text = Paragraph(
        "<i>Generated by SatyaAI Digital Trust Memory System</i>",
        ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=colors.grey, alignment=TA_CENTER)
    )
    story.append(footer_text)
    
    doc.build(story)
    
    return str(filepath)