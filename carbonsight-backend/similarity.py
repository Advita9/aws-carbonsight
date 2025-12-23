# similarity.py
import math

def cosine_similarity(vec1, vec2):
    """
    Compute cosine similarity between two numeric vectors.
    vec1 and vec2 are lists of Decimals → convert to float for math.
    """
    v1 = [float(x) for x in vec1]
    v2 = [float(x) for x in vec2]

    dot = sum(a * b for a, b in zip(v1, v2))
    mag1 = math.sqrt(sum(a * a for a in v1))
    mag2 = math.sqrt(sum(b * b for b in v2))

    if mag1 == 0 or mag2 == 0:
        return 0.0

    return dot / (mag1 * mag2)
