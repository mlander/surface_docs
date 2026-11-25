# What it builds on

Everything here sits on top of systems core already has. A plugin is still a plugin. An entity is still an entity, saved by its own storage. Config is still config. Permissions, routes and cache metadata work as they do today. What it adds sits beside them: one HTTP route that serves every operation, a route for a generated form where a module wants one, and an access check on those routes that asks the permission each operation names.

One thing is new: the description, and the operations that run through it. It is new because no existing system can hold what the others need. The existing systems can read from it, and otherwise work as they do today.

- **Constraint plugins.** Every rule the server checks is a core constraint plugin. Nothing new runs a rule.
- **Config schema and field definitions.** Read into structures as they are, as the bridge until a module declares the structure in Portable Schema.
- **JSON Schema.** Core already derives it from Typed Data for API responses and uses it for component props. A structure is written in it.
- **`#config_target`.** Core already maps a hand-written form's element to a config key and a violation back to the element. A generated form does the same from the description. The proof of concept does not read `#config_target` yet, so a form that has it and a resource do not describe the same thing until it does.
- **Form API elements.** A generated form is built from them. Field widgets are not changed.
- **Tool API.** Every operation is published as a Tool API tool.
- **Entity storage and access, and existing permissions.** A resource for an entity type uses its storage and access. An operation names a permission that already exists and creates none.
