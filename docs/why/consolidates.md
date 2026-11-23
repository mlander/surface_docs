# What it could consolidate

What is written several times today could be written once. Nothing in this table happens on its own: each line takes effect only where a module chooses to adopt the step it depends on.

| Today | With one description |
|---|---|
| A settings form's `buildForm()`, `validateForm()` and `submitForm()` | Read from the description. A hand-written form still works. |
| A plugin's five settings methods | One declaration |
| Separate input descriptions for recipe inputs, config actions, Tool API tools and HTTP | Read from the operation |
| Several tools for the actions on one thing, each with its own input | One resource with several operations sharing one structure |
| A different alter hook per system for the same data | One way to add to a description, with a known owner for each key. Existing hooks keep working. |
| Hand-written config schema | Can be generated from a structure, and stricter than most hand-written files. In the long term this could make writing config schema by hand unnecessary. |
| Typed Data for storage and JSON Schema for props and APIs | They could converge on JSON Schema over time. Typed Data and config schema keep being read. |

Most of the gain is in contributed modules, and none of it arrives until the later rungs of [the adoption ladder](../adopting/index.md). The earlier rungs pay off differently: one validation for every way in, and a Tool API tool, from the first step.
