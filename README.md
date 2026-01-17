# 🧠 SatyaAI — Digital Trust Memory System  
A Multimodal Long-Term Misinformation Memory Engine built on Qdrant

---

## 📌 Overview

SatyaAI is a multimodal digital trust memory system designed to combat long-term and resurfacing misinformation.

Unlike traditional fact-checkers or chatbots that analyze content in isolation, SatyaAI is built as a persistent narrative intelligence engine. It stores and retrieves historical claims, images, and videos to detect how misinformation narratives evolve, resurface, and spread across time and platforms.

SatyaAI does not declare content “true” or “false.”  
Instead, it provides evidence-based historical memory so that journalists, researchers, and institutions can make informed decisions.

---

## 🎯 Problem Statement

Misinformation does not disappear after being debunked.  
It resurfaces during elections, disasters, pandemics, and social crises — often with minor wording changes or reused visuals.

Examples:
- Old flood images reshared as new disasters  
- Debunked vaccine rumors resurfacing every few years  
- The same political narratives recycled across platforms  

Current AI systems lack long-term memory. They repeatedly rediscover the same misinformation because they cannot remember what has already happened.

SatyaAI reframes misinformation as a memory and narrative intelligence problem.

---

## 💡 What SatyaAI Solves

SatyaAI enables:

- Long-term storage of misinformation narratives  
- Multimodal retrieval across text, images, and video  
- Detection of resurfacing and recurring narratives  
- Historical reconstruction of how claims evolve  
- Evidence-grounded trust reports  

This transforms misinformation handling from reactionary fact-checking into proactive narrative intelligence.

---

## 🏗 System Architecture

SatyaAI follows a layered multimodal memory architecture:

1. User Interface (Streamlit Dashboard)  
2. Multimodal Ingestion Layer (Text, Image, Video)  
3. Embedding Layer (Sentence Transformers, CLIP, Video Frames)  
4. Vector Memory Core (Qdrant)  
5. Narrative Intelligence Layer  
6. Evidence-Based Output Layer  

All system intelligence is retrieval-driven and grounded in stored evidence.

---

## 🧠 Why Qdrant is Central

Qdrant is used as the primary long-term vector memory system.

It enables:
- High-dimensional semantic similarity search  
- Multimodal vector storage  
- Structured payload filtering  
- Narrative-level grouping  
- Scalable persistent memory  

SatyaAI does not use Qdrant as simple storage — it is the core cognitive substrate of the system.

---

## 🔀 Multimodal Strategy

SatyaAI supports three primary modalities:

Text  
- Semantic embedding of claims  
- Detects paraphrased and mutated narratives  

Images  
- Visual similarity search  
- Detects reused or slightly modified images  

Video  
- Videos are decomposed into frames  
- Frames are embedded as visual memory  
- Enables resurfacing detection even when full videos change  

Each memory item stores metadata including narrative_id, year, source, and type.

---

## 🧩 Memory Beyond a Single Prompt

SatyaAI implements true long-term memory.

Narratives are persistent objects that evolve over time.  
New inputs either reinforce an existing narrative or create a new narrative.

The system separates:

- Knowledge memory (stored narratives)  
- Interaction context (user queries)  
- System intelligence (risk scoring and resurfacing logic)  

---

## 🔍 Retrieval, Memory & Recommendation Logic

1. New content is embedded  
2. Qdrant similarity search retrieves nearest memories  
3. High similarity links to an existing narrative  
4. Low similarity creates a new narrative  
5. Trust reports aggregate narrative-level evidence  

Outputs include:
- occurrence counts  
- first/last seen dates  
- platform diffusion  
- resurfacing alerts  
- historical timelines  

All outputs are traceable to retrieved records.

---

## ⚖ Ethics, Responsibility & Limitations

SatyaAI is a decision-support system, not an authority.

Principles:
- No automated truth labeling  
- Evidence-first outputs  
- Human-in-the-loop analysis  
- Transparency of retrieved data  
- Privacy-aware payload design  

Limitations:
- Embedding bias  
- Partial visual matches  
- Incomplete datasets  

Future improvements:
- Audio ingestion  
- Narrative decay modeling  
- Multilingual memory  
- Influence network analysis  

---

## 🖥 User Interface

The SatyaAI dashboard provides:

- Narrative system metrics  
- Claim analysis and trust reports  
- Image investigation and reuse detection  
- Video memory ingestion  
- Narrative memory explorer  
- Memory distribution analytics  

Designed for journalists, researchers, and public institutions.

---

## 🔍 Demo & Examples

Example 1 – Claim resurfacing

Input:
Old vaccine infertility rumor resurfaces

Output:
- Narrative ID  
- Occurrences  
- Risk Level  
- First and last seen  
- Platform history  

---

Example 2 – Image reuse

Input:
Uploaded flood image

Output:
- Linked narrative  
- Similar historical visuals  
- Visual reuse detected  

---

Example 3 – Narrative exploration

Action:
Open “Explore Narratives” tab

Output:
- Narrative clusters  
- Timeline reconstruction  
- Multimodal memory

---

Screenshots available in:

demo/screenshots/

---

## ⚙ Setup Instructions

1. Clone repository  
git clone <repo-link>  
cd SatyaAI  

2. Create virtual environment  
python -m venv venv  
venv\Scripts\activate  

3. Install dependencies  
pip install -r requirements.txt  

4. Initialize Qdrant  
python -m core.qdrant.schema  

5. Run application  
streamlit run ui/app.py  

---

## 📦 Tech Stack

Python  
Streamlit  
Qdrant  
Sentence Transformers  
CLIP  
OpenCV  
Matplotlib  

---

## 🏁 Conclusion

SatyaAI demonstrates how multimodal vector memory can serve as long-term societal infrastructure rather than short-lived assistants.

By integrating Qdrant-powered retrieval, narrative intelligence, and evidence-based outputs, SatyaAI enables historically grounded digital trust systems.
