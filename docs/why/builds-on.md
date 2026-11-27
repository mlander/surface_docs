# What it builds on, and what it could consolidate

Everything here sits on systems core already has. A plugin is still a plugin, an entity is still saved by its own storage, and config is still config. Permissions, routes and cache metadata work as they do today.

Beside existing code it adds an optional route for a generated form, and an access check on routes that run an operation, asking the permission the operation names. It also serves every operation over HTTP, described in one OpenAPI document.

## What it builds on

The one new piece is the description and the operations that run through it. It builds on:

- **Config schema and field definitions.** Read into structures wherever a module has not declared its own: content entity fields, plugin settings, and config another module owns. A declared key is still checked against config schema at its path.
- **Constraint plugins.** Core's constraints stay. Those JSON Schema can state, such as a length or a pattern, are written as keywords a client can check itself; the rest, such as `ValidPath`, run on the server as core's plugins ([how each lands](../path/portable-schema.md#constraints)).
- **JSON Schema.** Core already derives it from Typed Data and uses it for component props. A structure is written in it, as Portable Schema.
- **Form API elements.** A generated form is built from them. Field widgets do not change.
- **Tool API.** When it is installed, every operation is published as a Tool API tool.
- **Entity storage, access and existing permissions.** A resource for an entity type uses its storage and access. An operation names a permission that already exists and creates none.

## What it could consolidate {#consolidate}

What is written several times today, or not at all, could come from one description. Each line takes effect only where a module adopts the step it depends on.

| | Today | With one description |
|---|---|---|
| **Forms** | Each form writes its own `buildForm()`, `validateForm()` and `submitForm()`, and follows Form API's good practice or not | Generated from the description, built the same way every time. A hand-written form still works. |
| **Component forms** | Canvas matches each component prop's JSON Schema to a field type and widget, which edit and store the value. A shape no core field type matches, such as a duration, needs a module to supply one. | A component's props schema is read as a structure, so its form is drawn the same way as any other. The proof of concept places a component in a block this way. |
| **Config schema** | Written by hand, apart from the form that edits the same keys | Stays for now. For keys a module declares, it can be generated from the declaration, with a test that fails when the two drift. |
| **What a write accepts** | Each way in reads and checks input its own way: a form's elements, a Drush command's arguments, a config action's | One pipeline at every way in: accept and coerce the input, validate it, map it to storage, then write |
| **Permissions** | The form's route asks the permission. A Drush command, a config action or a Tool API tool that writes the same settings asks none unless its author adds it | The operation names the permission, and every way in asks it |
| **Ways in** | A Tool API tool, an HTTP endpoint and a Drush command are each written separately, with their own input | Derived from the operations: each is one way to run the same operation |
| **The contract** | Each way in describes its own input, if it describes it at all | One document per operation, which every way in and every client reads. An alter on the description, such as another module adding a key or narrowing a rule, shows up in all of them alike. A form alter changes one form. |
| **Dry run** | Rare: a form's checks and its save are tied to the form, so no other way in can check without saving | Every operation can run without writing and answer what would change and what would be refused |
| **Observability** | Each way in logs, or not, on its own | Every write goes through one runner, so one place can record who ran what, through which way in, and what was refused |

!!! question "TBD"
    What the runner records itself, and what it leaves to logging and other modules, is an [open question](../open/index.md#observability).

Portable Schema is meant to eventually succeed Typed Data and config schema. That is a long way off, and both keep being read in the meantime.

Most of the gain is in contributed modules and comes at the later rungs of [the adoption ladder](../adopting/index.md). The first rung with a resource class already gives one validation and one permission for every way in, and a Tool API tool per operation.
