# Adopting it

The first real step asks for one thing: a resource class beside the form a module already has. The class names the thing, where its values are stored, and its operations, each with the permission it asks. The hand-written form stays where it is and keeps working. Stored config does not change. Config schema does not change. Routes do not change.

Before that step there is a rung that asks for nothing at all. Config schema and field definitions are read into structures as they are, so a block that has only config schema can already be placed through a resource, with no change to the block.

## The ladder

A module climbs at its own pace. Every rung works without the next one, and a module can stop on any rung for good.

| Rung | What the module does | What it gets | What it does not touch |
|---|---|---|---|
| **0. Nothing** | No change. This is the default. | Its config schema and field definitions are read into structures. A block with only config schema is reachable as a resource the day core ships the placement resource. | Everything. |
| **1. A resource beside the form** | Adds one resource class with its operations, and for simple config a storage class that names the config object. | One validation for every way in that runs the operation, a Tool API tool per operation, an HTTP call, and a served JSON Schema of what each operation accepts. | The hand-written form, its route, stored config, config schema, the permission list. |
| **2. An explicit structure** | Declares the structure in code where config schema cannot say enough. | Choices that depend on the site, rules between keys, keys that depend on another key's value, input that is not stored. | The same as rung 1. |
| **3. The generated form** | Points the route at the operation's form. Optional. | The hand-written form can go. | Stored config and config schema. The form id and element tree change, which matters to modules that alter the form ([What contrib sees](contrib.md)). Core's policy does not keep a form's element tree stable ([render arrays](https://www.drupal.org/about/core/policies/core-change-policies/frontend-bc-policy#render-arrays)). |
| **4. Old code removed** | Deletes `buildForm()`, `validateForm()`, `submitForm()` and the duplicate defaults. | Less code to keep in step. | Stored config and config schema. |

Rung 0 costs nothing, and reading never has to stop. An entity's fields are set up on each site, so their structure is always read. A settings object with fixed rules can keep its config schema as the source for good. Declaring a structure in code (rung 2) pays off where the rules are code: a list that depends on the site or on another key, a comparison between two keys, or input that is never stored.

Rung 3 is late and optional. A generated form is one more way to run an operation that already works without it. Nothing on rungs 0 to 2 depends on it, and each owner takes it at its own pace, or never. It is the first rung that costs another module anything, which is why it sits this high.

## Worked examples

Each example is built and tested in the proof of concept, on code that exists in core or a contributed module. Each says what was added, in files and lines, and what was left untouched.

- **[Placing a block](place-block.md).** Rungs 0 and 2 side by side. A block plugin that declares its own structure is placed through it. Core's branding block, which has only config schema, is placed the same way, with its structure read from that config schema and no change to the block.
- **[Site information](site-information.md).** Rung 1 on simple config: a config object gets a named operation that asks the permission core's route asks today. The `system.site` code is written for the page; the same step on `system.performance` is in the proof of concept and tested.
- **[Fields and Tool API tools](fields-and-tools.md).** One field resource with three operations becomes three Tool API tools whose inputs agree, compared with Tool Belt's `field_add` on the address field type.
- **[What contrib sees](contrib.md).** What changes for a contributed module at each rung, and what does not.

## Open to improve

- **Rung 1 for simple config lists its keys again.** In the proof of concept a resource over a config object declares each key it edits, and is either held to the config schema core wrote or generates the config schema itself. Step 2 proposes that an operation name its keys and read them from the config object's schema, declaring only a key config schema cannot describe ([Where an operation's keys come from](../path/resources-operations.md#keys)). That is not yet in the proof of concept.
- **A hand-written form running the operation.** Step 2's core change lets a hand-written `ConfigFormBase` ask the same operation, so the form gets the same checks without being generated ([core gaps, step 2](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/core-gaps.md#step-2-operations-and-access-for-simple-config)). No worked example shows that yet: on each of them, core's own form still saves the way it does today.
- **More examples.** Candidates are the content type (`surface_examples_node_type`), a setting one module adds to another module's form, a plugin with two sets of settings, and a config entity. The proof of concept's [adoption notes](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/adoption.md) group core's forms by how much work each family needs.
