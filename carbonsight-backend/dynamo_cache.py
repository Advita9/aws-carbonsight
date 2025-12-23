import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal
import hashlib
import os

from similarity import cosine_similarity

dynamodb = boto3.resource("dynamodb")
CACHE_TABLE = os.environ.get("CACHE_TABLE_NAME")
table = dynamodb.Table(CACHE_TABLE)

# Semantic threshold — can tune over time
SIMILARITY_THRESHOLD = 0.82


def hash_prompt(prompt: str) -> str:
    """
    SHA256 hash — remains the primary key.
    """
    return hashlib.sha256(prompt.encode()).hexdigest()


def save_to_cache(prompt: str, embedding, response: str, model: str):
    """
    Store a fully computed result in DynamoDB.
    embedding is a list of Decimal numbers.
    """

    prompt_hash = hash_prompt(prompt)

    entry = {
        "promptHash": prompt_hash,
        "prompt": prompt,
        "embedding": embedding,      # already converted to Decimal in lambda_handler
        "response": response,
        "model": model
    }

    table.put_item(Item=entry)


def find_all_cached_items():
    """
    Full table scan — works for now.
    Upgrade later using GSI or vector DB.
    """
    resp = table.scan()
    return resp.get("Items", [])


def find_similar_prompt(query_embedding):
    """
    Full semantic similarity search.

    Steps:
    1. Fetch all cached entries (scan)
    2. Compute cosine similarity with query embedding
    3. Pick highest similarity above threshold
    4. If match found → return cached record
    """

    items = find_all_cached_items()

    if not items:
        print("Semantic cache: EMPTY")
        return None

    best_similarity = 0
    best_match = None

    # Convert query embedding (list of Decimals) to floats
    query_vec = [float(x) for x in query_embedding]

    for item in items:
        cached_vec = [float(x) for x in item["embedding"]]

        sim = cosine_similarity(query_vec, cached_vec)

        if sim > best_similarity:
            best_similarity = sim
            best_match = item

    # Debug logging
    print("Semantic similarity:", best_similarity)

    if best_similarity >= SIMILARITY_THRESHOLD:
        print("Semantic cache HIT!")
        return {
            "response": best_match["response"],
            "model": best_match["model"]
        }

    print("Semantic cache MISS")
    return None



