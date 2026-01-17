from core.narratives.narrative_manager import process_new_claim


print("\n--- Adding claims to system ---\n")

process_new_claim("Fake image shows massive Delhi flood", {"year": 2020, "source": "facebook"})
process_new_claim("Old flood photo reshared as current Delhi disaster", {"year": 2022, "source": "twitter"})
process_new_claim("Same flood image going viral again this monsoon", {"year": 2024, "source": "whatsapp"})

process_new_claim("Viral post claims vaccine causes infertility", {"year": 2021, "source": "telegram"})
process_new_claim("Old vaccine infertility rumor resurfaces", {"year": 2023, "source": "twitter"})
