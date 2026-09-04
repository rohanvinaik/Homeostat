"""Intent tests for the genotype consequence vector's structural-consequence axis (axis 1):
`class_shift` and `structural_consequence`. Paired with the Detective characterization per the
two-step.
"""

from homeostat.consequence import class_shift, structural_consequence


def test_class_shift_ranks_the_structural_change():
    assert class_shift("membrane", "membrane") == 0.0  # same class
    assert class_shift("membrane", "soluble") == 1.0  # confident FLIP -- the biggest change
    assert class_shift("soluble", "membrane") == 1.0  # symmetric
    assert class_shift("membrane", "uncertain") == 0.5  # partial (one side abstains)
    assert class_shift("uncertain", "soluble") == 0.5
    assert class_shift("uncertain", "uncertain") == 0.0


def test_structural_consequence_identical_is_all_zeros():
    aa = "MKLVAAGGSSTTPPFFYYWW"  # 20 residues (>= TM_WINDOW so structural_class is defined)
    assert structural_consequence(aa, aa) == (0.0, 0.0, 0.0, 0.0, 0.0)


def test_structural_consequence_measures_the_change():
    # all-Ala -> all-Lys: composition fully disjoint; charge neutral -> all-positive; gravy shifts.
    _cshift, comp, dgravy, dcharge, _darom = structural_consequence("A" * 20, "K" * 20)
    assert comp == 2.0  # composition L1 distance: fully disjoint = maximal
    assert dcharge == 1.0  # net charge 0 (all A) -> +1 (all K)
    assert dgravy > 0  # A hydrophobic (+1.8) -> K hydrophilic (-3.9)
