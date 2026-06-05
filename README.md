# Wayne Barrass-Brown Art Gallery

A personal portfolio site for drawings, paintings, digital art, pumpkin carvings, and other work. The site is a single static page (`index.html`) with category filters, lazy-loaded images, and click-through to full-resolution files.

Repository: [github.com/waynebb7/wayne_barrass-brown_art_gallery](https://github.com/waynebb7/wayne_barrass-brown_art_gallery)

## View locally

Open `index.html` in your browser, or run a simple local server from the project folder:

```powershell
python -m http.server 8000
```

Then visit [http://localhost:8000](http://localhost:8000).

## Live site

**https://waynebb7.github.io/wayne_barrass-brown_art_gallery/**

The gallery is private by default. Visitors need a passcode to open it.

## Access modes

| Mode | URL | What you can do |
| --- | --- | --- |
| Viewer (read only) | `index.html` | Browse, filter, and open full-size images |
| Admin | `admin.html` | Add artwork, hide images, manage categories, export changes |

### Default passcodes

Change these in `index.html` before sharing the site. Search for `ACCESS_CONFIG`:

| Mode | Default passcode |
| --- | --- |
| Viewer | `gallery-view` |
| Admin | `wayne-admin` |

Share the **viewer** passcode with people you want to see the gallery. Keep the **admin** passcode private.

### How it works

- **Viewer mode** shows the published gallery only. It does not load browser-only edits, uploads, or hidden images.
- **Admin mode** unlocks all editing tools (add artwork, right-click categories, hidden artwork, manage categories, export).
- Use **Remember on this device** to stay signed in on that browser.
- **Sign out** clears access and returns to the passcode screen.

### Security note

GitHub Pages serves static files only. The passcode check runs in the browser, so this is best treated as casual privacy rather than strong security. Someone technical could still inspect the page source. For stronger protection you would need server-side authentication or a service such as Cloudflare Access.

## Deploy with GitHub Pages

This repo includes a GitHub Actions workflow (`.github/workflows/pages.yml`) that publishes the site on every push to `main`.

### One-time setup

1. Open the repository on GitHub: [github.com/waynebb7/wayne_barrass-brown_art_gallery](https://github.com/waynebb7/wayne_barrass-brown_art_gallery)
2. Go to **Settings** → **Pages**
3. Under **Build and deployment**, set **Source** to **GitHub Actions**
4. Push the workflow to `main` (if it is not there yet)

### Publish updates

After setup, each push to `main` deploys automatically. You can also run the workflow manually from the **Actions** tab → **Deploy to GitHub Pages** → **Run workflow**.

To deploy from your machine:

```powershell
git add .
git commit -m "Your message"
git push origin main
```

The live URL will be:

`https://waynebb7.github.io/wayne_barrass-brown_art_gallery/`

It can take 1–2 minutes after a push for changes to appear.

## Adding new artwork

### In the browser

1. Sign in with the **admin** passcode (viewer mode is read-only).
2. Open the gallery and click **Add artwork**.
3. Choose one or more image files.
4. Set alt text and categories for each preview.
5. Click **Add to gallery**.

New pieces appear at the top of the gallery with a dashed outline. Because GitHub Pages is a static site, they are stored in **this browser only** until you export them. Other visitors will not see them until you publish the exported files.

5. Click **Export added artwork** to download:
   - each image file
   - a `gallery-additions.txt` file with HTML snippets and publish steps

6. Copy the downloaded images into `images/`, paste the HTML into `index.html`, then run:

```powershell
pip install Pillow
python optimize_images.py
```

### Manually

1. Copy the image file into `images/`.
2. Add a gallery entry to `index.html` inside `<ul id="gallery">`:

```html
<li data-categories="sketches">
  <a href="images/my-new-piece.jpg">
    <img src="images/display/my-new-piece.jpg" alt="My new piece" loading="lazy">
  </a>
</li>
```

3. Run `python optimize_images.py`.

Set `data-categories` to one or more of: `digital`, `manga`, `pumpkins`, `sketches`, `figures`, `painting`, `photos`, `other`.

You can also right-click any image and change its categories. Those edits are saved in localStorage for that browser only.

## Permanently deleting hidden artwork (admin)

In **Hidden artwork**, **Delete permanently** asks for confirmation twice.

- **Added artwork** (browser uploads) is erased from this browser immediately.
- **Built-in gallery images** are removed from the gallery and the browser records a permanent deletion. Your browser downloads:
  - `index.html` with the gallery entry removed (when the page can fetch the current file)
  - `delete-artwork.ps1` to delete the original and display image files
  - `gallery-deletion.json` for the Python alternative below
  - `gallery-deletion-steps.txt` with instructions

Apply the deletion to the project folder:

```powershell
# Option A: PowerShell
.\delete-artwork.ps1

# Option B: Python
python delete_artwork.py gallery-deletion.json
```

Then commit and push so GitHub Pages stops serving the removed images.

## Project structure

| Path | Purpose |
| --- | --- |
| `index.html` | Gallery page with passcode gate |
| `admin.html` | Shortcut to admin sign in |
| `images/` | Full-resolution originals (used when an image is clicked) |
| `images/display/` | Optimized display images (max 800px wide) |
| `optimize_images.py` | Regenerates files in `images/display/` from `index.html` |
| `delete_artwork.py` | Removes gallery entries from `index.html` and deletes image files |
| `LICENSE` | MIT License |
