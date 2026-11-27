---
topic: tool-api
human_reviewed: 2026-11-26
---

# Why not Tool API

Surface does not replace Tool API. It takes it a step further: when Tool API is installed, every operation is published as a Tool API tool automatically. Tool API is optional; without it, operations still run through forms and Drush. Much of the difference is naming. An operation and a Tool API tool describe the same action; Surface declares it on the thing it acts on.

## What Tool API does well

A Tool API tool gives an action one way in that many systems can run: Drush (`drush tool:run`), ECA, FlowDrop, Maestro and MCP servers. A module that provides one reaches all of them at once.

## What it leaves to each author

The actions on one thing are usually several Tool API tools: create a content type, update it, delete it. Each is its own plugin class with its own input definition, and nothing makes the definitions agree. A module that adds a setting to content types has to find and change every Tool API tool that takes content type settings, and the form, each in its own way.

## The step Surface takes

Surface describes the thing once, as a resource, and its actions as operations of that resource. Each operation is published as a Tool API tool.

- **One class instead of one per action.** Create, update and delete on a content type are three operations declared together.
- **Inputs agree because they come from one place.** Update takes the same keys as create, with the same checks and the same error messages. Where an operation takes fewer keys, it names them against the shared structure.
- **A change reaches every action at once.** A module that adds a key to the structure adds it to every operation that takes it, to every Tool API tool and to the form.

The Tool API tools still run everywhere Tool API tools run. What changes is where their input comes from.

## Hand-written Tool API tools still fit

A module still writes a Tool API tool where an action is not an operation on a resource, or where a smaller tool works better: one that takes fewer keys, fixes some values, or chains several operations for an orchestration flow or an AI agent.

Tool API takes Typed Data input definitions today and is to adopt Portable Schema as well. A hand-written Tool API tool and a published operation will then describe their input in the same schema language.

## Field CRUD both ways {#field-crud}

With Tool API tools, each action on a field is its own plugin class with its own input definition. Tool Belt ships these:

| File | Holds |
|---|---|
| `src/Plugin/tool/Tool/FieldAdd.php` | Adds a field to a bundle, using an existing storage |
| `src/Plugin/tool/Tool/FieldUpdate.php` | Updates a field on a bundle |
| `src/Plugin/tool/Tool/FieldDelete.php` | Deletes a field from a bundle |
| `src/Plugin/tool/Tool/EntityBundleFieldDefinitions.php` | Reads a bundle's field configuration |

With a resource, the field on a bundle is described once and each action is an operation on it. The proof of concept's field example:

| File | Holds |
|---|---|
| `src/Resource/FieldInstanceResource.php` | The field's structure and its operations: create with a new storage, reuse an existing storage, update. A read is added beside them; a delete would be one more operation here. |
| `src/Storage/FieldInstanceResourceStorage.php` | Where a field's values are kept: its field config entity |

What each gives:

| | Tool API tools | A resource |
|---|---|---|
| Tool API tools | One per class | One per operation, generated |
| Drush | `drush tool:run` | `drush tool:run` and `drush surface:run` |
| HTTP endpoints | None | One per operation |
| OpenAPI | None | One document for every endpoint |
| Form | Field UI's own, separate | Generated from the same structure |

A Tool API tool is an action with an input and an output. It has no identity, path or method, so nothing in its structure maps it to an HTTP endpoint or an OpenAPI document. An MCP server can expose it, as a tool call. A resource has identity keys and named operations, which map to a path and a method.

!!! question "TBD"
    HTTP and OpenAPI are assumed. Where they live, in core or in a module, is [open](../open/later.md).

## On real code

Compared with Tool Belt's `FieldAdd`, the field resource's Tool API tools offer the field type's settings with their real choices and labels, where config schema gives only bare types. [Fields and Tool API tools](../adopting/fields-and-tools.md) shows both input schemas side by side.
