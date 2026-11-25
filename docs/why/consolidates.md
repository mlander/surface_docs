# What it could consolidate

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
