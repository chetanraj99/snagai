
from sentence_transformers import SentenceTransformer, util  # type: ignore

# Load DistilBERT model
model = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight BERT variant

# Historical snag reports
# descriptions = [
#     "Cracked wall near the staircase",
#     "Broken pipe in the bathroom",
#     "Peeling paint in the living room"
# ]
# solutions = [
#     "Repair the crack and repaint.",
#     "Replace the pipe with a new one.",
#     "Scrape off old paint and repaint."
# ]

descriptions = [
    "Engine producing unusual noise during operation",
    "Landing gear not retracting properly",
    "Cabin pressurization system malfunctioning",
    "Navigation system showing incorrect coordinates",
    "Fuel leakage detected in the left wing",
    "Crack observed on the tail section of engine",
    "Faulty communication noise system between cockpit and ATC",
    "Hydraulic fluid levels lower than normal",
    "Flaps not responding during takeoff and landing",
    "Warning lights blinking intermittently on the dashboard"
]

solutions = [
    "Inspect the engine and perform necessary repairs or replacements.",
    "Check landing gear hydraulic systems and repair or replace malfunctioning components.",
    "Diagnose the pressurization system and fix leaks or replace faulty components.",
    "Recalibrate or replace the navigation system.",
    "Inspect and repair the fuel system, replacing damaged components as needed.",
    "Conduct structural analysis and repair or replace the damaged section.",
    "Check and repair communication equipment or wiring as necessary.",
    "Refill hydraulic fluid and inspect for leaks or system malfunctions.",
    "Diagnose and repair the flaps' control system or actuators.",
    "Investigate the electrical system and replace faulty sensors or wiring."
]

# Generate embeddings for the descriptions
description_embeddings = model.encode(descriptions)

# User query
# query = "An abnormal noise is being produced by the machine during operation."
# query="The engine is emitting an unusual sound while running."
# query="The engine generates an unexpected sound when in use."
query = "noise"
query_embedding = model.encode(query)

# Compute similarity
similarities = util.cos_sim(query_embedding, description_embeddings).flatten()

# Find the best match
best_match_index = similarities.argmax()
recommended_solution = solutions[best_match_index]
print(f"Matched Query: {descriptions[best_match_index]}")
print(f"Recommended Solution: {recommended_solution}")
