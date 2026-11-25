---
topic: tool-api
---

# Why not Tool API

Surface does not replace Tool API. It publishes every operation as a Tool API tool, and the proof of concept depends on Tool API.

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

## On real code

The field instance resource in the proof of concept has three operations: create a field, re-use an existing field, and update one. Each is published as a Tool API tool. Compared with a hand-written Tool API tool that adds a field to a bundle, these offer the field type's settings with their real choices and labels, where config schema gives only bare types. The same resource also produces the Field UI form. [Fields and Tool API tools](../adopting/fields-and-tools.md) shows both input schemas side by side.
