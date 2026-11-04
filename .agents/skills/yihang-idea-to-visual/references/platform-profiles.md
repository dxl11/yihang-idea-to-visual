# Platform Profiles

Platform configuration is separated from skill core instructions.

**Config file:** [assets/platform-profiles/profiles.json](../assets/platform-profiles/profiles.json)

## Rules

1. Each project selects **exactly one** platform.
2. All pages (cover + body) share that platform's canvas size.
3. Do **not** auto-generate multi-size variants.
4. Record selection in `design/platform.json` with profile id, width, height, and verification note.
5. Size fields include `source` and `verified_at`. When network is available, prefer checking official docs. If unverifiable, keep the configured default and state that it is **not** claimed as a freshly verified official rule.

## Included profiles (initial)

- `xiaohongshu` — Xiaohongshu / 小红书
- `wechat_mp_cover` — WeChat Official Account cover-oriented
- `wechat_moments` — WeChat Moments
- `douyin_carousel` — Douyin image post
- `weibo` — Weibo
- `instagram_portrait` — Instagram portrait
- `linkedin` — LinkedIn
- `custom` — user-specified width/height

## Custom size

When `custom` is chosen, require positive integer width and height. Persist both in `design/platform.json`.

## Extending

Add a new object to `profiles.json` with: `id`, `label`, `width`, `height`, `aspect_ratio`, `notes`, `source`, `verified_at`. Keep SKILL.md unchanged.
