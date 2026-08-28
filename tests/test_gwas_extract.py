"""Intent test for the exact-match trait filter."""

from homeostat.gwas_extract import trait_matches


def test_exact_single_trait_only():
    assert trait_matches("leprosy", "leprosy")
    assert trait_matches("Crohn disease", "crohns")
    assert trait_matches("inflammatory bowel disease", "ibd")
    # co-mapped / compound rows are NOT a match for either component
    assert not trait_matches("Crohn disease, leprosy", "leprosy")
    assert not trait_matches("Crohn disease, leprosy", "crohns")
    assert not trait_matches("ulcerative colitis, Crohn disease", "crohns")
    assert trait_matches("  leprosy  ", "leprosy")  # whitespace tolerated
    assert not trait_matches("  leprosy  ", "crohns")
