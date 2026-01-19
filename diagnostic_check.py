"""
diagnostic_check.py - Check system status
"""
import sys
import os

print("🔍 SatyaAI System Diagnostic")
print("=" * 60)

# Check 1: File structure
print("\n1️⃣ Checking file structure...")
files_to_check = [
    "ui/pages/analytics.py",
    "ui/pages/exports.py",
    "core/analytics/trend_detector.py",
    "core/analytics/__init__.py",
    "core/exports/json_exporter.py",
    "core/exports/csv_exporter.py",
]

for file in files_to_check:
    if os.path.exists(file):
        print(f"   ✅ {file}")
    else:
        print(f"   ❌ {file} - MISSING!")

# Check 2: Import test
print("\n2️⃣ Testing imports...")
try:
    from ui.pages.analytics import render_analytics_page
    print("   ✅ analytics.render_analytics_page")
except Exception as e:
    print(f"   ❌ analytics import failed: {e}")

try:
    from ui.pages.exports import render_export_page
    print("   ✅ exports.render_export_page")
except Exception as e:
    print(f"   ❌ exports import failed: {e}")

try:
    from core.analytics.trend_detector import analyze_narrative_clusters
    print("   ✅ trend_detector imports")
except Exception as e:
    print(f"   ❌ trend_detector import failed: {e}")

# Check 3: Data test
print("\n3️⃣ Checking data...")
try:
    from core.narratives.narrative_explorer import get_all_narratives
    narratives = get_all_narratives()
    print(f"   ✅ Found {len(narratives)} narratives")
    print(f"   ✅ Total memories: {sum(len(v) for v in narratives.values())}")
except Exception as e:
    print(f"   ❌ Data check failed: {e}")

print("\n" + "=" * 60)
print("Diagnostic complete!")