"""
Trend detection and analytics for narratives
"""
from collections import defaultdict
from datetime import datetime, timedelta


def analyze_narrative_clusters(narratives):
    """
    Analyze narrative ecosystem statistics.
    
    Args:
        narratives: Dictionary of narrative_id -> list of memories
        
    Returns:
        dict: Cluster statistics
    """
    if not narratives:
        return {
            'total_narratives': 0,
            'total_memories': 0,
            'avg_narrative_size': 0,
            'largest_narrative': 0,
            'modality_distribution': {},
            'yearly_activity': {}
        }
    
    total_memories = sum(len(v) for v in narratives.values())
    sizes = [len(v) for v in narratives.values()]
    
    # Modality distribution
    modality_dist = defaultdict(int)
    for memories in narratives.values():
        for m in memories:
            modality = m.get('type', 'unknown')
            modality_dist[modality] += 1
    
    # Yearly activity
    yearly = defaultdict(int)
    for memories in narratives.values():
        for m in memories:
            year = m.get('year')
            if year and str(year).isdigit():
                yearly[int(year)] += 1
    
    return {
        'total_narratives': len(narratives),
        'total_memories': total_memories,
        'avg_narrative_size': total_memories / len(narratives) if narratives else 0,
        'largest_narrative': max(sizes) if sizes else 0,
        'modality_distribution': dict(modality_dist),
        'yearly_activity': dict(sorted(yearly.items()))
    }


def detect_viral_narratives(narratives, time_window_days=365):
    """
    Detect narratives that went viral (rapid spread).
    
    Args:
        narratives: Dictionary of narrative_id -> list of memories
        time_window_days: Time window to check for virality
        
    Returns:
        list: List of viral narratives with metrics
    """
    viral = []
    current_year = datetime.now().year
    cutoff_year = current_year - (time_window_days // 365)
    
    for nid, memories in narratives.items():
        # Count recent vs total
        recent = sum(1 for m in memories 
                    if m.get('year') and int(m.get('year', 0)) >= cutoff_year)
        total = len(memories)
        
        if total == 0:
            continue
        
        # Velocity metric
        velocity = recent / total if total > 0 else 0
        
        # Platform diversity
        platforms = len(set(m.get('source') for m in memories if m.get('source')))
        
        # Risk score
        risk_score = (velocity * 40) + (platforms * 15) + (min(recent, 10) * 5)
        
        if recent >= 3 and velocity > 0.3:  # At least 3 recent mentions and 30% velocity
            viral.append({
                'narrative_id': nid,
                'recent_mentions': recent,
                'total_mentions': total,
                'velocity': velocity,
                'platforms': platforms,
                'risk_score': round(risk_score, 2)
            })
    
    return sorted(viral, key=lambda x: x['risk_score'], reverse=True)


def compute_platform_risk_scores(narratives):
    """
    Compute risk scores by platform.
    
    Args:
        narratives: Dictionary of narrative_id -> list of memories
        
    Returns:
        dict: Platform risk scores
    """
    platform_stats = defaultdict(lambda: {
        'narratives': set(),
        'total_mentions': 0,
        'high_risk_narratives': set()
    })
    
    for nid, memories in narratives.items():
        # Determine if narrative is high risk
        is_high_risk = len(memories) >= 3 or len(set(m.get('source') for m in memories)) >= 2
        
        for m in memories:
            source = m.get('source', 'unknown')
            platform_stats[source]['narratives'].add(nid)
            platform_stats[source]['total_mentions'] += 1
            
            if is_high_risk:
                platform_stats[source]['high_risk_narratives'].add(nid)
    
    # Compute risk scores
    result = {}
    for platform, stats in platform_stats.items():
        unique_narratives = len(stats['narratives'])
        high_risk_count = len(stats['high_risk_narratives'])
        total_mentions = stats['total_mentions']
        
        # Risk score formula
        risk_score = (
            unique_narratives * 10 +
            high_risk_count * 25 +
            min(total_mentions, 20) * 2
        )
        
        if risk_score >= 100:
            risk_level = "CRITICAL"
        elif risk_score >= 60:
            risk_level = "HIGH"
        elif risk_score >= 30:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        
        result[platform] = {
            'unique_narratives': unique_narratives,
            'total_mentions': total_mentions,
            'high_risk_count': high_risk_count,
            'risk_score': risk_score,
            'risk_level': risk_level
        }
    
    return dict(sorted(result.items(), key=lambda x: x[1]['risk_score'], reverse=True))


def detect_coordinated_campaigns(narratives):
    """
    Detect potential coordinated campaigns (multiple narratives on same platform, same time).
    
    Args:
        narratives: Dictionary of narrative_id -> list of memories
        
    Returns:
        list: List of potential campaigns
    """
    # Group by year and platform
    campaigns_map = defaultdict(lambda: defaultdict(set))
    
    for nid, memories in narratives.items():
        for m in memories:
            year = m.get('year')
            source = m.get('source')
            if year and source:
                campaigns_map[year][source].add(nid)
    
    # Detect coordination
    campaigns = []
    for year, platforms in campaigns_map.items():
        for platform, narrative_ids in platforms.items():
            if len(narrative_ids) >= 3:  # 3+ narratives on same platform, same year
                coordination_score = len(narrative_ids) * 10
                
                campaigns.append({
                    'year': year,
                    'platform': platform,
                    'narrative_count': len(narrative_ids),
                    'narrative_ids': list(narrative_ids),
                    'coordination_score': coordination_score
                })
    
    return sorted(campaigns, key=lambda x: x['coordination_score'], reverse=True)