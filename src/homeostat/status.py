"""Pull pipeline progress from the filesystem: `make status` (or --json).

Read-only; derives everything from artifacts, so it is always safe to run,
including while the pipeline or download is mid-flight.
"""

import json
import sys

from homeostat.paths import (
    AUTOSOMES,
    CANDIDATES,
    GENOTYPE_RAW,
    SCAN_PROGRESS,
    SHARDS,
    SITES_VCF,
    SITES_VCF_EXPECTED,
    SITES_VCF_PART,
    SUMMARY,
)


def collect() -> dict:
    expected = int(SITES_VCF_EXPECTED.read_text().strip()) if SITES_VCF_EXPECTED.exists() else None
    if SITES_VCF.exists():
        download = {"state": "complete", "bytes": SITES_VCF.stat().st_size}
    elif SITES_VCF_PART.exists():
        got = SITES_VCF_PART.stat().st_size
        download = {
            "state": "downloading",
            "bytes": got,
            "expected": expected,
            "pct": round(100 * got / expected, 1) if expected else None,
        }
    else:
        download = {"state": "not started"}

    done = [c for c in AUTOSOMES if (SHARDS / f"chr{c}.done").exists()]
    matched = 0
    for c in done:
        matched += json.loads((SHARDS / f"chr{c}.done").read_text()).get("matched", 0)
    scan_state = {
        "chroms_done": f"{len(done)}/{len(AUTOSOMES)}",
        "done": done,
        "matched_in_done_shards": matched,
    }
    if SCAN_PROGRESS.exists():
        scan_state["live"] = json.loads(SCAN_PROGRESS.read_text())

    if SUMMARY.exists():
        s = json.loads(SUMMARY.read_text())
        rank_state = {
            "state": "complete",
            "candidates_total": s["candidates_total"],
            "candidates_priority_gt0": s["candidates_priority_gt0"],
            "completed": s["completed"],
        }
    else:
        rank_state = {"state": "complete" if CANDIDATES.exists() else "pending"}

    return {
        "genotype_local": GENOTYPE_RAW.exists(),
        "download": download,
        "scan": scan_state,
        "rank": rank_state,
    }


def main() -> None:
    status = collect()
    if "--json" in sys.argv:
        print(json.dumps(status, indent=2))
        return
    print("Homeostat §13.1 E/I/R filter — status")
    print(f"  genotype copied : {status['genotype_local']}")
    d = status["download"]
    extra = f" ({d.get('pct')}%)" if d.get("pct") is not None else ""
    print(f"  1000G sites vcf : {d['state']}{extra}")
    s = status["scan"]
    print(
        f"  scan            : {s['chroms_done']} chroms, "
        f"{s['matched_in_done_shards']} sites matched in finished shards"
    )
    if "live" in s:
        live = s["live"]
        print(
            f"                    live: chrom {live['current_chrom']}, "
            f"{live['lines_scanned']:,} lines, updated {live['updated']}"
        )
    r = status["rank"]
    line = f"  rank            : {r['state']}"
    if r.get("candidates_total") is not None:
        line += (
            f" — {r['candidates_total']} candidates, "
            f"{r['candidates_priority_gt0']} with priority > 0"
        )
    print(line)


if __name__ == "__main__":
    main()
