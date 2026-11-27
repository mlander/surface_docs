# What it builds on, and what it could consolidate

Everything here sits on systems core already has. A plugin is still a plugin, an entity is still saved by its own storage, and config is still config. Permissions, routes and cache metadata work as they do today.

Beside existing code it adds an optional route for a generated form, and an access check on routes that run an operation, asking the permission the operation names. It also serves every operation over HTTP, described in one OpenAPI document.

## What it builds on

The one new piece is the description and the operations that run through it. It builds on:

- **Config schema and field definitions.** Read into structures for config another module owns and has not converted, and for plugins and config with no resource class.
- **Constraint plugins.** A check with no JSON Schema keyword, such as core's `ValidPath`, runs as core's constraint plugin. Keyword checks, such as a length or a pattern, run in Portable Schema's validator.
- **JSON Schema.** Core already derives it from Typed Data and uses it for component props. A structure is written in it.
- **Form API elements.** A generated form is built from them. Field widgets do not change.
- **Tool API.** Every operation is published as a Tool API tool.
- **Entity storage, access and existing permissions.** A resource for an entity type uses its storage and access. An operation names a permission that already exists and creates none.

## What it could consolidate {#consolidate}

What is written several times today could be written once. Each line takes effect only where a module adopts the step it depends on.

| Today | With one description |
|---|---|
| A settings form's `buildForm()`, `validateForm()` and `submitForm()` | Generated from the description. A hand-written form still works. |
| A block plugin's config schema, `defaultConfiguration()`, `blockForm()`, `blockValidate()` and `blockSubmit()` | One declaration |
| Separate input descriptions for recipe inputs, config actions and Tool API tools | Read from the operation |
| Several Tool API tools for the actions on one thing, each with its own input | One resource with several operations sharing one structure |
| A different alter hook per system for the same data | One way to add keys to a description, with a known owner for each key. Existing hooks keep working. |
| Hand-written config schema for keys a module owns | Generated from the structure the module declares. Hand-written config schema keeps working. |

Portable Schema is meant to eventually succeed Typed Data and config schema. That is a long way off, and both keep being read in the meantime.

Most of the gain is in contributed modules and comes at the later rungs of [the adoption ladder](../adopting/index.md). The first rung with a resource class already gives one validation for every way in and a Tool API tool per operation.
