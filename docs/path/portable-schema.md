---
topic: served-contract
---

# Portable Schema

Portable Schema is how a structure is written down and served. It is JSON Schema 2020-12, the dialect core's serialization module already writes, with fixed rules where the standard leaves a choice, so a PHP and a JavaScript validator give the same verdict, and a small set of extension keywords.

## What core gains, and the core change

A client that wants to send a valid write learns the rules before it sends, instead of by being refused. Today the serialization module's JSON Schema describes what a normalizer outputs, and nothing describes what an operation on a config object or an entity accepts.

[Step 4](https://git.drupalcode.org/project/surface/-/blob/d5486fd4/docs/core-gaps.md#step-4-a-served-contract): for an operation from step 2, compose a schema of what it accepts from the definitions that [step 1](groundwork.md) enriched, and serve it beside the operation, with the rule and the tests that it is never stricter than validation. Not drafted as one issue: its parts are step 1's, starting with constraints as keywords, [#3627330](https://www.drupal.org/project/drupal/issues/3627330).

## Served

Every document the proof of concept serves is a Portable Schema document. For the newsletter settings on [Structures](structures.md#declared-in-code), the schema of the "configure" operation is plain JSON Schema with one extension keyword, `portable-check`, naming the `Email` constraint the server also runs:

```json
--8<-- "tests/fixtures/contracts/first.newsletter.json:27:74"
```

The excerpt leaves out the document's `$schema` and the member that states the contract version and the operation's id and kind. The file is a committed baseline, and the test suite fails on a breaking change to it.

The served contract is never stricter than the validation that judges the write. What validation accepts, the schema accepts, judged on the values after coercion (a form's `"50"` for an integer becomes `50` first). Where a rule cannot be stated, the schema stays at the declared width and says so: a constraint with no keyword is named under `portable-check`, and a rule that reads site state is marked as settled by the server. Matrix tests run each example's accepted and refused values through validation and through both documents with a standard validator ([Never stricter than the runtime](https://git.drupalcode.org/project/surface/-/blob/d5486fd4/docs/served-contract.md#never-stricter-than-the-runtime)).

There are two documents, by one code path ([decision](https://git.drupalcode.org/project/surface/-/blob/d5486fd4/docs/decisions.md#two-documents-never-stricter-than-the-runtime)):

- **The schema for these answers**, for one set of values: each list narrowed for the sibling values as they stand. A form is drawn from it.
- **The full schema**, which reads no value and holds for any: every dependency that can be listed is written as `if`/`then`. A validator, or an agent planning its values, reads this one. The store location's region, for the first of its two countries:

    ```json
    --8<-- "tests/fixtures/contracts/first.store.json:87:119"
    ```

One document cannot do both: a list that depends on a sibling is either narrowed for one value, and wrong for the others, or written for all of them as conditionals, which a form would need a JSON Schema evaluator to draw from.

## Extension keywords

Plain JSON Schema keywords come first. Most of what a definition cannot say today has a standard keyword that core's output does not use yet: `maxLength`, `minimum`, `pattern`, `uniqueItems`, `default`, `examples`, `oneOf` of `const` and `title` for labeled choices, `if`/`then` for a rule between keys, `readOnly` for a locked key, `writeOnly` for a secret. A generic 2020-12 validator reads every one of them and ignores the rest.

A small set needs extension keywords:

| What the standard cannot say | Keyword |
|---|---|
| A rule only the server checks, and its message | `portable-check`, `x-portable-messages` |
| A value chosen by another key | Written today as `if`/`then`, with the deciding key named in the proof of concept's own `x-surface`. The dialect has `portable-typeBy` for it. |
| Hints for drawing a form | `x-portable-ui`: the widget, placeholder, grouping and weight. Written only when a caller asks, so the contract names no widget. |
| Where to ask the server for what the document leaves out | `x-portable-links`: an entity lookup, or one entry of a long list |

Portable Schema is by fago: a dialect of JSON Schema 2020-12 with reference validators in PHP and JavaScript that pass one set of conformance fixtures. Its `x-` keywords are annotations only, an unknown keyword is an error, and `format` is asserted. What the proof of concept still writes under its own `x-surface` (which keys a key depends on, and its markers) is expected to move into the dialect's keywords in later contract versions ([Contract 5](https://git.drupalcode.org/project/surface/-/blob/d5486fd4/docs/served-contract.md#contract-5)).

The schema language for core is an [open question](../open/index.md#schema-language).

## What exists in the proof of concept

- One emitter writes both documents (`Contract\ContractEmitter`), and a reader reads a JSON Schema document back into a structure (`Contract\SchemaReader`). `SchemaRoundTripTest` reads the shipped full schemas back into structures and compares the result with the original document.
- `AdvertisedSchemaAcceptanceTest` and `InputCoercionMatrixTest` check that the documents are never stricter than validation, and that validation runs through the dialect's validator.
- A React app renders a working form from the documents alone, with no PHP (`surface_examples_react`).
- Generated side by side with the Tool API's own description of the same data: the field tools against Tool Belt's `field_add` (`modules/surface_examples_field/COMPARISON.md`), and a setting another module added to content types (`modules/surface_examples_node_type_tool/COMPARISON.md`).

## Considered and set aside

- **One document for both uses.** Merged, it would make a drawing client evaluate conditionals to learn what a select offers; kept alone, it is true of one set of values only.
- **An OpenAPI `discriminator` for a group of keys chosen by a sibling.** A discriminator names a property inside the object it picks between, and here the deciding key is a sibling ([decision](https://git.drupalcode.org/project/surface/-/blob/d5486fd4/docs/decisions.md#no-openapi-discriminator-for-variants)).
- **Widget names in the contract.** They are hints a renderer asks for, under `x-portable-ui` ([decision](https://git.drupalcode.org/project/surface/-/blob/d5486fd4/docs/decisions.md#the-ui-hints-are-x-portable-ui)).
- **Every `Regex` as `pattern`, and `idn-email`.** PHP and JavaScript read some pattern constructs and international email addresses differently, so those are checked on the server only ([decision](https://git.drupalcode.org/project/surface/-/blob/d5486fd4/docs/decisions.md#a-pattern-both-engines-read-alike)).
- **A keyword vocabulary of the proof of concept's own.** Since contract 5 the served document is a Portable Schema document, and the proof of concept's own keywords moved into the dialect's ([decision](https://git.drupalcode.org/project/surface/-/blob/d5486fd4/docs/decisions.md#the-served-document-is-a-portable-schema-document)).

## Open to improve

- The schema language: which JSON Schema draft, which extension keywords, and one validator or two. Core validates component props with a different library, and its serialization tests check against an older draft.
- Portable Schema's PHP validator builds on opis/json-schema, licensed Apache-2.0, which Drupal core's GPL-2.0-or-later license cannot include. Its README says adding it to core would need a GPLv2-compatible PHP base.
- How a contributed constraint states its own keywords (step 1.2's optional interface).
- Reading a JSON Schema into data definitions, the other direction, is [#3627345](https://www.drupal.org/project/drupal/issues/3627345). It is not in the first steps; the proof of concept has a reader that does it today.

## Validation cases

Every example's committed baseline, the matrix tests over them, the two Tool API comparisons, and the React client. See [How each piece is validated](validation.md#portable-schema).

## Ready when

- [ ] Core's serialization module writes the keywords of step 1 for every definition it describes.
- [ ] A served contract for one simple config operation passes the matrix tests against core's validation.
- [ ] The schema language question is decided with fago and the serialization maintainers.
- [ ] The license question for the PHP validator has an answer.

## How to help

- Run a core config object's schema through a Portable Schema validator and a generic 2020-12 one, and report where they differ.
- Compare core's component props validator with the dialect's profile.
- Review the extension keyword table above against JSON Schema's next release.
- Write a client in another language against one served document.
