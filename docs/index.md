# Describe it once

Drupal describes the same data several times. A block plugin with settings writes a config schema file, `defaultConfiguration()`, a form in `blockForm()`, checks in `blockValidate()` and copying in `blockSubmit()`. In Drupal core 11.4 the site name is described in 6 places, a content type's "Create new revision" setting in 5, and the menu block's number of levels in 6.[^counts] A Tool API tool or an HTTP client needs it described once more.

The copies can disagree, and each is only checked where it lives. A check written in a form does not run when a recipe or a config import sets the value. None of the existing places can be grown to hold all of it: config schema describes what is stored, a form is PHP code nothing else can read, and a config action has no description of its input.

## The direction

A module describes its data once. The form, the validation, the Tool API tool, the HTTP call and the published description all read from that one description, so they accept the same values and refuse the same values in the same words.

Three concepts carry it:

- **[Structures](path/structures.md).** The description of a thing's data: each key, its type, its choices and its rules. Most structures are read from the config schema and field definitions a module already has. A structure has no actions of its own. A block plugin's settings, a field type's settings and a condition plugin's settings are structures: data shapes that something else stores and acts on.
- **[Resources and their operations](path/resources-operations.md).** A resource is a structure with identity, storage and permissions, and the named actions on it, such as "update the site information" or "place a block". A config object, a placed block and a content type are resources. Each operation is one action, with its input, its permission and its checks.
- **[Portable Schema](path/portable-schema.md).** How structures and resources are written down and served: JSON Schema, with a small agreed set of extension keywords. It is a library that does not depend on Drupal, with validators in PHP and JavaScript that give the same answers. A resource's operation input and a plugin's settings are described in the same way.

## Add it once, beside what exists

The ask is to add the description once. Everything else reads from it.

- **Nothing changes until a module chooses.** Existing config schema and field definitions are read as they are. A block that has only config schema can already be placed through a resource.
- **The first step is small.** A module adds one resource class beside its existing form. The form keeps working. Stored config does not change.
- **New pieces sit beside existing APIs.** Nothing is removed or deprecated to make room. Each change is sized for a [minor release](path/release-fit.md). Once the new pieces are in use, older ones can be deprecated gracefully on core's usual schedule.
- **Forms follow when wanted.** A module may replace its hand-written form with one read from the description, at its own pace, or never. Once every way in reads the same description, other parts of core that copy and transform input can be simplified over time.

The first change is a new input layer beside forms. It describes each action's input once, and Tool API tools, Drush, recipes and HTTP clients read it. A form can read from the same layer right away, or later at its own pace.

It builds on what core has: constraint plugins, JSON Schema, `#config_target`, Form API elements, entity storage and access. What it does not change:

- **Plugins, entities and config.** A plugin is still a plugin, an entity is still an entity, config is still config. Config storage, export and import work as they do today, and stored data does not change.
- **Routing and controllers.** Existing routes and controllers are untouched. A module adds a route only if it wants a generated form at a second path.
- **Permissions.** An operation names a permission that already exists. None are created.
- **Field widgets.** They are not changed.

## Why not more Tool API tools?

Core could add a Tool API tool for each action on each thing. One thing would then have several tools, each in its own file with its own input, and an alter would have to find and change each one. Or core could add one resource with its operations, and every operation is published as a Tool API tool. The tools come from the description, and so do the form's checks and the HTTP call. [Why not Tool API?](why/not-tool-api.md) compares the two.

## Where to go next

- **[Why not Tool API?](why/not-tool-api.md)** Tool API has a role in this. Surface takes its idea one step further.
- **[See it on real code](adopting/index.md).** Placing a block, the site information settings, and field settings as Tool API tools, each as a small change beside what exists.
- **[The path into core](path/index.md).** How the proof of concept is split into pieces core can review, and how each is validated.
- **[The board](board.md).** Every talking point, how mature it is, and where help is needed.

## How to read this site

Everything here is open to discussion. A lot of thought has gone into it. The proof of concept has ports of real contributed modules, a test suite, and a written record of each decision with the reason it was made. The pages link to those records. Some parts are more mature than others, and each talking point carries [a maturity level](about/maturity.md) so you can tell which. Every part can still be improved. [Proposing a change](open/proposing-a-change.md) says how to revisit something already decided.

The work is done in the [Surface API proof of concept](https://www.drupal.org/project/surface). It is on drupal.org for its issue queue and repository while it is prototyped, and will have no full release. The goal is for its parts to move into core once they are ready.

[^counts]: A place counts when it states the type, the label, the default, the allowed values or a rule for the value. Code that only reads the value does not count. Site name: the config schema, the installed default, the site information form, the installer's form, the branding block's off-canvas form, and the install command's `--site-name` option. "Create new revision": the config schema, the `NodeType` class, `NodeTypeInterface`, the content type form, and the config action on the setter. Menu block levels: the config schema, `defaultConfiguration()`, `blockForm()`, `blockValidate()`, `blockSubmit()`, and a constraint validator.
