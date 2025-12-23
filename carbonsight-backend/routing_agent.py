import os
from bedrock_client import invoke_nova
from carbon_agent import predict_energy_cost, should_downgrade

# ONLY supported Nova models
NOVA_MICRO = os.environ.get("NOVA_MICRO_ID")
NOVA_LITE = os.environ.get("NOVA_LITE_ID")
NOVA_PRO = os.environ.get("NOVA_PRO_ID")

def classify_complexity(prompt: str) -> str:

    classification_prompt = f"""
You are a classifier. Categorize the following task into one of four levels:
simple, medium, complex, very complex.

Task: "{prompt}"

Respond with ONLY one word.
"""

    raw = invoke_nova(NOVA_MICRO, classification_prompt, max_tokens=5)
    raw = raw.strip().lower()

    if "simple" in raw:
        return "simple"
    if "medium" in raw:
        return "medium"
    if "very" in raw:
        return "very complex"
    if "complex" in raw:
        return "complex"

    return "medium"


def select_model(complexity: str, predicted_tokens=300):
    """
    Energy-aware routing.
    Chooses the greenest model that still satisfies the reasoning requirement.
    """

    # Nova-2-lite removed entirely — safe models only
    candidates = {
        "simple": [NOVA_MICRO, NOVA_LITE],
        "medium": [NOVA_MICRO, NOVA_LITE],
        "complex": [NOVA_LITE, NOVA_PRO],
        "very complex": [NOVA_PRO]
    }

    options = candidates.get(complexity, [NOVA_LITE])

    # score each candidate
    scored = []
    for model_id in options:
        prediction = predict_energy_cost(model_id, predicted_tokens)
        scored.append((model_id, prediction["efficiency_score"], prediction))

    # pick the highest-efficiency model
    scored.sort(key=lambda x: x[1], reverse=True)
    best_model, _, prediction = scored[0]

    # downgrade if needed
    if should_downgrade(prediction["predicted_kwh"]):
        return options[0]  # smallest model in category

    return best_model




