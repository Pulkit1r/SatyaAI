"""
JSON export functionality
"""
import json
from datetime import datetime
from pathlib import Path
from core.config import EXPORT_DIR


def export_trust_report_json(report: dict, narrative_id: str = None) -> str:
    """
    Export trust report to JSON file.
    
    Args:
        report: Trust report dictionary
        narrative_id: Optional narrative ID for filename
        
    Returns:
        str: Path to exported file
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if narrative_id:
        filename = f"trust_report_{narrative_id}_{timestamp}.json"
    else:
        filename = f"trust_report_{timestamp}.json"
    
    filepath = EXPORT_DIR / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    return str(filepath)


def export_narrative_history_json(narrative_id: str, memories: list) -> str:
    """
    Export narrative history to JSON.
    
    Args:
        narrative_id: Narrative ID
        memories: List of memory objects
        
    Returns:
        str: Path to exported file
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"narrative_{narrative_id}_{timestamp}.json"
    filepath = EXPORT_DIR / filename
    
    export_data = {
        "narrative_id": narrative_id,
        "exported_at": datetime.now().isoformat(),
        "total_memories": len(memories),
        "memories": memories
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    return str(filepath)


def export_all_narratives_json(narratives: dict) -> str:
    """
    Export all narratives to JSON.
    
    Args:
        narratives: Dictionary of all narratives
        
    Returns:
        str: Path to exported file
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"all_narratives_{timestamp}.json"
    filepath = EXPORT_DIR / filename
    
    export_data = {
        "exported_at": datetime.now().isoformat(),
        "total_narratives": len(narratives),
        "total_memories": sum(len(v) for v in narratives.values()),
        "narratives": narratives
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    return str(filepath)