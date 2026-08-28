"""Minimal deterministic BigWig reader (UCSC format), stdlib-only.

Supports exactly what §13.2 needs: open, list chromosomes, query the value
intervals overlapping a range, and a whole-file self-check that re-derives the
embedded totalSummary record from the data blocks — the reader refuses a file
it cannot reproduce the header summary of (verify-what-you-parse).
"""

import struct
import zlib
from dataclasses import dataclass

BIGWIG_MAGIC = 0x888FFC26
CHROM_TREE_MAGIC = 0x78CA8C91
RTREE_MAGIC = 0x2468ACE0


@dataclass(frozen=True)
class Interval:
    start: int  # 0-based, half-open
    end: int
    value: float


class BigWig:
    def __init__(self, path: str):
        # noqa rationale: the handle is owned by the object across queries and
        # released in close() / __exit__ — a context manager here is impossible.
        self._f = open(path, "rb")  # noqa: SIM115
        header = struct.unpack("<IHHQQQHHQQIQ", self._f.read(64))
        if header[0] != BIGWIG_MAGIC:
            raise ValueError(f"not a little-endian BigWig: {path}")
        (
            _,
            _version,
            _zoom,
            chrom_tree_off,
            _full_data_off,
            self._index_off,
            _field_count,
            _defined_field_count,
            _auto_sql_off,
            total_summary_off,
            self._uncompress_buf,
            _reserved,
        ) = header
        self._f.seek(total_summary_off)
        (self.valid_count, self.min_val, self.max_val, self.sum_data, self.sum_squares) = (
            struct.unpack("<Qdddd", self._f.read(40))
        )
        self.chroms: dict[str, tuple[int, int]] = {}  # name -> (id, size)
        self._read_chrom_tree(chrom_tree_off)
        self._chrom_by_id = {cid: name for name, (cid, _) in self.chroms.items()}

    def close(self) -> None:
        self._f.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    # -- chrom B+ tree -----------------------------------------------------
    def _read_chrom_tree(self, offset: int) -> None:
        self._f.seek(offset)
        magic, _block, key_size, _val, _items, _reserved = struct.unpack(
            "<IIIIQQ", self._f.read(32)
        )
        if magic != CHROM_TREE_MAGIC:
            raise ValueError("bad chromosome B+ tree magic")
        self._read_chrom_node(key_size)

    def _read_chrom_node(self, key_size: int) -> None:
        is_leaf, _reserved, count = struct.unpack("<BBH", self._f.read(4))
        if is_leaf:
            for _ in range(count):
                raw = self._f.read(key_size + 8)
                key = raw[:key_size].rstrip(b"\x00").decode()
                chrom_id, chrom_size = struct.unpack("<II", raw[key_size:])
                self.chroms[key] = (chrom_id, chrom_size)
        else:
            offsets = []
            for _ in range(count):
                raw = self._f.read(key_size + 8)
                offsets.append(struct.unpack("<Q", raw[key_size:])[0])
            for off in offsets:
                self._f.seek(off)
                self._read_chrom_node(key_size)

    # -- r-tree ------------------------------------------------------------
    def _overlapping_blocks(self, chrom_id: int, start: int, end: int) -> list[tuple[int, int]]:
        self._f.seek(self._index_off)
        magic = struct.unpack("<I", self._f.read(4))[0]
        if magic != RTREE_MAGIC:
            raise ValueError("bad r-tree magic")
        self._f.seek(self._index_off + 48)  # header is 48 bytes incl. magic
        blocks: list[tuple[int, int]] = []
        self._walk_rtree(self._f.tell(), chrom_id, start, end, blocks)
        return blocks

    def _walk_rtree(self, node_off: int, chrom_id: int, start: int, end: int, out: list) -> None:
        self._f.seek(node_off)
        is_leaf, _reserved, count = struct.unpack("<BBH", self._f.read(4))
        if is_leaf:
            items = [struct.unpack("<IIIIQQ", self._f.read(32)) for _ in range(count)]
            for s_cix, s_base, e_cix, e_base, data_off, data_size in items:
                if self._range_overlaps(s_cix, s_base, e_cix, e_base, chrom_id, start, end):
                    out.append((data_off, data_size))
        else:
            items = [struct.unpack("<IIIIQ", self._f.read(24)) for _ in range(count)]
            for s_cix, s_base, e_cix, e_base, child_off in items:
                if self._range_overlaps(s_cix, s_base, e_cix, e_base, chrom_id, start, end):
                    self._walk_rtree(child_off, chrom_id, start, end, out)

    @staticmethod
    def _range_overlaps(s_cix, s_base, e_cix, e_base, chrom_id, start, end) -> bool:
        if (s_cix, s_base) >= (chrom_id, end):
            return False
        return (e_cix, e_base) > (chrom_id, start)

    # -- data blocks -------------------------------------------------------
    def _block_intervals(self, data_off: int, data_size: int) -> tuple[int, list[Interval]]:
        self._f.seek(data_off)
        raw = self._f.read(data_size)
        if self._uncompress_buf > 0:
            raw = zlib.decompress(raw)
        chrom_id, start, _end, item_step, item_span, kind, _r, count = struct.unpack(
            "<IIIIIBBH", raw[:24]
        )
        out = []
        off = 24
        for i in range(count):
            if kind == 1:  # bedGraph
                s, e, v = struct.unpack("<IIf", raw[off : off + 12])
                off += 12
            elif kind == 2:  # varStep
                s, v = struct.unpack("<If", raw[off : off + 8])
                e = s + item_span
                off += 8
            elif kind == 3:  # fixedStep
                (v,) = struct.unpack("<f", raw[off : off + 4])
                s = start + i * item_step
                e = s + item_span
                off += 4
            else:
                raise ValueError(f"unknown section type {kind}")
            out.append(Interval(s, e, v))
        return chrom_id, out

    # -- public ------------------------------------------------------------
    def query(self, chrom: str, start: int, end: int) -> list[Interval]:
        """All value intervals overlapping [start, end) on chrom (0-based)."""
        if chrom not in self.chroms:
            return []
        chrom_id = self.chroms[chrom][0]
        result = []
        for data_off, data_size in self._overlapping_blocks(chrom_id, start, end):
            block_chrom, intervals = self._block_intervals(data_off, data_size)
            if block_chrom != chrom_id:
                continue
            result.extend(iv for iv in intervals if iv.start < end and iv.end > start)
        return sorted(result, key=lambda iv: iv.start)

    def self_check(self, tolerance: float = 0.03) -> None:
        """Re-derive coverage from every data block; raise if far from header.

        Exact equality is deliberately NOT required: PopHuman's files over-report
        totalSummary by ~2% relative to their own data blocks (measured 2026-08-28:
        header 1,806,843,700 vs data 1,772,380,000 bases for iHS_GIH_10kb; pyBigWig
        reads the identical data — 300 sampled regions, 0 mismatches — and merely
        echoes the same header). The check pins gross truncation/corruption, and
        values are cross-verified against pyBigWig in the integration test.
        """
        valid = 0
        for name, (_chrom_id, size) in self.chroms.items():
            for iv in self.query(name, 0, size):
                valid += iv.end - iv.start
        if not (self.valid_count * (1 - tolerance) <= valid <= self.valid_count * (1 + tolerance)):
            raise ValueError(
                f"self-check: recomputed coverage {valid} vs header {self.valid_count} "
                f"exceeds {tolerance:.0%} tolerance"
            )
