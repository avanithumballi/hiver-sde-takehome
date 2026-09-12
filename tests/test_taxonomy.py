from src.taxonomy import INTENTS

def test_taxonomy_has_eight_intents():
    assert len(INTENTS) == 8
    assert "unclear" in INTENTS
