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

This project can be published with [GitHub Pages](https://pages.github.com/) by enabling Pages for the `main` branch in the repository settings. Once enabled, the site will be available at:

`https://waynebb7.github.io/wayne_barrass-brown_art_gallery/`

## Adding new artwork

### In the browser

1. Open the gallery and click **Add artwork**.
2. Choose one or more image files.
3. Set alt text and categories for each preview.
4. Click **Add to gallery**.

New pieces appear at the top of the gallery with a dashed outline. They are stored in this browser until you export them.

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

## Project structure

| Path | Purpose |
| --- | --- |
| `index.html` | Gallery page |
| `images/` | Full-resolution originals (used when an image is clicked) |
| `images/display/` | Optimized display images (max 800px wide) |
| `optimize_images.py` | Regenerates files in `images/display/` from `index.html` |
| `LICENSE` | MIT License |
