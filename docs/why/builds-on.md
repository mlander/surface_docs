# What it builds on

Everything here sits on systems core already has. A plugin is still a plugin, an entity is still saved by its own storage, and config is still config. Permissions, routes and cache metadata work as they do today.

Beside existing code it adds an optional route for a generated form, and an access check on routes that run an operation, asking the permission the operation names. It also serves every operation over HTTP, described in one OpenAPI document.

The one new piece is the description and the operations that run through it. It is new because no existing system can hold what the others need ([One more description](one-more-description.md)). It builds on:

- **Config schema and field definitions.** Read into structures for config another module owns and has not converted, and for plugins and config with no resource class.
- **Constraint plugins.** Every check runs as a core constraint plugin.
- **JSON Schema.** Core already derives it from Typed Data and uses it for component props. A structure is written in it.
- **Form API elements.** A generated form is built from them. Field widgets do not change.
- **Tool API.** Every operation is published as a Tool API tool.
- **Entity storage, access and existing permissions.** A resource for an entity type uses its storage and access. An operation names a permission that already exists and creates none.
