#!/usr/bin/env python3
"""
Add `image: "URL"` to YAML front-matter after the `permalink:` line, using the
first <img src="..."> found in the file.

Usage:
  # Dry-run: show which files would be changed
  python3 scripts/add_featured_image.py --dry-run

  # Apply changes
  python3 scripts/add_featured_image.py --apply

Notes:
- Operates on all .html files recursively except the _site directory and .git.
- Only edits files that:
  * start with YAML front matter (---),
  * do not already have an `image:` key in the front matter,
  * contain at least one <img src="..."> (or src='...') in the content.
- The inserted value preserves the original src string (including templated `{{site.baseurl}}`).
- Be sure to commit or back up before running with --apply.
"""
import argparse
import re
from pathlib import Path

HTML_GLOB = '**/*.html'
EXCLUDE_DIRS = ['_site', '.git']

IMG_SRC_RE = re.compile(r'<img[^>]+src=(?P<quote>[\'\"])(?P<src>.+?)(?P=quote)', re.I | re.S)
FRONT_MATTER_RE = re.compile(r'^---\n(.*?)\n---\n', re.S)
IMAGE_KEY_RE = re.compile(r'(^|\n)image\s*:', re.I)
PERMALINK_RE = re.compile(r'(^|\n)permalink\s*:\s*(.+)', re.I)

def iter_files(root: Path):
    for p in root.glob(HTML_GLOB):
        # skip files in excluded directories
        if any(part in EXCLUDE_DIRS for part in p.parts):
            continue
        yield p

def process_file(path: Path):
    text = path.read_text(encoding='utf-8')
    fm = FRONT_MATTER_RE.search(text)
    if not fm:
        return None  # no YAML front matter
    fm_block = fm.group(1)
    if IMAGE_KEY_RE.search(fm_block):
        return None  # already has image key
    # find first image src in the rest of the file (after front matter)
    content = text[fm.end():]
    img_m = IMG_SRC_RE.search(content)
    if not img_m:
        return None  # no image found
    src = img_m.group('src').strip()
    # Build the image line
    image_line = f'image: "{src}"'
    # Determine where to insert: after permalink: if present, else before closing ---
    fm_text = fm.group(0)
    pm = PERMALINK_RE.search(fm_text)
    if pm:
        # Insert after the line that contains permalink
        insert_at = fm.start() + fm_text.find(pm.group(0)) + len(pm.group(0))
        new_text = text[:insert_at] + '\n' + image_line + text[insert_at:]
    else:
        # Insert before the final '---' closing the front matter
        closing_idx = fm.end() - len('---\n')
        new_text = text[:closing_idx] + image_line + '\n' + text[closing_idx:]
    # Return the change info and updated content
    return {
        'path': path,
        'image_src': src,
        'new_text': new_text,
    }

def main():
    parser = argparse.ArgumentParser(description='Add image front matter from first <img> in HTML files')
    parser.add_argument('--apply', action='store_true', help='Apply changes in-place')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be changed')
    parser.add_argument('--root', default='.', help='Repo root (defaults to current dir)')
    args = parser.parse_args()

    root = Path(args.root)
    changes = []
    for p in iter_files(root):
        res = process_file(p)
        if res:
            changes.append(res)

    if not changes:
        print('No files to update.')
        return

    print(f'Found {len(changes)} files to update:')
    for c in changes:
        print(f'  {c["path"]}  ->  image: "{c["image_src"]}"')

    if args.dry_run or not args.apply:
        print('\nDry run (no files changed). To apply changes run with --apply.')
        return

    # Apply changes
    for c in changes:
        p = c['path']
        p.write_text(c['new_text'], encoding='utf-8')
        print('Updated', p)
    print('\nDone. Please run `git add` and `git commit` to record the changes.')

if __name__ == '__main__':
    main()
