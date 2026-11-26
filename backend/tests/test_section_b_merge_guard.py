import pytest


def merge_with_collision_guard(parts: list[dict]) -> dict:
    merged: dict = {}
    for idx, part in enumerate(parts, start=1):
        conflict_keys = set(merged.keys()) & set(part.keys())
        if conflict_keys:
            raise ValueError(f"B{idx} 병합 중 키 충돌 감지: {sorted(conflict_keys)}")
        merged.update(part)
    return merged


def test_merge_guard_raises_on_conflict() -> None:
    p1 = {"same": 1, "a": 1}
    p2 = {"same": 2, "b": 2}
    with pytest.raises(ValueError):
        merge_with_collision_guard([p1, p2])
