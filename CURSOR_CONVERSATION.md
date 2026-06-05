# Cursor Conversation Context — Wayne Barrass-Brown Art Gallery

**Purpose:** Load this file at the start of a new Cursor chat to restore project context from prior sessions.

**Repository:** `d:\git\wayne_barrass-brown_art_gallery`  
**Live site:** https://waynebb7.github.io/wayne_barrass-brown_art_gallery/  
**Transcript reference:** [f8a3e0ac-24c0-4150-bea5-2e55f6a851f3](f8a3e0ac-24c0-4150-bea5-2e55f6a851f3)  
**Full transcript file:** `CURSOR_CONVERSATION_TRANSCRIPT.md` (ChatGPT export format, 102 merged messages)

---

## Project summary

Static single-page art portfolio for **Wayne Barrass-Brown**. Almost everything lives in `index.html` (~3000 lines) with CSS and JavaScript inline. Images are in `images/` (full resolution) and `images/display/` (optimized, max 800px wide via `optimize_images.py`).

**Architecture:** GitHub Pages static site — no backend. Browser-only storage (localStorage, IndexedDB) for admin edits until exported and committed to git.

---

## Chronology of user requests and outcomes

### Phase 1 — Gallery improvements (numbered list from early session)

| # | Request | Done |
|---|---------|------|
| 1 | Fix broken HTML in header | Fixed mismatched `<h3>` tags |
| 2 | Enable mobile viewing | Uncommented viewport meta tag |
| 3 | Add meaningful alt text | Generated from filenames for all images |
| 4 | Remove duplicate entries | Deduped gallery list items |
| 5 | Load Poppins font | Added Google Fonts links |
| 6 | Click to view full size | Wrapped images in `<a href="images/...">` |
| 7 | Single layout, vertical scroll | Removed `page2.html`; `index.html` only, vertical column |
| 8 | Lazy-load images | Added `loading="lazy"` |
| 9 | Optimize image files | Added `optimize_images.py`, `images/display/` |
| 10 | Use srcset / thumbnails | Display images served from `images/display/` |
| 11 | Stop duplicating image list | Single `index.html` (page2 deleted) |
| 12 | Clean up repo | `.gitignore`, removed `.DS_Store`, PSDs, unused images |
| 13 | Basic metadata | Title, description, Open Graph |
| 14 | Light categorization | Category filters + sub-filters (digital tools, sketch mediums) |
| 15 | Deploy GitHub Pages | `.github/workflows/pages.yml`, `.nojekyll`, README deploy section |
| 16 | Improve README | Full documentation |

**Bug reports handled:**
- `Rocks.jpg` / `page2.html` inconsistency → **Not applicable**; `page2.html` was intentionally deleted in step 7.
- Missing link to `page2.html` → **Intentional**; alternate layout removed.

### Phase 2 — Add artwork & admin features

- **Add artwork panel** — pick images, set alt/categories, save to IndexedDB, show in gallery with dashed outline.
- **Export added artwork** — downloads image files + `gallery-additions.txt` with HTML snippets.
- **Right-click category menu** — edit categories/tools on any image.
- **Hidden artwork** — hide from gallery (browser storage); restore or delete permanently.
- **Manage categories** — add/rename/delete custom categories.
- **Wide aspect tiles** — `gallery-item--wide` via `column-span: all` for panoramic images.

### Phase 3 — Private access (viewer vs admin)

- **Passcode gate** blocks page until sign-in.
- **Viewer mode** — browse/filter/open images only; no admin UI; no browser-only edits/uploads.
- **Admin mode** — full editing (add, hide, categories, export).
- **`admin.html`** — shortcut that sets admin sign-in intent.
- Default passcodes in `ACCESS_CONFIG` (change before sharing):
  - Viewer: `gallery-view`
  - Admin: `wayne-admin`
- Passcodes verified via SHA-256 at runtime (`hashPasscode`, `verifyPasscode`).
- **Security:** Client-side only — casual privacy, not strong auth. Store real passcodes in a password manager, not in README/repo.

### Phase 4 — Tile drag-and-drop (later removed)

- Implemented admin drag-to-reorder with `gallery-order.json` publish path.
- Multiple attempts to fix cross-column masonry drag (CSS columns, grid, explicit column containers).
- **User request:** Remove tile dragging completely → reverted to commit `0b75cc2` state (before drag was added).
- **Current status:** No drag handles, no `gallery-order.json`, no layout export button.

### Phase 5 — Permanent deletion from Hidden artwork

- **Double confirmation** before permanent delete.
- **Uploaded artwork** — deleted from IndexedDB immediately.
- **Built-in gallery images** — browser cannot delete server files directly; downloads:
  - `index.html` (with `<li>` removed, when fetch works)
  - `delete-artwork.ps1`
  - `gallery-deletion.json`
  - `gallery-deletion-steps.txt`
- **`delete_artwork.py`** — applies JSON deletion to `index.html` and deletes image files locally.
- **`PERMANENT_DELETIONS_STORAGE_KEY`** — `gallery-permanent-deletions` in localStorage prevents deleted items reappearing until `index.html` is updated in repo.

### Phase 6 — Add artwork troubleshooting

- User reported add artwork not working; asked if static site was the cause.
- **Answer:** Works in admin mode via IndexedDB, but only in that browser until exported. Not written to server automatically.
- **Fixes added:** Status messages, IndexedDB probe, filter reset to "All" after add, clearer hints, admin-only guards.

---

