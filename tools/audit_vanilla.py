"""Read installed EU5 text sources and write a reproducible inventory, not a benchmark.

Standard library only. This is a brace-aware inventory scanner, NOT a general
Clausewitz parser, include resolver, save parser, validator or setup generator.
It never edits game files and does not model DLC/VFS override precedence.
"""

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import struct


TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|#[^\r\n]*|[{}=]|[^\s{}=#"]+')
MOD_ROOT = Path(__file__).resolve().parents[1]


def scan(path):
    """Return literal block paths and scalar assignments; ignore commented text."""
    blocks, assignments, stack = [], [], []
    previous = previous2 = ""
    for match in TOKEN.finditer(path.read_text(encoding="utf-8-sig")):
        value = match.group()
        if value.startswith("#"):
            continue
        if value == "{":
            key = previous2 if previous == "=" else "<anonymous>"
            stack.append(key)
            blocks.append(tuple(stack))
        elif value == "}":
            if not stack:
                raise ValueError(f"Unbalanced closing brace: {path}")
            stack.pop()
        elif previous == "=":
            assignments.append((tuple(stack), previous2, value.strip('"')))
        previous2, previous = previous, value
    if stack:
        raise ValueError(f"Unclosed block: {path}")
    return blocks, assignments


def file_record(path, root):
    data = path.read_bytes()
    return {
        "path": path.relative_to(root).as_posix(),
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def inventory(root):
    setup = root / "main_menu/setup/1337"
    records = []
    parsed = {}
    for path in sorted(setup.glob("*.txt")):
        record = file_record(path, root)
        blocks, assignments = scan(path)
        record["root_blocks"] = [p[0] for p in blocks if len(p) == 1]
        record["root_scalar_keys"] = sorted({k for p, k, v in assignments if not p})
        records.append(record)
        parsed[path.name] = (blocks, assignments)

    country_blocks, country_assignments = parsed["10_countries.txt"]
    country_tags = [p[-1] for p in country_blocks
                    if len(p) == 3 and p[:2] == ("countries", "countries")]
    explicit_types = Counter(v for p, k, v in country_assignments
                             if len(p) == 3 and p[:2] == ("countries", "countries")
                             and k == "type")
    pop_blocks, _ = parsed["06_pops.txt"]
    _, market_assignments = parsed["03_markets.txt"]
    markets = [v for p, k, v in market_assignments
               if p == ("market_manager",) and k == "add_market"]
    character_blocks, _ = parsed["05_characters.txt"]
    dynasty_blocks, _ = parsed["04_dynasties.txt"]
    io_blocks, _ = parsed["15_international_organizations.txt"]
    war_blocks, _ = parsed["16_wars.txt"]

    templates_path = root / "in_game/map_data/location_templates.txt"
    templates, template_assignments = scan(templates_path)
    location_ids = {p[0] for p in templates if len(p) == 1}
    geography_path = root / "in_game/map_data/definitions.txt"
    geography, _ = scan(geography_path)
    regions = {p[-1]: [a[-1] for a in geography
                       if len(a) == 4 and a[:3] == p]
               for p in geography if len(p) == 3 and p[0] == "europe"}

    definitions = {}
    definition_paths = sorted((root / "in_game/setup/countries").glob("*.txt"))
    for path in definition_paths:
        blocks, _ = scan(path)
        for p in blocks:
            if len(p) == 1:
                definitions[p[0]] = path.relative_to(root).as_posix()
    formable_path = root / "in_game/common/formable_countries/00_formable_countries.txt"
    _, formables = scan(formable_path)
    formable_tags = {v for p, k, v in formables if len(p) == 1 and k == "tag"}

    scenario = json.loads((MOD_ROOT / "config/scenario.json").read_text(encoding="utf-8"))
    roster_checks = []
    for country in scenario["countries"]:
        tag = country["tag"]
        roster_checks.append({
            "tag": tag,
            "country_definition": definitions.get(tag),
            "has_formable_tag": tag in formable_tags,
            "capital_id_exists": country["capital"] in location_ids,
        })

    png = root / "in_game/map_data/locations.png"
    with png.open("rb") as stream:
        if stream.read(8) != b"\x89PNG\r\n\x1a\n":
            raise ValueError("locations.png is not a PNG")
        stream.seek(16)
        width, height = struct.unpack(">II", stream.read(8))

    dlc_setup_paths = sorted((root / "dlc").glob("*/main_menu/setup/**/*.txt"))
    dlc_setup_paths += sorted((root / "dlc").glob("*/in_game/setup/**/*.txt"))
    extra_sources = [templates_path, geography_path, formable_path,
                     root / "main_menu/common/bookmarks/00_bookmarks.txt",
                     root / "in_game/map_data/default.map"] + definition_paths
    branch = root / "loading_screen/caesar_branch.txt"
    revision = root / "loading_screen/caesar_rev.txt"
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "game_root": str(root),
        "kind": "static_source_inventory_not_runtime_benchmark",
        "source_scope": "installed_base_files_without_include_expansion_or_vfs_resolution",
        "caesar_branch": branch.read_text(encoding="utf-8").strip() if branch.exists() else None,
        "caesar_revision": revision.read_text(encoding="utf-8").strip() if revision.exists() else None,
        "setup_files": records,
        "setup_total_bytes": sum(r["bytes"] for r in records),
        "counts": {
            "country_blocks": len(country_tags),
            "distinct_country_tags": len(set(country_tags)),
            "explicit_country_type_fields": dict(sorted(explicit_types.items())),
            "country_blocks_without_explicit_type_field": len(country_tags) - sum(explicit_types.values()),
            "market_declarations": len(markets),
            "pop_location_blocks_including_empty": sum(len(p) == 2 and p[0] == "locations" for p in pop_blocks),
            "define_pop_blocks": sum(p[-1] == "define_pop" for p in pop_blocks),
            "character_db_blocks": sum(len(p) == 2 and p[0] == "character_db" for p in character_blocks),
            "dynasty_blocks": sum(len(p) == 2 and p[0] == "dynasty_manager" for p in dynasty_blocks),
            "international_organization_manager_child_blocks": sum(len(p) == 2 for p in io_blocks),
            "war_manager_child_blocks": sum(len(p) == 2 for p in war_blocks),
            "location_template_blocks": len(location_ids),
            "country_definition_tags": len(definitions),
        },
        "europe_regions_and_areas": regions,
        "location_template_topographies": dict(sorted(Counter(
            v for p, k, v in template_assignments if len(p) == 1 and k == "topography").items())),
        "map_png": {"width": width, "height": height, "bytes": png.stat().st_size},
        "country_roster_source_checks": roster_checks,
        "market_ids_exist": {m: m in location_ids for m in scenario["start_markets"]},
        "additional_source_files": [file_record(p, root) for p in extra_sources],
        "dlc_setup_candidates": [file_record(p, root) for p in dlc_setup_paths],
        "limitations": [
            "Source declarations are not counts of alive AI countries or runtime objects.",
            "Includes, templates, DLC activation and VFS precedence are not resolved.",
            "No startup time, simulation time, memory or in-game compatibility was measured.",
            "Formable tags do not supply complete start-country definitions.",
            "No game installation file was modified."
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--game-root", required=True, type=Path, help="EU5 game directory")
    parser.add_argument("--output", type=Path, default=MOD_ROOT / "docs/source_inventory.json")
    args = parser.parse_args()
    root = args.game_root.resolve(strict=True)
    output = args.output.resolve()
    if not output.is_relative_to(MOD_ROOT) or output.is_relative_to(root):
        parser.error("Audit output must stay inside this mod and outside the game installation.")
    if not (root / "main_menu/setup/1337/10_countries.txt").is_file():
        parser.error("Expected main_menu/setup/1337/10_countries.txt; re-audit layout after updates.")
    result = inventory(root)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "counts": result["counts"],
                      "roster_checked": len(result["country_roster_source_checks"])}, ensure_ascii=False))


if __name__ == "__main__":
    main()
