#!/usr/bin/env python3

def cosineSimilarity(vec1, vec2):
    """
    Calculate cosine similarity between two vectors.

    Args:
        vec1: First vector (list or array of numbers)
        vec2: Second vector (list or array of numbers)

    Returns:
        float: Cosine similarity value between -1 and 1
    """
    # Calculate dot product
    dot_product = sum(a * b for a, b in zip(vec1, vec2))

    # Calculate magnitudes
    magnitude1 = sum(a * a for a in vec1) ** 0.5
    magnitude2 = sum(b * b for b in vec2) ** 0.5

    # Avoid division by zero
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0

    # Calculate cosine similarity
    return dot_product / (magnitude1 * magnitude2)
