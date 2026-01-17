from core.reports.trust_report import generate_trust_report

query = "fake flood image in delhi"

report = generate_trust_report(query)

print("\n🧠 DIGITAL TRUST REPORT\n")
print("Narrative ID:", report.get("narrative_id"))
print("Sources seen:", report.get("sources_seen"))
print("\nTimeline:\n")

for item in report.get("timeline", []):
    print(item)

print("\nInsight:\n", report.get("insight"))
