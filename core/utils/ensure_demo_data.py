"""
Ensure demo data exists in the system
"""
import os

def ensure_demo_data_loaded():
    """Load demo data if system is empty"""
    try:
        from core.narratives.narrative_explorer import get_all_narratives
        from core.narratives.narrative_manager import process_new_claim
        
        # Check if system has data
        narratives = get_all_narratives(limit=10)
        
        if len(narratives) == 0:
            print("📦 No data found. Loading demo dataset...")
            
            # Demo claims
            demo_claims = [
                ("Fake image shows massive Delhi flood", 2020, "facebook"),
                ("Old flood photo reshared as current disaster", 2022, "twitter"),
                ("Same flood image viral again this monsoon", 2024, "whatsapp"),
                ("Vaccine causes infertility claim goes viral", 2021, "telegram"),
                ("Old vaccine infertility rumor resurfaces", 2023, "twitter"),
                ("Government hid flood data from public", 2022, "whatsapp"),
                ("Doctored video of political leader spreads", 2023, "facebook"),
                ("Climate change hoax narrative resurfaces", 2020, "twitter"),
                ("COVID vaccine microchip conspiracy theory", 2021, "telegram"),
                ("Election fraud claims go viral again", 2024, "twitter"),
            ]
            
            for claim, year, source in demo_claims:
                try:
                    process_new_claim(claim, {"year": year, "source": source})
                except Exception as e:
                    print(f"⚠️  Error loading demo claim: {e}")
            
            print("✅ Demo data loaded successfully!")
            return True
        else:
            print(f"✓ Found {len(narratives)} existing narratives")
            return False
            
    except Exception as e:
        print(f"⚠️  Could not load demo data: {e}")
        return False