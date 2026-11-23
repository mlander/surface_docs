# Surface API and Drupal core

The source of a site that makes the case for describing each piece of Drupal data once, and lays out a path for the Surface API proof of concept's ideas into Drupal core.

- The site: https://mlander.github.io/surface_docs/
- The proof of concept: https://www.drupal.org/project/surface
- How to contribute, the writing rules and the page templates: [CONTRIBUTING.md](CONTRIBUTING.md)

## Layout

- `docs/`: the pages.
- `topics.yml`: every talking point with its maturity and destination. The status strip on each page and the board are built from it.
- `hooks.py`: the build step that reads `topics.yml`.
- `module/`: the proof of concept as a git submodule, pinned to one commit. Code on the site is pulled from here.

## Building

```bash
pip install -r requirements.txt
git submodule update --init
mkdocs serve
```

A push to `main` publishes through GitHub Actions.
