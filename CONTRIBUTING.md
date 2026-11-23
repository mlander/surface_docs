# Contributing to this site

This site makes the case for moving Surface API's ideas into Drupal core and shows what that looks like on real code. It says two things at once: a lot of thought has gone into this, and there is room to improve it. Pages state the proposal plainly, show the reasoning and the alternatives already weighed, and say what is still open.

The module itself lives on drupal.org at [project/surface](https://www.drupal.org/project/surface). Its own documentation is the reference. This site is the argument and the map, and it links into the reference instead of copying it.

## Three concepts, and no more

The site introduces three concepts. Everything else is described in plain words as something one of them can say or do.

- **Structure.** The description of a thing's data: each key, its type, its choices and its rules.
- **Resource and its operations.** The thing itself, where it is stored and who may change it, and the named actions on it ("update the site information", "place a block").
- **Portable Schema.** How a structure is written down and served: JSON Schema, with a small agreed set of extension keywords.

Do not give other parts their own names on this site. A key whose allowed values depend on another key is "a key that depends on another key", not a new term. A form, a Tool API tool and an HTTP call are "ways to run an operation". Use core's existing names for everything core already has: constraint plugins, third-party settings, config schema, Form API.

## Small and non-invasive

Every retrofit is shown as the smallest change that works. Say what a module adds, and say plainly what it does not have to touch: its stored config, its config schema, its existing form, its routes. Show counts of files and lines added, and of files removed (usually none).

## Writing

- Direct and concise. Active voice. Cut any sentence that gives no mechanism and no reason.
- No analogies. Explain the mechanism.
- Plain words. No term a reader outside the module would have to look up.
- American spelling. No em-dashes.
- Write "Tool API tool", not "AI tool".
- Call the module "the Surface API proof of concept" or "the proof of concept", not a contrib module. It is on drupal.org for its issue queue and repository while it is prototyped, and will have no full release.
- When talking about config schema's future, use "could" and "long term". Nothing here removes or deprecates it.
- Do not promise a share of code removed. Counts of places a value is described are fine, with a footnote saying how they were counted and against which core version.

## Code on the site

Code is pulled from the module at the pinned commit, never pasted:

```text
--8<-- "modules/surface_examples_block/src/Resource/BlockPlacementResource.php:20:60"
```

The path is relative to the `module/` submodule. A missing file fails the build. When the module is bumped to a new commit, rebuild and check that each line range still shows what its page says.

Show a class's surface code in full: attribute arguments and keys are never elided. Methods that are not about the description may be left out with a comment saying so.

## Maturity

Every talking point has a level in `topics.yml`: Settled, Working, Sketch or Question. A person sets it; a generated review alone never makes something Settled. `proposed` is a first reading from the evidence, for the person who sets the level. See `docs/about/maturity.md`.

Change a level in its own commit, with the reason in the message.

## Page templates

### A worked example (`docs/adopting/`)

1. **Today.** What the module has now, and how many places describe the same data.
2. **The change.** The resource added beside what exists. Only the new lines. A count of files and lines added and removed.
3. **What it gets.** The same input refused the same way from the form, the Tool API tool and HTTP.
4. **Later, if ever.** What declaring more, or retiring the hand-written form, would change, and whether it is worth it here.
5. **Another module's view.** How a module that adds to this one does so, before and after.
6. **What stays as it is.**
7. **Try it.**

### A part of the core path (`docs/path/`)

1. **What it is**, in two sentences.
2. **What core gains, and the core change** it needs, with issue links.
3. **What exists** in the proof of concept.
4. **Considered and set aside**: the alternatives already weighed, one line each with why.
5. **Open to improve**: what is still on the table.
6. **Validation cases**: which retrofits prove it.
7. **Ready when**: the checklist.
8. **How to help**: three to five concrete tasks.

## Building

```bash
pip install -r requirements.txt
git submodule update --init
mkdocs serve
```

`mkdocs build --strict` must pass before a push.
