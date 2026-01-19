"""
Load demo data into SatyaAI
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.narratives.narrative_manager import process_new_claim

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
    ("Election fraud claims go viral again", 2024, "twitter")
]

print("=" * 60)
print("🔄 Loading Demo Data into SatyaAI")
print("=" * 60)

for idx, (claim, year, source) in enumerate(demo_claims, 1):
    try:
        nid = process_new_claim(claim, {"year": year, "source": source})
        print(f"{idx}. ✅ {claim[:50]}... → {nid}")
    except Exception as e:
        print(f"{idx}. ❌ Error: {e}")

print("=" * 60)
print("✅ Demo dataset loaded successfully!")
print(f"📊 Total claims added: {len(demo_claims)}")
print("=" * 60)
print("\n📝 Next steps:")
print("   streamlit run ui/app.py")