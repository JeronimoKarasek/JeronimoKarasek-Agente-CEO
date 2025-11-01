from __future__ import annotations

def score_preflight(duration_s: float | None = None, hook_ms: int | None = None, cta_present: bool | None = None, readability: float | None = None) -> float:
    score = 0.0
    if duration_s is not None:
        # Prefer 20-35s
        if 20 <= duration_s <= 35:
            score += 0.4
        else:
            score += 0.2
    if hook_ms is not None:
        if hook_ms <= 2000:
            score += 0.2
        else:
            score += 0.05
    if cta_present:
        score += 0.2
    if readability is not None:
        score += max(0.0, min(readability, 1.0)) * 0.2
    return round(min(score, 1.0), 2)

