#!/usr/bin/env python3
import json
import re
from pathlib import Path

from jsonschema import Draft202012Validator

root = Path(".agents/skills/yihang-idea-to-visual")
schemas = {
    "brand": root / "schemas/brand-profile.schema.json",
    "state": root / "schemas/project-state.schema.json",
    "design": root / "schemas/design-profile.schema.json",
    "manifest": root / "schemas/page-manifest.schema.json",
}
for name, path in schemas.items():
    Draft202012Validator.check_schema(json.loads(path.read_text(encoding="utf-8")))
    print("schema ok", name)

brand = json.loads((root / "assets/brand-kit/brand-profile.sample.json").read_text(encoding="utf-8"))
Draft202012Validator(json.loads(schemas["brand"].read_text(encoding="utf-8"))).validate(brand)
state = json.loads((root / "assets/templates/project-template/state.json").read_text(encoding="utf-8"))
Draft202012Validator(json.loads(schemas["state"].read_text(encoding="utf-8"))).validate(state)

text = (root / "SKILL.md").read_text(encoding="utf-8")
missing = []
for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", text):
    target = match.group(1).strip()
    if target.startswith("http") or target.startswith("#"):
        continue
    target = target.split("#", 1)[0]
    if not target:
        continue
    if not (root / target).exists():
        missing.append(target)
if missing:
    raise SystemExit(f"Missing SKILL.md references: {missing}")


def check(readme: Path):
    miss = []
    body = readme.read_text(encoding="utf-8")
    for match in re.finditer(r"\[[^\]]+\]\((?!https?://)([^)]+)\)", body):
        target = match.group(1).strip()
        if target.startswith("#") or target.startswith("mailto:"):
            continue
        target = target.split("#", 1)[0]
        if not target or " " in target:
            continue
        if not (readme.parent / target).exists():
            miss.append((str(readme), target))
    return miss


broken = check(Path("README.md")) + check(Path("README.en.md"))
if broken:
    raise SystemExit(f"Broken README links: {broken}")
print("schema + link checks OK")
