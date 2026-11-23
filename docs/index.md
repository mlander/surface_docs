# Describe it once

Drupal describes the same data several times. A block plugin with settings writes a config schema file, `defaultConfiguration()`, a form in `blockForm()`, checks in `blockValidate()` and copying in `blockSubmit()`. In Drupal core 11.4 the site name is described in 6 places, a content type's "Create new revision" setting in 5, and the menu block's number of levels in 6.[^counts] A Tool API tool or an HTTP client needs it described once more.

The copies can disagree, and each is only checked where it lives. A check written in a form does not run when a recipe or a config import sets the value. None of the existing places can be grown to hold all of it: config schema describes what is stored, a form is PHP code nothing else can read, and a config action has no description of its input.

## The direction

A module describes its data once. The form, the validation, the Tool API tool, the HTTP call and the published description all read from that one description, so they accept the same values and refuse the same values in the same words.

Three concepts carry it:

- **[Structures](path/structures.md).** The description of a thing's data: each key, its type, its choices and its rules. Most structures are read from the config schema and field definitions a module already has.
- **[Resources and their operations](path/resources-operations.md).** The thing itself, where it is stored and who may change it, and the named actions on it, such as "update the site information" or "place a block".
- **[Portable Schema](path/portable-schema.md).** How a structure is written down and served: JSON Schema, with a small agreed set of extension keywords.

## An evolution, not a new system beside Drupal

- **Nothing changes until a module chooses.** Existing config schema and field definitions are read as they are. A block that has only config schema can already be placed through a resource.
- **The first step is small.** A module adds one resource class beside its existing form. The form keeps working. Stored config does not change.
- **Each step only adds.** No API is removed or deprecated. Each change on the path is sized for a [minor release](path/release-fit.md).
- **Generated forms come last, and only where wanted.** A module may replace its hand-written form with one read from the description, at its own pace, or never.

It builds on what core has: constraint plugins, JSON Schema, `#config_target`, Form API elements, entity storage and access. A plugin is still a plugin, an entity is still an entity, config is still config.

## Where to go next

- **[See it on real code](adopting/index.md).** Placing a block, the site information settings, and field settings as Tool API tools, each as a small change beside what exists.
- **[Why not Tool API?](why/not-tool-api.md)** It has a role in this. Surface takes its idea one step further.
- **[The path into core](path/index.md).** How the proof of concept is split into pieces core can review, and how each is validated.
- **[The board](board.md).** Every talking point, how solid it is, and where help is needed.

## How to read this site

A lot of thought has gone into this, and the pages say what was decided and why. There is also plenty of room to improve it. Each page says what is still open, and [Proposing a change](open/proposing-a-change.md) says how to revisit something already decided. Some parts are settled after long design work; others are first sketches. Each talking point carries [a maturity level](about/maturity.md) so you know which is which.

The work is done in the [Surface API proof of concept](https://www.drupal.org/project/surface). It is on drupal.org for its issue queue and repository while it is prototyped, and will have no full release. The goal is for its parts to move into core once they are ready.

[^counts]: A place counts when it states the type, the label, the default, the allowed values or a rule for the value. Code that only reads the value does not count. Site name: the config schema, the installed default, the site information form, the installer's form, the branding block's off-canvas form, and the install command's `--site-name` option. "Create new revision": the config schema, the `NodeType` class, `NodeTypeInterface`, the content type form, and the config action on the setter. Menu block levels: the config schema, `defaultConfiguration()`, `blockForm()`, `blockValidate()`, `blockSubmit()`, and a constraint validator.
