import os
from bedrock_client import embed_text
from dynamo_cache import find_similar_prompt  # NEW semantic lookup

def embedding_agent(prompt: str):
    """
    Generates embedding for the prompt,
    then performs semantic cache lookup using the new optimized function.
    """

    # 1. Generate embedding via Bedrock
    embedding = embed_text(prompt)

    # 2. Perform semantic lookup from DynamoDB
    cached = find_similar_prompt(embedding)

    if cached:
        return {
            "cached": True,
            "cachedFrom": "semantic-cache",
            "response": cached["response"],
            "modelUsed": cached["model"]
        }

    # 3. No semantic match
    return {
        "cached": False,
        "embedding": embedding
    }



