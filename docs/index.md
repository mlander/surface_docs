# Describe it once

Drupal describes the same data several times. A block plugin with settings writes a config schema file, `defaultConfiguration()`, a form in `blockForm()`, checks in `blockValidate()` and copying in `blockSubmit()`. In Drupal core 11.4 the site name is described in 6 places, a content type's "Create new revision" setting in 5, and the menu block's number of levels in 6. A Tool API tool or an HTTP client needs it described once more.

The copies can disagree, and each is only checked where it lives. A check written in a form does not run when a recipe or a config import sets the value. None of the existing places can be grown to hold all of it: config schema describes what is stored, a form is PHP code nothing else can read, and a config action has no description of its input.

## The direction

A module describes its data once. Three concepts carry it:

- **[Structures](path/structures.md).** The description of a thing's data: each key, its type, its choices and its rules. A structure is declared in Portable Schema, or read from the config schema and field definitions a module already has, as a bridge until it converts. A structure has no actions of its own. A block plugin's settings, a field type's settings and a condition plugin's settings are structures: data shapes that something else stores and acts on.
- **[Resources and their operations](path/resources-operations.md).** A resource is a structure with identity, storage and permissions, and the named actions on it, such as "update the site information" or "place a block". A config object, a placed block and a content type are resources. Each operation is one action, with its input, its permission and its checks.
- **[Portable Schema](path/portable-schema.md).** How structures and resources are written down and served: JSON Schema, with a small agreed set of extension keywords. It is a library that does not depend on Drupal, with validators in PHP and JavaScript that give the same answers. A resource's operation input and a plugin's settings are described in the same way.

## Add it once, beside what exists

The ask is one new input layer beside forms. Every way in reads it, so all of them accept and refuse the same values.

- **Additive.** It [builds on](why/builds-on.md) config schema, field definitions, constraint plugins, JSON Schema, Form API and entity storage and access. Core's first changes are small patches to Typed Data, validation and the Field API, each fit for a [minor release](path/release-fit.md). Nothing is removed to make room.
- **Opt in.** Nothing changes until a module chooses, and stored data does not change. Existing config schema and field definitions are read as they are.
- **A small first step.** A module adds one resource class beside its form. Each of its operations gets Tool API tools and HTTP calls, and the same checks at every way in. For the site information settings that is 46 lines of code ([Site information](adopting/site-information.md)).
- **Forms when wanted.** A generated form replaces a hand-written one at the module's own pace, or never. `hook_form_alter()` still works on it, and since it is drawn from the [Portable Schema](path/portable-schema.md) document, a headless client can draw the same form.
- **Deprecation on core's schedule.** Older APIs are deprecated only once the new ones are in use, [in a minor release and removed in the next major](https://www.drupal.org/about/core/policies/core-change-policies/allowed-changes#s-deprecations).

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
