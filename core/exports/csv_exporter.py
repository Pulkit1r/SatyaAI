"""
CSV export functionality
"""
import csv
from datetime import datetime
from pathlib import Path
from core.config import EXPORT_DIR


def export_narrative_history_csv(narrative_id: str, memories: list) -> str:
    """
    Export narrative history to CSV.
    
    Args:
        narrative_id: Narrative ID
        memories: List of memory objects
        
    Returns:
        str: Path to exported file
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"narrative_{narrative_id}_{timestamp}.csv"
    filepath = EXPORT_DIR / filename
    
    # Define CSV columns
    fieldnames = ['year', 'source', 'type', 'claim', 'narrative_id', 'path']
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        
        for memory in memories:
            # Ensure all fields exist
            row = {field: memory.get(field, '') for field in fieldnames}
            writer.writerow(row)
    
    return str(filepath)


def export_all_narratives_csv(narratives: dict) -> str:
    """
    Export all narratives to CSV (flattened).
    
    Args:
        narratives: Dictionary of all narratives
        
    Returns:
        str: Path to exported file
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"all_narratives_{timestamp}.csv"
    filepath = EXPORT_DIR / filename
    
    fieldnames = ['narrative_id', 'year', 'source', 'type', 'claim', 'path']
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        
        for narrative_id, memories in narratives.items():
            for memory in memories:
                row = {
                    'narrative_id': narrative_id,
                    **{field: memory.get(field, '') for field in fieldnames[1:]}
                }
                writer.writerow(row)
    
    return str(filepath)


def export_analytics_report_csv(analytics_data: dict) -> str:
    """
    Export analytics summary to CSV.
    
    Args:
        analytics_data: Analytics dictionary
        
    Returns:
        str: Path to exported file
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"analytics_report_{timestamp}.csv"
    filepath = EXPORT_DIR / filename
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Metric', 'Value'])
        
        for key, value in analytics_data.items():
            if isinstance(value, (str, int, float)):
                writer.writerow([key, value])
            elif isinstance(value, dict):
                writer.writerow([key, str(value)])
    
    return str(filepath)