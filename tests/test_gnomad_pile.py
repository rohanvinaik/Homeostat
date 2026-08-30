"""Intent tests for the gnomAD v2.1.1 exome pile parser, pinned from the REAL
INFO format (anchored keys, AN=0 -> AF absent, PASS-only, scientific notation)."""

from homeostat.gnomad_pile import info_get, parse_line, pile_row

# A realistic PASS line with all three ancestry AF/AN present.
_PASS = (
    "1\t100\trs1\tG\tA\t.\tPASS\t"
    "AC=5;AN=1000;AF=5.0e-03;AC_sas=3;AN_sas=200;AF_sas=1.5e-02;"
    "AC_nfe=2;AN_nfe=500;AF_nfe=4.0e-03;AC_eas=0;AN_eas=100;AF_eas=0.0e+00;"
    "controls_AF_sas=9.9e-01;AF_sas_male=1.0e-02"
)


def test_info_get_is_field_anchored():
    info = _PASS.split("\t")[7]
    # must return the real AF_sas, NOT controls_AF_sas or AF_sas_male
    assert info_get(info, "AF_sas") == "1.5e-02"
    assert info_get(info, "AN_sas") == "200"
    assert info_get(info, "AF_eas") == "0.0e+00"
    assert info_get(info, "MISSING") is None


def test_parse_pass_line_extracts_three_pops():
    rec = parse_line(_PASS)
    assert rec is not None
    chrom, pos, ref, alt, af_sas, af_nfe, af_eas, an_sas, an_nfe, an_eas = rec
    assert (chrom, pos, ref, alt) == ("1", "100", "G", "A")
    assert af_sas == 0.015 and af_nfe == 0.004 and af_eas == 0.0
    assert (an_sas, an_nfe, an_eas) == (200, 500, 100)


def test_non_pass_dropped():
    assert parse_line(_PASS.replace("\tPASS\t", "\tAC0\t")) is None


def test_an_zero_missing_af_dropped():
    # the real gnomAD shape: AN_sas=0 and AF_sas absent -> not evaluable
    line = (
        "1\t12198\t.\tG\tC\t.\tPASS\t"
        "AC_sas=0;AN_sas=0;AN_nfe=500;AF_nfe=1e-02;AN_eas=100;AF_eas=1e-02"
    )
    assert parse_line(line) is None


def test_focal_monomorphic_dropped():
    # SAS AF exactly 0 -> no branch signal in the focal pop
    line = (
        "1\t100\t.\tG\tA\t.\tPASS\t"
        "AN_sas=200;AF_sas=0.0e+00;AN_nfe=500;AF_nfe=4e-03;AN_eas=100;AF_eas=1e-02"
    )
    assert parse_line(line) is None


def test_non_autosome_dropped():
    assert parse_line(_PASS.replace("1\t100", "X\t100", 1)) is None


def test_pile_row_order_and_pbs_nonnegative_shape():
    rec = parse_line(_PASS)
    row, p, chrom, pos = pile_row(rec)
    cols = row.rstrip("\n").split("\t")
    # column order must match eir_cohort: chrom,pos,ref,alt,af,af,af,maf,fst,pbs
    assert cols[0] == "1" and cols[1] == "100" and cols[2] == "G" and cols[3] == "A"
    assert len(cols) == 10
    assert chrom == "1" and pos == 100
    assert cols[7] == f"{min(0.015, 0.985):.4f}"  # maf_sas
    assert isinstance(p, float)
