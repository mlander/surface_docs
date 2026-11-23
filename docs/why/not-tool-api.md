---
topic: tool-api
---

# Why not Tool API

Tool API has a role in this, and the proof of concept depends on it. Surface does not replace Tool API. It takes Tool API's idea one step further, and every operation it describes is published as a Tool API tool.

## What Tool API does well

Tool API gives an action one way in that many systems can run: the command line (`drush tool:run`), ECA, FlowDrop, Maestro and MCP servers. A module that provides a tool reaches all of them at once.

## What it leaves to each tool's author

Each tool states its own input. Actions on one thing are usually several tools: create a content type, update it, delete it. Each is its own plugin class, and each states its own input definition. Nothing makes the definitions agree. If a module adds a setting to content types, it has to find and change every tool that takes content type settings, plus the form, plus the HTTP endpoint, each in its own way.

## The step Surface takes

Surface describes the thing once, as a resource, and the actions on it as operations of that resource. The operations share one structure:

- **One class in place of one per action.** Create, update and delete on a content type are three operations of one resource, declared together.
- **Inputs agree because they are read from one place.** Update takes the same keys as create, with the same rules and the same words when a value is refused. Where an operation takes less, it says so against the shared structure.
- **A change reaches every action at once.** A module that adds a key to the structure adds it to every operation that takes it, to the form, to the Tool API tools and to HTTP. One change, made once, in one place.

So the tools are still Tool API tools, run by everything that runs Tool API tools. What changes is where their input comes from.

## On real code

The field instance resource in the proof of concept has create, reuse and update operations. Each becomes a Tool API tool. Compared with a hand-written tool that adds a field to a bundle, the tool read from the resource offers the field type's settings with their real choices and labels, instead of the bare types a config schema gives. The same resource also produces the Field UI form, with no second description. [Fields and Tool API tools](../adopting/fields-and-tools.md) shows both input schemas side by side.

## In one sentence

Where Tool API gives every action one way in, Surface gives every thing one description that all its actions, and every way in, share.
