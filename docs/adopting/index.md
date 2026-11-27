# Adopting it

A module adopts by adding a resource class beside the form(s) it already has. One resource can cover several forms, such as a placed block's add, edit and delete forms, each as one operation. The class names the thing, where its values are stored, and its operations, each with a permission that already exists. The forms, their routes, stored config and config schema stay as they are.

## The ladder

A module climbs at its own pace. Each rung works without the next.

| Rung | The module | It gets |
|---|---|---|
| **0. Nothing** | Changes nothing. | A resource in another module can still offer this module's config and fields API-first, with their structures read from its config schema and field definitions. |
| **1. A resource beside the form(s)** | Adds a resource class with its operations, and for simple config a storage class that names the config object. | API-first: each operation is a Tool API tool, an HTTP endpoint described in OpenAPI and a Drush command, with one permission and one validation at every way in that runs it. |
| **2. An explicit structure** | Declares a plugin's settings in Portable Schema, with the rules that are code. | Choices that depend on the site, rules between keys, keys that depend on another key's value. |
| **3. The generated form(s)** | Points each form's route at the generated form for its operation. Optional. | The hand-written forms can go. A module that alters one of them has to move its alter ([What contrib sees](contrib.md)). |
| **4. Old code removed** | Deletes the hand-written form classes, often whole, since `buildForm()`, `validateForm()` and `submitForm()` have nothing left to do, and the duplicate defaults. What stays bespoke is cosmetic, such as grouping, a success message or a redirect, and moves to a form alter. | Less code to keep in step. |

Stored config and config schema do not change at any rung.

A module declares in Portable Schema the keys of config it owns. It writes the class anyway, and a declared key carries its title, description, default and checks to every way in. It reads keys from config schema only for config another module owns and has not converted, so the owner's rules are not copied into a module that does not own them. A plugin's settings stay read until the plugin declares them at rung 2.

Rung 3 is the first rung that costs another module anything, which is why it comes late and is optional, but recommended.

## Worked examples

Each is built and tested in the proof of concept, on code from core or a contributed module.

- **[Example 1: Site information](site-information.md).** A basic settings form. A config object gets an operation with the permission its route asks today, and every key declared in Portable Schema.
- **[Example 2: Placing a block](place-block.md).** A block that declares its structure and core's branding block, which has only config schema, placed through one resource.
- **[Example 3: Fields and Tool API tools](fields-and-tools.md).** One field resource with three operations becomes three Tool API tools whose inputs agree, compared with Tool Belt's `field_add`.
- **[What contrib sees](contrib.md).** What changes for a contributed module at each rung.
