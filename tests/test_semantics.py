def test_semantic_module_import():
    from app.semantic_matcher import semantic_score_percent
    s = semantic_score_percent("python pandas", "looking for python developer")
    assert isinstance(s, float)
    assert 0.0 <= s <= 100.0
