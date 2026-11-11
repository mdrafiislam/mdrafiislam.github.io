"""Refresh data/citations.json from the public Google Scholar profile page.

Runs once a day from .github/workflows/update-citations.yml.
Scholar's robots.txt allows profile pages (/citations?user=). The script makes
one request, identifies itself honestly, and never retries or works around a
block: if Scholar refuses or the page layout changes, the previous numbers are
kept and the website keeps showing them with their original date.
"""
import datetime
import json
import pathlib
import re
import sys
import urllib.request

SCHOLAR_ID = "sG1AczMAAAAJ"
URL = f"https://scholar.google.com/citations?user={SCHOLAR_ID}&hl=en"
OUT = pathlib.Path(__file__).resolve().parent.parent / "data" / "citations.json"
USER_AGENT = "mdrafiislam.github.io citation updater (+https://mdrafiislam.github.io; once daily)"


def parse(html: str) -> dict:
    """Return the 'All' column of Scholar's citation table."""
    cells = re.findall(r'class="gsc_rsb_std">\s*([\d,]+)\s*<', html)
    if len(cells) < 6:
        raise ValueError(f"expected 6 table cells, found {len(cells)}")
    nums = [int(c.replace(",", "")) for c in cells[:6]]
    # Row order: citations, h-index, i10-index; columns: All, Since <year>.
    return {"citations": nums[0], "h_index": nums[2], "i10_index": nums[4]}


def main() -> int:
    old = json.loads(OUT.read_text()) if OUT.exists() else {}
    try:
        req = urllib.request.Request(URL, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=30) as resp:
            html = resp.read().decode("utf-8", "replace")
        new = parse(html)
    except Exception as exc:  # blocked, offline, or layout changed
        print(f"::warning::Scholar not updated, keeping previous values ({exc})")
        return 0

    # Sanity check: citation counts should not collapse overnight.
    if old.get("citations") and new["citations"] < 0.8 * old["citations"]:
        print(f"::warning::Implausible drop {old['citations']} -> {new['citations']}; keeping previous values")
        return 0

    today = datetime.date.today().isoformat()
    changed = any(new[k] != old.get(k) for k in new)
    data = {
        "scholar_id": SCHOLAR_ID,
        **new,
        "updated": today if changed else old.get("updated", today),
        "checked": today,
    }
    OUT.write_text(json.dumps(data, indent=2) + "\n")
    print(f"Scholar: {new} ({'changed' if changed else 'unchanged'})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