## Current feature state (as of last session)

### Working / in place

- GitHub Pages deployment on push to `main`
- Passcode gate (viewer + admin)
- Category and sub-category filters
- CSS column masonry layout (`column-count: 3`, responsive 2/1)
- Add artwork (admin, IndexedDB)
- Export added artwork
- Hidden artwork (hide / restore / permanent delete with export workflow)
- Manage categories
- Right-click category menu (admin)
- `optimize_images.py` and `delete_artwork.py`
- README with deploy, access, add/delete workflows

### Removed / not present

- Tile drag-and-drop reordering
- `gallery-order.json` layout publishing
- `page2.html` alternate grid layout
- Export gallery layout button

### Uncommitted local changes (may differ from `main`)

Recent work (drag removal, deletion workflow, add-artwork fixes) may be staged or uncommitted. Check `git status` and diff against `main` before assuming production matches local.

---

## Key files

| Path | Purpose |
|------|---------|
| `index.html` | Entire gallery app (HTML, CSS, JS, passcodes as hashes) |
| `admin.html` | Admin sign-in shortcut |
| `README.md` | User-facing documentation |
| `optimize_images.py` | Regenerate `images/display/` from `index.html` |
| `delete_artwork.py` | Remove entries from `index.html` + delete image files |
| `.github/workflows/pages.yml` | GitHub Pages deploy |
| `.nojekyll` | Disable Jekyll on GitHub Pages |
| `images/` | Full-resolution originals |
| `images/display/` | Web-optimized display images |

---

## JavaScript constants & storage keys

```text
ACCESS_CONFIG              — passcode labels + SHA-256 hashes
ACCESS_STORAGE_KEY         — remembered access role
ACCESS_INTENT_KEY          — admin.html redirect intent
STORAGE_KEY                  — gallery-category-overrides (localStorage)
TOOLS_STORAGE_KEY          — gallery-tool-overrides
CATEGORIES_STORAGE_KEY       — gallery-categories
HIDDEN_STORAGE_KEY           — gallery-hidden-items
PERMANENT_DELETIONS_STORAGE_KEY — gallery-permanent-deletions
UPLOAD_DB_NAME               — art-gallery-uploads (IndexedDB)
UPLOAD_STORE_NAME            — uploads
WIDE_ASPECT_RATIO            — 1.55 (wide tile threshold)
```

**Default categories:** digital, manga, pumpkins, sketches, figures, painting, photos, other

**Sub-filters:** digital (iPad, Procreate, Solidworks, Photoshop, Illustrator); sketches (pen, pencil, coloured pencil, charcoal)

---

## Admin workflows

### Add new artwork (browser → published)

1. Sign in as **admin**
2. Add artwork → choose files → Add to gallery
3. Export added artwork
4. Copy images to `images/`
5. Paste HTML into `<ul id="gallery">` in `index.html`
6. `python optimize_images.py`
7. Commit and push

### Hide artwork

- Right-click → Hide from gallery
- View in **Hidden artwork** panel
- **Show in gallery** to restore

### Permanently delete hidden artwork

1. Hidden artwork → Delete permanently (two confirmations)
2. For built-in images: apply downloaded `index.html`, run `delete-artwork.ps1` or `python delete_artwork.py gallery-deletion.json`
3. Commit and push

### Change passcodes

Edit `ACCESS_CONFIG` in `index.html` — use SHA-256 hashes, not plain text in production.

---

## Git commit history (relevant)

```text
bedfa74 — Add drag-and-drop (later reverted locally)
0b75cc2 — Implement access gate (viewer/admin)  ← state before drag
3581232 — Add GitHub Pages deployment workflow
73cd56c — Enhanced index.html (filters, styling, hidden artwork UI)
```

---

## Known limitations

1. **Static site** — browser cannot write to `images/` or `index.html` on the server; export + git push required.
2. **Passcodes** — visible to anyone who inspects `index.html`; hashes are not secret.
3. **Admin edits** — category overrides, hidden items, uploads persist per-browser unless exported/published.
4. **Viewer mode** — does not see browser-added uploads or hidden-item state.
5. **Add artwork** — needs IndexedDB + HTTPS (GitHub Pages or local server); `file://` may fail.
6. **Tile reordering** — removed by user request; do not re-implement without explicit ask.

---

## User preferences observed

- Wants **minimal scope** changes; dislikes over-engineering.
- **Removed** tile drag-and-drop after multiple failed UX attempts — do not restore unless asked.
- Wants **double confirmation** for destructive deletes.
- Wants **real file deletion** from project folder (via scripts, not browser-only hide).
- Uses **Windows / PowerShell**.
- **Do not commit** unless explicitly asked.
- Store passcodes in **password manager**, not in repo/README.

---

## Suggested prompt for next session

Copy into a new Cursor chat:

```text
Read CURSOR_CONVERSATION.md and README.md for context on this art gallery project.
Continue from the current state described there.
```

Or attach `@CURSOR_CONVERSATION.md` when starting a chat.

---

## Open questions / possible follow-ups

- [ ] Commit and push recent changes (drag removal, deletion workflow, add-artwork fixes) if not yet on `main`
- [ ] Change default passcodes in `ACCESS_CONFIG` before wider sharing
- [ ] User may want stronger auth later (Cloudflare Access, etc.) — not implemented
- [ ] Tile reordering was explicitly abandoned — alternative: manual HTML order or future different UX

---

*Generated from Cursor agent session. Last updated: June 2026.*
