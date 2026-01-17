from core.memory.text_store import store_claim
from core.memory.text_search import search_claims


# Store some digital-trust memories
store_claim("This photo shows a recent flood in Delhi", {"year": 2024, "source": "twitter"})
store_claim("Old image shared as current Delhi flood", {"year": 2021, "source": "facebook"})
store_claim("Viral post claims government hid flood data", {"year": 2022, "source": "whatsapp"})
store_claim("Same flood image resurfaces every monsoon", {"year": 2023, "source": "instagram"})


print("\n🔍 Searching similar claims...\n")

results = search_claims("fake flood photo in delhi")

for r in results:
    print(r.payload, " | score:", r.score)
