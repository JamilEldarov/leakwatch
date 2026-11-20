"""Explainable hackathon scoring (heuristic, not validated threat intelligence)."""
from app.detector import Entity

BASE = {"domain": 25, "username": 40, "email": 60, "document_marker": 70}


def score_finding(entity: Entity, text: str, all_entities: list[Entity]) -> tuple[int, str, str]:
    score = BASE[entity.kind]
    reasons = [f"{entity.kind} indicator"]
    kinds = {e.kind for e in all_entities}
    if "document_marker" in kinds and entity.kind != "document_marker":
        score += 15
        reasons.append("document-related marker in same post")
    if len(kinds) >= 3:
        score += 10
        reasons.append("multiple indicator types")
    if any(word in text.lower() for word in ("password", "passwd", "api_key", "secret=")):
        score += 15
        reasons.append("credential-related keyword (not validated)")
    score = min(score, 100)
    level = "HIGH" if score >= 75 else "MEDIUM" if score >= 45 else "LOW"
    return score, level, "; ".join(reasons)
