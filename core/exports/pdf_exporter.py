"""
PDF report generation
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
        TableStyle, PageBreak, Image
    )
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


def export_trust_report_pdf(report: dict) -> str:
    """
    Generate PDF trust report.
    
    Args:
        report: Trust report dictionary
        
    Returns:
        str: Path to generated PDF
        
    Raises:
        ImportError: If reportlab is not installed
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
    doc = SimpleDocTemplate(str(filepath), pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2C5F8D'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#2C5F8D'),
        spaceAfter=12
    )
    
    # Title
    story.append(Paragraph("🧠 SatyaAI Trust Report", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Header info
    story.append(Paragraph(f"<b>Narrative ID:</b> {narrative_id}", styles['Normal']))
    story.append(Paragraph(
        f"<b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
        styles['Normal']
    ))
    story.append(Spacer(1, 0.3*inch))
    
    # Key metrics
    story.append(Paragraph("Key Metrics", heading_style))
    
    metrics_data = [
        ['Metric', 'Value'],
        ['Occurrence Count', str(report.get('occurrence_count', 0))],
        ['Risk Level', report.get('risk_level', 'Unknown')],
        ['Threat Level', report.get('threat_level', 'Unknown')],
        ['First Seen', str(report.get('first_seen', 'Unknown'))],
        ['Last Seen', str(report.get('last_seen', 'Unknown'))],
        ['Lifespan', f"{report.get('lifespan', 0)} years"],
        ['Narrative State', report.get('narrative_state', 'Unknown')],
    ]
    
    metrics_table = Table(metrics_data, colWidths=[3*inch, 3*inch])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C5F8D')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(metrics_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Platforms
    story.append(Paragraph("Platforms Detected", heading_style))
    platforms = report.get('sources_seen', [])
    platforms_text = ', '.join(platforms) if platforms else 'None'
    story.append(Paragraph(platforms_text, styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Insight
    story.append(Paragraph("Intelligence Assessment", heading_style))
    insight = report.get('insight', 'No insight available.')
    story.append(Paragraph(insight, styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Timeline
    story.append(Paragraph("Historical Timeline", heading_style))
    timeline = report.get('timeline', [])
    
    if timeline:
        timeline_data = [['Year', 'Source', 'Claim/Description']]
        
        for item in timeline[:10]:  # Limit to first 10
            year = str(item.get('year', 'N/A'))
            source = str(item.get('source', 'Unknown'))
            claim = str(item.get('claim', 'Visual content'))[:60]
            timeline_data.append([year, source, claim])
        
        timeline_table = Table(timeline_data, colWidths=[0.8*inch, 1.2*inch, 4*inch])
        timeline_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C5F8D')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))
        
        story.append(timeline_table)
    
    story.append(Spacer(1, 0.5*inch))
    
    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    
    story.append(Paragraph(
        "This report was generated by SatyaAI Digital Trust Memory System<br/>"
        "© 2024 SatyaAI | For decision-support purposes only",
        footer_style
    ))
    
    # Build PDF
    doc.build(story)
    
    return str(filepath)


def export_narrative_report_pdf(narrative_id: str, memories: list, stats: dict) -> str:
    """
    Generate comprehensive narrative report PDF.
    
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
    filename = f"narrative_report_{narrative_id}_{timestamp}.pdf"
    filepath = EXPORT_DIR / filename
    
    doc = SimpleDocTemplate(str(filepath), pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=colors.HexColor('#2C5F8D'),
        alignment=TA_CENTER
    )
    
    story.append(Paragraph(f"Narrative Analysis Report", title_style))
    story.append(Paragraph(f"ID: {narrative_id}", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Statistics
    story.append(Paragraph("Narrative Statistics", styles['Heading2']))
    
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
    ]
    
    stats_table = Table(stats_data, colWidths=[2.5*inch, 3.5*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ]))
    
    story.append(stats_table)
    story.append(PageBreak())
    
    # Memory timeline
    story.append(Paragraph("Complete Memory Timeline", styles['Heading2']))
    
    for i, memory in enumerate(memories, 1):
        story.append(Paragraph(f"<b>Memory {i}</b>", styles['Normal']))
        story.append(Paragraph(
            f"Year: {memory.get('year', 'Unknown')} | "
            f"Source: {memory.get('source', 'Unknown')} | "
            f"Type: {memory.get('type', 'Unknown')}",
            styles['Normal']
        ))
        
        if memory.get('claim'):
            story.append(Paragraph(f"Claim: {memory['claim']}", styles['Normal']))
        
        story.append(Spacer(1, 0.1*inch))
    
    doc.build(story)
    
    return str(filepath)