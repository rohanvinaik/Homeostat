"""Intent tests for the genotype consequence vector (design A, dense): the structural-consequence
axis (`class_shift`, `structural_consequence`), the biophysics delta (`biophysics_consequence`),
the assembled `consequence_vector`, and the fungibility read (`consequence_similarity`, cosine).
Paired with the Detective characterization per the two-step.
"""

from homeostat.consequence import (
    _delta,
    biophysics_consequence,
    class_shift,
    consequence_similarity,
    consequence_vector,
    structural_consequence,
)

_AA = "MKLVAAGGSSTTPPFFYYWW"  # 20 residues (>= TM_WINDOW so structural_class is defined)


def test_class_shift_ranks_the_structural_change():
    assert class_shift("membrane", "membrane") == 0.0  # same class
    assert class_shift("membrane", "soluble") == 1.0  # confident FLIP -- the biggest change
    assert class_shift("soluble", "membrane") == 1.0  # symmetric
    assert class_shift("membrane", "uncertain") == 0.5  # partial (one side abstains)
    assert class_shift("uncertain", "soluble") == 0.5
    assert class_shift("uncertain", "uncertain") == 0.0


def test_structural_consequence_identical_is_all_zeros():
    assert structural_consequence(_AA, _AA) == (0.0, 0.0, 0.0, 0.0, 0.0)


def test_structural_consequence_measures_the_change():
    # all-Ala -> all-Lys: composition fully disjoint; charge neutral -> all-positive; gravy shifts.
    _cshift, comp, dgravy, dcharge, _darom = structural_consequence("A" * 20, "K" * 20)
    assert comp == 2.0  # composition L1 distance: fully disjoint = maximal
    assert dcharge == 1.0  # net charge 0 (all A) -> +1 (all K)
    assert dgravy > 0  # A hydrophobic (+1.8) -> K hydrophilic (-3.9)


def test_delta_is_abs_difference_or_zero_on_missing():
    assert _delta(1.0, 0.5) == 0.5  # both present -> |diff|
    assert _delta(None, 0.2) == 0.0  # missing ref -> informational zero
    assert _delta(0.5, None) == 0.0  # missing var -> informational zero


def test_biophysics_consequence_identical_is_zero():
    assert biophysics_consequence("ATAT", "ATAT") == (0.0, 0.0)


def test_biophysics_consequence_measures_the_phase_flip():
    # "TA" (YR, balance +1) vs "AT" (RY, balance -1): same bendability, YR/RY balance flips -> 2.0.
    assert biophysics_consequence("TA", "AT") == (0.0, 2.0)


def test_consequence_vector_shape_and_zero():
    v = consequence_vector(_AA, _AA, "ATAT", "ATAT", 0.3)
    assert len(v) == 8  # 5 structural + 2 biophysics + 1 rarity
    assert v == (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3)  # no consequence, only the rarity gate


def test_consequence_similarity_is_fungibility_by_direction():
    assert consequence_similarity((1.0, 2.0, 3.0), (1.0, 2.0, 3.0)) == 1.0  # identical -> fungible
    assert consequence_similarity((1.0, 2.0, 3.0), (2.0, 4.0, 6.0)) == 1.0  # proportional
    assert consequence_similarity((1.0, 0.0), (0.0, 1.0)) == 0.0  # orthogonal -> not fungible
    assert consequence_similarity((0.0, 0.0), (1.0, 1.0)) == 0.0  # zero vector -> no direction
