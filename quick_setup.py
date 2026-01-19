"""
Quick setup script - initialize everything with more demo data
"""
import sys
import os

print("🚀 SatyaAI Quick Setup")
print("=" * 60)

# 1. Initialize database
print("\n1️⃣ Initializing Qdrant database...")
try:
    from core.qdrant.schema import setup_collections
    setup_collections()
    print("   ✅ Database initialized")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# 2. Load demo data
print("\n2️⃣ Loading demo narratives...")
try:
    from core.narratives.narrative_manager import process_new_claim
    
    demo_claims = [
        # Flood narrative cluster
        ("Fake image shows massive Delhi flood", 2020, "facebook"),
        ("Old flood photo reshared as current disaster", 2022, "twitter"),
        ("Same flood image viral again this monsoon", 2024, "whatsapp"),
        ("Doctored flood images spread on social media", 2023, "telegram"),
        
        # Vaccine narrative cluster
        ("Vaccine causes infertility claim goes viral", 2021, "telegram"),
        ("Old vaccine infertility rumor resurfaces", 2023, "twitter"),
        ("COVID vaccine side effects being hidden", 2024, "facebook"),
        ("Vaccine misinformation spreads again", 2024, "whatsapp"),
        
        # Government narrative cluster
        ("Government hid flood data from public", 2022, "whatsapp"),
        ("Officials accused of hiding disaster statistics", 2023, "twitter"),
        ("Data manipulation claims go viral", 2024, "facebook"),
        
        # Political narrative cluster
        ("Doctored video of political leader spreads", 2023, "facebook"),
        ("Fake speech video goes viral", 2024, "twitter"),
        ("Manipulated politician footage resurfaces", 2024, "telegram"),
        
        # Climate narrative cluster
        ("Climate change hoax narrative resurfaces", 2020, "twitter"),
        ("Climate denial claims spread on forums", 2022, "facebook"),
        ("Old climate hoax post goes viral again", 2024, "whatsapp"),
        
        # Election narrative cluster
        ("Election fraud claims go viral", 2024, "twitter"),
        ("Voter fraud allegations resurface", 2024, "facebook"),
        ("Election rigging narrative spreads", 2024, "telegram"),
    ]
    
    narrative_count = 0
    for idx, (claim, year, source) in enumerate(demo_claims, 1):
        try:
            nid = process_new_claim(claim, {"year": year, "source": source})
            print(f"   {idx}. ✅ {claim[:50]}...")
            narrative_count += 1
        except Exception as e:
            print(f"   {idx}. ⚠️  Failed: {claim[:30]}... ({e})")
    
    print(f"\n✅ Loaded {narrative_count}/{len(demo_claims)} demo claims")
    
except Exception as e:
    print(f"❌ Error loading demo data: {e}")
    import traceback
    traceback.print_exc()

# 3. Verify setup
print("\n3️⃣ Verifying system...")
try:
    from core.narratives.narrative_explorer import get_all_narratives
    narratives = get_all_narratives()
    total_memories = sum(len(v) for v in narratives.values())
    
    print(f"   ✅ Found {len(narratives)} narratives")
    print(f"   ✅ Total memories: {total_memories}")
    
    if len(narratives) > 0:
        print("\n   📊 Narrative Distribution:")
        for nid, memories in list(narratives.items())[:5]:
            print(f"      • {nid}: {len(memories)} memories")
        if len(narratives) > 5:
            print(f"      ... and {len(narratives) - 5} more")
    
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 60)
print("✅ Setup complete!")
print("\n📝 Next steps:")
print("   1. Run: streamlit run ui/app.py")
print("   2. Navigate to Analytics or Export tabs")
print("   3. Explore the demo narratives")
print("=" * 60)