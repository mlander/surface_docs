---
topic: resource
---

# Resources and operations

A resource is a thing with identity and storage: a config object, a config entity, a content entity or a plugin's settings, with who may change it. An operation is a named action on it, such as "update the site information" or "place a block", with a structure for its own input and a permission; a form, a Tool API tool, an HTTP call and Drush are each one way to run it.

## What core gains, and the core change

Entity types already have operations, access per field and validation on write, so a resource is derived for each one today. A simple config object has none of it: a `ConfigFormBase` subclass and a route with `_permission`, and `Config::save()` casts values without checking a constraint. A Drush command, a config action, a REST endpoint or an agent that writes a settings object asks no permission and runs no validation unless its author wrote them.

[Step 2](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/core-gaps.md#step-2-operations-and-access-for-simple-config): a simple config object may name its operations, each with a permission, and an optional access handler that answers per key, as `fieldAccess()` does per field. A write through an operation validates against the config schema before it saves. Not drafted as an issue.

### Where an operation's keys come from {#keys}

The proposal for step 2:

- **Read by default.** An operation names the keys it takes. Each key's type, label and constraints are read from the config object's existing schema. Config schema is not changed, and neither are config import validation, config translation or typed config, which read it.
- **Declared where config schema cannot say enough.** A fixed list of choices with labels, a rule that depends on the site, a comparison between two keys, or input that is never stored. The declared key is checked against the config schema at its path, so it can only narrow what config schema allows.
- **Generated only on opt-in.** A module that owns its config object and declares its keys may write its config schema from them with a build-time command. The file is committed, and a test fails when the two drift. Core reads an ordinary config schema file either way, so step 2 does not need the generator.

For core's `system.site`, rung 1 is then six key names and a permission. The cost is the labels: config schema's are short ("Max age") where a form's titles are fuller, so a Tool API tool shows the shorter ones until the module declares the key.

Not yet in the proof of concept: naming keys and reading the rest. Today a resource over a config object declares each key it takes, and is checked against the config schema core wrote or generates its own ([decision](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/decisions.md#a-config-object-is-described-by-its-resource)). That decision becomes the opt-in above. Generated forms are [step 5](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/core-gaps.md#step-5-form-api-last).

## Operations

An operation is declared on the resource's class with an attribute, as plugins and hooks are declared. The newsletter settings of the first example, whose keys are on [Structures](structures.md#declared-in-code):

```php
--8<-- "modules/surface_examples_first/src/Resource/NewsletterResource.php:18:27"
```

That is the whole resource apart from its keys and a storage class naming the config object. A route that names the resource and the operation is a working form with no form class, and one Tool API tool per operation is derived from it. A method in place of the attribute is needed only when the operation knows more: identity, a constraint or defaults ([decision](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/decisions.md#an-operation-on-the-class)). One service runs every operation for every caller in one order: the permission before anything is loaded, then access, then validation, then the write ([decision](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/decisions.md#one-runner-runs-an-operation)).

## Access

An operation names a permission that exists. It creates none, so the permissions list does not grow; the expected choice is the permission the settings form's route asks for today. A config object that only a form's route guarded stays closed to every other caller until its owner names the permission. Core does not guess it.

Beyond the permission, an access class may answer per key: open, locked (shown and fixed) or left out, as field access has a field one may see and not change ([decision](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/decisions.md#access-has-three-answers)). Whether an answer can be stated ahead of time is read from its cacheability, never declared: one that varies only by permissions or roles is stated in a cached schema for the account that asks ([decision](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/decisions.md#access-is-static-or-runtime-read-from-its-cacheability)). A resource that acts on another module's things asks that thing's access each time, so it holds whatever node grants or a workflow module add ([decision](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/decisions.md#a-gate-is-borrowed-never-copied)).

## Validation

One validation for every way in. A write through an operation validates the whole config object, the written values laid over what is stored, against its config schema before anything is saved ([decision](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/decisions.md#the-whole-object-is-checked)). In the Honeypot port, three `validateForm()` rules that ran only in the form, and one permission, now hold at the route, the form, the Tool API tool and the HTTP API alike.

Only the new way in is strict. `Config::save()`, a config action and a hand-written form behave as they do today.

## Storage

Storage stays where it is. A storage class loads, prepares and commits: a simple config object, a config entity through its own `save()`, a plugin's configuration, a content entity. Adopting needs no update path and leaves a config export as it was. A resource may hold only the keys of a config object that its form edits: `system.performance`'s page cache maximum age at `cache.page.max_age`, with the keys beside it kept byte for byte ([decision](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/decisions.md#a-resource-may-hold-some-keys-of-a-config-object-it-does-not-own)).

## Forms

A form is one way to run an operation. A hand-written form can keep running it, and can read one more fact at a time from the description: `#options` from a labeled `Choice`, a key disabled where access locks it. Generated forms are optional: one generic form per operation, built from Form API elements. They handle complex forms out of the box: grouped keys, keys that depend on another key's value, and forms in several steps. Cosmetic overrides stay in Form API: a class that alters the generated render array, such as the block placement form's message and redirect, changes how it looks, never what a value means. A module adopts a generated form at its own pace, or never ([the adoption ladder](../adopting/index.md)).

Two things in Form API work against a generated form today, and step 5 is where they would change: `#states` and an element's own checks run apart from the definition's rules, and a form keeps only the first error per element; and an element does not read its own value back in the shape its definition describes. The proof of concept clears the element's server-side check and keeps its limits as browser hints, so the rule's own message is the one shown ([decision](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/decisions.md#an-element-hints-and-the-rule-speaks)).

The ports are not smaller. Honeypot's form class was 201 lines and its port is 216, of which the resource class is 48. What changed is that every rule holds at every way in.

## Widgets

Field widgets are not changed. A generated form draws each key with its own small set of widgets, chosen from the key's schema alone, and a resource may ask for one by name where the schema does not settle it ([decision](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/decisions.md#a-widget-is-chosen-from-the-definition)). Whether field widgets and those widgets grow toward one shared contract is a [question for another day](../open/later.md).

## Considered and set aside

- **Declaring every key in code as the default.** Each key core's config schema already describes would be written a second time, and rung 1 would be a class of key declarations instead of a list of names.
- **Generating config schema as the default.** Two files could describe one object during the transition, and core would need a rule for which one wins.
- **A new permission per operation.** It would grow the permissions list and leave the existing route permission and the new one to disagree.
- **Copying another thing's access check** ("has edit any page content"). It agrees with the owner's answer only until a module that changes access is enabled.
- **Mapping a form element's error back to the rule's message.** That keeps two checks that can disagree.
- **Extending `ConfigFormBase`.** `copyFormValuesToConfig()` is private static, so a generated form replaces it rather than extends it.
- **A form class per operation.** One generic form serves every operation; none of the ported plugins needed its own ([adoption](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/adoption.md#group-d-multiple-named-forms)).

## Open to improve

- Where a config object names its operations: a PHP class with an attribute, as the proof of concept does, or an `operations:` key on the object's config schema.
- `#config_target` and its `toConfig` and `fromConfig` callbacks are not read yet, so a form that has them and a resource do not yet describe the same thing.
- [Recording who ran what](../open/index.md#observability): every way in runs through one place, and what that place records is not settled.
- A config entity's dependencies on content are added when it is saved through an operation, and dropped when it is saved any other way.
- Through the Tool API tool, an edit sends required keys again on every call. A decision is pending.

## Validation cases

Simple config (adoption group F: the first example's settings and `system.performance`), config entities (group E: content types and placed blocks), multiple named forms (group D), and the Honeypot and Pathauto ports. See [How each piece is validated](validation.md#resources-and-operations).

## Ready when

- [ ] A core settings form gets a resource beside it with no change to its config schema, its stored config or its form.
- [ ] The same refused value is refused with the same message from the form, the Tool API tool, Drush and HTTP.
- [ ] The question of where operations are named is decided.
- [ ] The configuration system and Form API maintainers have reviewed it.

## How to help

- Pick a core settings form and list its operations and the permission each would name.
- Compare the resource's access answers with a real `fieldAccess()` implementation.
- Read `#config_target` in a resource, so a form that has it and the resource agree.
- Try a hand-written form that reads its `#options` from the description.
