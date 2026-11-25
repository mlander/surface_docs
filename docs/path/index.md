# The path into core

The proof of concept works from end to end, but core does not take it as one piece. It moves in five steps. Each is reviewed by the maintainers of the subsystem it touches, needs only the steps before it, and pays off on its own.

## The sequence

1. **Facts on a data definition** ([Groundwork in core](groundwork.md)). Typed Data, validation and the Field API learn to state a default, examples, labels for choices, and rules that depend on another key. Core's existing JSON Schema output shows these facts with no other change, and every later step reads them.
2. **Operations for simple config** ([Resources and operations](resources-operations.md)). A config object gets named operations beside its form, each with a permission, and a write through one is validated. Every settings object that adopts it gets one set of checks at every way in, and a Tool API tool per operation.
3. **Another module's keys** ([Structures](structures.md#another-module)). A place in a simple config object for another module's keys, as config entities have third-party settings. A module adds its own setting to another module's settings, under the same checks.
4. **A served contract** ([Portable Schema](portable-schema.md)). What each operation accepts, served as JSON Schema and never stricter than the validation that judges the write. Tool API, HTTP clients and headless forms read one document.
5. **Form API, when wanted** ([Forms](resources-operations.md#forms)). A form generated from the same description, which a module adopts at its own pace. The hand-written form can then go.

[Structures](structures.md) run through all five: read from config schema and field definitions from step 1 on, and declared in Portable Schema as modules convert. Nothing asks Form API to change before step 5.

## How a step moves

Each step is prototyped in the proof of concept, extracted as a change to one core subsystem, tried on real core and contributed modules ([How each piece is validated](validation.md)), filed as a core issue that stands on its own, and reviewed by that subsystem's maintainers. What review changes goes back into the proof of concept.

Three step 1 issues are open in core's queue. The rest of step 1 is drafted in the proof of concept's [core gaps](https://git.drupalcode.org/project/surface/-/blob/d5486fd4/docs/core-gaps.md#the-order). Steps 2 to 5 are not drafted.

## What stays out

HTTP and OpenAPI, staged edits, a React client and a code generator stay in the proof of concept and are not proposed now ([Stays in the proof of concept](stays-in-poc.md)).

The proof of concept shows that the definitions core has, plus the facts of step 1, are enough to state a settings object's rules once and hold every way in to them. It does not show that this order is the only one, or that its PHP API is the one core should adopt. Where the pieces land in core, and under which names, is an [open question](../open/index.md#where-the-parts-land). Whether each fits a minor release is checked on [Release fit](release-fit.md).
