# Adopting it

A module adopts by adding a resource class beside the form it already has. The class names the thing, where its values are stored, and its operations, each with a permission that already exists. The form, its route, stored config and config schema stay as they are.

## The ladder

A module climbs at its own pace. Each rung works without the next.

| Rung | The module | It gets |
|---|---|---|
| **0. Nothing** | Changes nothing. | Its config schema and field definitions are read into structures. A block with only config schema can be placed through a resource. |
| **1. A resource beside the form** | Adds a resource class with its operations, and for simple config a storage class that names the config object. | One validation for every way in that runs an operation, and a Tool API tool per operation. |
| **2. An explicit structure** | Declares a plugin's settings in Portable Schema, with the rules that are code. | Choices that depend on the site, rules between keys, keys that depend on another key's value. |
| **3. The generated form** | Points its route at the operation's form. Optional. | The hand-written form can go. A module that alters the form has to move its alter ([What contrib sees](contrib.md)). |
| **4. Old code removed** | Deletes `buildForm()`, `validateForm()`, `submitForm()` and the duplicate defaults. | Less code to keep in step. |

Stored config and config schema do not change at any rung.

A module declares in Portable Schema the keys of config it owns. It writes the class anyway, and a declared key carries its title, description, default and checks to every way in. It reads keys from config schema only for config another module owns and has not converted, so the owner's rules are not copied into a module that does not own them. A plugin's settings stay read until the plugin declares them at rung 2.

Rung 3 is the first rung that costs another module anything, which is why it comes late and is optional.

## Worked examples

Each is built and tested in the proof of concept, on code from core or a contributed module.

- **[Example 1: Site information](site-information.md).** A basic settings form. A config object gets an operation with the permission its route asks today, and every key declared in Portable Schema.
- **[Example 2: Placing a block](place-block.md).** A block that declares its structure and core's branding block, which has only config schema, placed through one resource.
- **[Example 3: Fields and Tool API tools](fields-and-tools.md).** One field resource with three operations becomes three Tool API tools whose inputs agree, compared with Tool Belt's `field_add`.
- **[What contrib sees](contrib.md).** What changes for a contributed module at each rung.
