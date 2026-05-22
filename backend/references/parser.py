"""RIS 和 BibTeX 文献格式解析器。"""

import re
from pathlib import Path


# ─── RIS 解析 ─────────────────────────────────────────────────────

RIS_TAG_MAP = {
    "TI": "title",
    "T1": "title",
    "CT": "title",
    "AU": "authors",
    "A1": "authors",
    "PY": "year",
    "Y1": "year",
    "JO": "journal",
    "JF": "journal",
    "JA": "journal",
    "VL": "volume",
    "IS": "number",
    "SP": "pages",
    "EP": "pages_end",
    "DO": "doi",
    "AB": "abstract",
    "N2": "abstract",
    "KW": "keywords",
    "UR": "url",
    "L1": "url",
    "TY": "ref_type",
    "SN": "issn",
    "M3": "doi",
}

RIS_TYPE_MAP = {
    "JOUR": "article",
    "BOOK": "book",
    "CONF": "conference",
    "CHAP": "chapter",
    "THES": "thesis",
    "GEN": "generic",
    "RPRT": "report",
    "ELEC": "webpage",
    "PAT": "patent",
}


def parse_ris(text: str) -> list[dict]:
    """解析 RIS 格式文本，返回文献字典列表。"""
    refs = []
    current = {}
    pages_start = None

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        # 检测记录结束
        if line.upper().startswith("ER  -"):
            if current:
                # 处理 pages
                if pages_start and current.get("pages_end"):
                    current["pages"] = f"{pages_start}-{current['pages_end']}"
                elif pages_start:
                    current["pages"] = pages_start
                refs.append(current)
                current = {}
                pages_start = None
            continue

        if len(line) < 6:
            continue
        tag = line[:2].upper().strip()
        # RIS 格式: "TY  - JOUR" — 去掉标签后的空格、短横、空格
        value = line[3:].lstrip("- ").strip()

        field = RIS_TAG_MAP.get(tag)
        if not field:
            if tag == "EP":
                current["pages_end"] = value
            continue

        if field == "authors":
            current.setdefault("authors", []).append(value)
        elif field == "keywords":
            current.setdefault("keywords", []).append(value)
        elif field == "ref_type":
            current["ref_type"] = RIS_TYPE_MAP.get(value.upper(), value.lower())
        elif field == "pages":
            pages_start = value
        elif field == "year":
            # 提取 4 位年份
            m = re.search(r"\b(\d{4})\b", value)
            if m:
                current["year"] = m.group(1)
        else:
            if field not in current:  # 第一个值优先
                current[field] = value

    # 处理文件末尾可能没有 ER 的情况
    if current:
        refs.append(current)

    return refs


# ─── BibTeX 解析 ──────────────────────────────────────────────────

BIB_TYPE_MAP = {
    "article": "article",
    "book": "book",
    "inproceedings": "conference",
    "incollection": "chapter",
    "phdthesis": "thesis",
    "mastersthesis": "thesis",
    "techreport": "report",
    "misc": "generic",
}


def parse_bibtex(text: str) -> list[dict]:
    """解析 BibTeX 格式文本，返回文献字典列表。"""
    refs = []
    # 匹配每个条目: @type{key, ... }
    entries = re.findall(
        r"@(\w+)\s*\{\s*([^,]+)\s*,([^@]*)\}",
        text,
        re.IGNORECASE | re.DOTALL,
    )

    for bib_type, bib_key, body in entries:
        ref: dict = {
            "ref_type": BIB_TYPE_MAP.get(bib_type.lower(), "generic"),
            "bib_key": bib_key.strip(),
        }

        # 提取字段:  field = {value} 或 field = "value"
        fields = re.findall(
            r"(\w+)\s*=\s*\{([^}]*)\}|(\w+)\s*=\s*\"([^\"]*)\"",
            body,
            re.IGNORECASE,
        )
        for f1, v1, f2, v2 in fields:
            fname = (f1 or f2).lower().strip()
            value = v1 or v2
            if not value:
                continue

            if fname == "author" or fname == "authors":
                # 解析作者: "and" 分隔
                authors = [a.strip() for a in re.split(r"\s+and\s+", value) if a.strip()]
                ref["authors"] = authors
            elif fname == "title":
                ref["title"] = value
            elif fname == "journal":
                ref["journal"] = value
            elif fname == "year":
                m = re.search(r"\b(\d{4})\b", value)
                if m:
                    ref["year"] = m.group(1)
            elif fname == "volume":
                ref["volume"] = value
            elif fname == "number":
                ref["number"] = value
            elif fname == "pages":
                ref["pages"] = value
            elif fname == "doi":
                ref["doi"] = value
            elif fname == "abstract":
                ref["abstract"] = value
            elif fname == "keywords":
                ref["keywords"] = [k.strip() for k in re.split(r"[,;]+", value) if k.strip()]
            elif fname == "url":
                ref["url"] = value
            elif fname == "isbn":
                ref["issn"] = value

        if ref.get("title"):
            refs.append(ref)

    return refs


# ─── 统一入口 ──────────────────────────────────────────────────────


def parse_file(file_path: str | Path) -> list[dict]:
    """根据文件扩展名自动选择解析器。"""
    path = Path(file_path)
    text = path.read_text(encoding="utf-8", errors="replace")

    ext = path.suffix.lower()
    if ext == ".ris":
        return parse_ris(text)
    elif ext == ".bib":
        return parse_bibtex(text)
    else:
        raise ValueError(f"不支持的文献格式: {ext}（仅支持 .ris 和 .bib）")
