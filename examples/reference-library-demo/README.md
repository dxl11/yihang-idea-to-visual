# Visual reference library (framework)

The built-in library lives at:

`.agents/skills/yihang-idea-to-visual/assets/visual-reference-library/`

It currently ships **empty** (category folders + empty `catalog.json` only). Add real images later, then rebuild the index:

```bash
python .agents/skills/yihang-idea-to-visual/scripts/build_reference_index.py --full
```

Empty catalogs are valid: cover/editorial stages skip retrieval and continue the normal design flow.
