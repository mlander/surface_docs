# The path into core

The proof of concept works from end to end, but core does not take it as one piece. It is split into pieces that core can review one at a time, each reviewed by the maintainers of the subsystem it touches. There are three concepts, the small core changes they read from, and the parts that stay behind.

## The pieces

| Piece | What it is | Steps in core | Expected to change shape |
|---|---|---|---|
| [Groundwork in core](groundwork.md) | Small additive changes to Typed Data, validation and the Field API, so a data definition can state a default, examples, labels for its choices, its conditions and its constraints as JSON Schema keywords. Not a concept of its own. | Step 1 | Little. Each item is a small patch, and its review settles its names and signatures. |
| [Structures](structures.md) | The description of a thing's data. Read from config schema and field definitions as they are, or declared in code where those cannot say enough. | Read from what step 1 completes. Another module's keys: step 3 | The idea of reading is stable. The PHP API for declaring keys is expected to change, and so are a structure's name and home in core. |
| [Resources and operations](resources-operations.md) | The thing itself, where it is stored and who may change it, and the named actions on it. A form, a Tool API tool and an HTTP call are each one way to run an operation. | Step 2. Generated forms: step 5 | Where a config object names its operations is open. Generated forms are the least settled part. |
| [Portable Schema](portable-schema.md) | How a structure is written down and served: JSON Schema, with a small agreed set of extension keywords. | Step 4, with the keywords of step 1 | The plain JSON Schema keywords are not expected to change. The extension keywords and the dialect are open. |
| [Stays in the proof of concept](stays-in-poc.md) | HTTP and OpenAPI, staged edits, a React client, a generator. | None | Not proposed now. |

The steps are the ones in the proof of concept's [core gaps](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/core-gaps.md#the-order), in that order:

1. **Facts on a data definition.** Small changes to Typed Data, validation and the Field API, and one to the coding standards.
2. **Operations and access for simple config.** A config object gets named operations, a permission each, and access per key, as entity types have.
3. **Third-party settings for simple config.** A place in a simple config object for another module's keys, as config entities have.
4. **A served contract.** A JSON Schema of what an operation accepts, never stricter than the validation that judges the write.
5. **Form API, last.** A form derived from the same description.

The order is bottom-up. Each step pays off in code core already has and needs no later step. Nothing asks Form API to change before step 5.

## How a piece moves

Every piece goes through the same loop:

1. **Prototype in the proof of concept.** The idea is built, tested and used by the examples there.
2. **Extract the piece.** Its smallest form is written as a change to one core subsystem, with what it reads from and what reads from it.
3. **Validate it on real retrofits.** The piece is tried on a fixed set of core and contributed modules and measured ([How each piece is validated](validation.md)).
4. **Open the core issue.** The issue states the gap in core's own terms, the change, and what a site gains from that change alone.
5. **Review with the subsystem's maintainers.** They decide the shape it takes in core.
6. **Iterate.** What the review changes goes back into the proof of concept, and the retrofits run again.

Three step 1 issues are open in core's queue: [#3620920](https://www.drupal.org/project/drupal/issues/3620920), [#3620922](https://www.drupal.org/project/drupal/issues/3620922) and [#3627330](https://www.drupal.org/project/drupal/issues/3627330). The rest of step 1 is drafted and not filed. Steps 2 to 5 are not drafted.

## What the proof of concept is evidence for

It shows that the definitions core already has, plus the facts of step 1, are enough to state a settings object's rules once and hold a form, a Tool API tool, an HTTP API and a schema to them. It does not show that this order is the only one, that its PHP API is the one core should adopt, or that content entities fit the same way. Its entity side is paused ([core gaps](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/core-gaps.md#what-this-module-is-evidence-for-and-what-it-is-not)).

Where the pieces land in core, and under which names, is an [open question](../open/index.md#where-the-parts-land). Whether each fits a minor release is checked on [Release fit](release-fit.md).
