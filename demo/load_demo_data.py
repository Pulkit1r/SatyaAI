from core.narratives.narrative_manager import process_new_claim

demo_claims = [
("Fake image shows massive Delhi flood", 2020, "facebook"),
("Old flood photo reshared as current disaster", 2022, "twitter"),
("Same flood image viral again this monsoon", 2024, "whatsapp"),
("Vaccine causes infertility claim goes viral", 2021, "telegram"),
("Old vaccine infertility rumor resurfaces", 2023, "twitter")
]

for c in demo_claims:
    process_new_claim(c[0], {"year": c[1], "source": c[2]})

print("✅ Demo dataset loaded")
