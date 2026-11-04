# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Primary: Cursor users evaluating and installing Agent Skills—they need to understand what this skill does and run one install command with confidence.

Secondary: Creators, researchers, and operators who want a repeatable personal-IP pipeline from raw idea to publishable carousel images. They care that thinking is protected and the output is upload-ready.

## Product Purpose

**Yihang Idea to Visual** (`yihang-idea-to-visual`) turns a raw idea into a branded social-media image carousel (cover + body PNGs + ZIP) through a single Agent Skill with staged confirmations.

Success for the public README surface: a first-time visitor knows what this is, why it differs from a generic “AI writing” tool, and can install it into Cursor in one command.

## Positioning

One Agent Skill owns the full pipeline end-to-end—Thought Reviewer → article polish → titles → cover → editorial pagination → review → ordered PNG/ZIP export—while protecting locked article text. It is not a multi-agent crew, MCP server, or web app. Thought Reviewer is an internal module, not a separate skill.

## Operating Context

- Distributed via Vercel Skills CLI (`npx skills`) from GitHub `dxl11/yihang-idea-to-visual`
- Runs inside Cursor as skill `yihang-idea-to-visual`
- Private project state under `.idea-to-visual/projects/` (gitignored)
- Optional local Python helpers (Pillow) for typography and export

## Capabilities and Constraints

- Seven gated stages; Thought Reviewer skippable
- Exact article integrity after lock
- One platform / one canvas size per project
- Thought library + visual reference library
- No bundled cloud image API; image generation depends on host tools
- Install docs and skill id must remain accurate; do not invent pricing, customers, or unverified benchmarks
- Public README deliverable for this request: redesigned `README.md` / `README.en.md` with a custom banner; visual world fully open except product facts and install commands

## Brand Commitments

- Product name: Idea to Visual / Yihang Idea to Visual
- Skill id: `yihang-idea-to-visual`
- Visual identity for the README surface: **fully open** (user approved unrestricted art direction for this redesign)
- License: MIT for code/docs; asset policy in `ASSET-LICENSES.md`

## Evidence on Hand

- Working skill at `.agents/skills/yihang-idea-to-visual/`
- Bilingual README pair, CHANGELOG, tests, Thought Reviewer module (v1.2.0)
- Demo visual reference assets and thought-library method cards
- No customer testimonials or usage metrics—do not fabricate

## Product Principles

1. Clarity before decoration: visitors must grasp the mechanism in one viewport of reading.
2. Install is the primary action; secondary audiences get the promise without burying the command.
3. Protect author intent as a product claim, not a slogan.
4. Single-skill honesty: never market as an agent team or SaaS app.
5. Facts stay verifiable; style may be bold.

## Accessibility & Inclusion

README must remain readable as GitHub Markdown (semantic headings, alt text on banner, sufficient contrast in banner artwork). No motion-only information.
