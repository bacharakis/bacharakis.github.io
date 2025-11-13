## Quick context

This repository is a personal GitHub Pages site built with Jekyll using the `jekyll-theme-chirpy` theme. The source content is in the repository and the site is built into `_site/` for publishing.

Key files and directories
- `_config.yml` — site configuration and permalink defaults (posts use `/posts/:title/`).
- `tools/run.sh` — development server wrapper. Use `./tools/run.sh` to start a local server (accepts `-H` to set host, `-p` for production mode).
- `tools/test.sh` — build + htmlproofer checks. Run `./tools/test.sh` to run a production build and link checks.
- `_posts/` and `_drafts/` — blog content in Jekyll post format. Posts in this repo are HTML-exported WordPress posts with YAML front matter.
- `assets/` — images and static assets used by posts and pages.
- `.github/workflows/pages-deploy.yml` — CI build + htmlproofer and the GitHub Pages deploy flow.

## What I (an AI agent) should know before editing or adding content

- This is a static Jekyll site. Changes to content (files in `_posts`, `_pages`, `_tabs`, etc.) often only require a local `./tools/run.sh` to preview.
- Production builds use `JEKYLL_ENV=production` and are tested with `htmlproofer` (see `tools/test.sh` and the CI workflow). Keep internal links and `site.baseurl` usage correct.
- Posts here include front-matter fields like `layout`, `title`, `date`, `permalink`, `categories`, `tags`, and `image.path`. Match existing examples in `_posts/` when creating new posts.
- The project's `_config.yml` sets global defaults (notably `permalink: /posts/:title/` for posts). Do not change permalink format unless you update links site-wide.

## Editing rules & patterns to follow

- When adding posts: copy the front matter pattern from existing files in `_posts/`. Example: `permalink: "/2020/04/08/zero-inbox/"` or omit and rely on default `/posts/:title/`.
- Use `{{ site.baseurl }}` for asset paths inside posts (existing posts use `/assets/img/...`).
- Keep posts' HTML content structure consistent with existing exported WordPress HTML (you can edit the HTML), but prefer lightweight Markdown where possible — ensure front matter `layout: post` remains.
- If you change CSS, templates, or theme-related files, be aware the theme is provided by the `jekyll-theme-chirpy` gem. Theme files are not all in this repo; the README documents which theme files may be copied in.

## Build, test and deploy (developer workflows)

- Local dev server (live reload):
  - ./tools/run.sh
  - Options: `-H <host>` to bind (default 127.0.0.1), `-p` to run in production mode.
- Production build and content checks:
  - ./tools/test.sh
  - This runs `JEKYLL_ENV=production bundle exec jekyll b` then `htmlproofer _site` (internal links only).
- CI: `.github/workflows/pages-deploy.yml` runs `bundle exec jekyll b` and `htmlproofer` before deploying to GitHub Pages.

## Integration and dependencies

- Ruby & Bundler: The project uses a Ruby toolchain (see `Gemfile`) — the GH Actions workflow sets Ruby 3.3. When running locally, use `bundle install` then `bundle exec` where appropriate.
- htmlproofer is used for link validation in `tools/test.sh` and CI — tests will fail if broken internal links or problems are found.

## Examples and quick patterns

- Start the dev server bound to all hosts (useful for container/dev environment):
  - `./tools/run.sh -H 0.0.0.0`
- Run the full production build & checks locally before pushing:
  - `./tools/test.sh`
- Asset reference inside a post (example found in `_posts/2020-04-08-zero-inbox.html`):
  - `<img src="/assets/img/2020/04/zero-inbox1.png">`

## Safety & constraints for automated changes

- Do NOT change `permalink` defaults in `_config.yml` without updating existing links and redirects — the site assumes `/posts/:title/` for many links.
- Avoid modifying theme internals unless adding files under `_includes`, `_layouts`, or `_sass` that intentionally override theme defaults.
- When adding or moving images, place them under `assets/img/<year>/<month>/` to match existing organization.

## If you need more context

- Inspect these files to learn patterns: `_config.yml`, `_posts/` (example: `2020-04-08-zero-inbox.html`), `tools/run.sh`, `tools/test.sh`, `.github/workflows/pages-deploy.yml`.

If anything above is unclear or you'd like me to expand on specific parts (linking policy, front-matter fields, or theme overrides), tell me which section to iterate on.
