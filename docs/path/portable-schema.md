---
topic: served-contract
---

# Portable Schema

Portable Schema is how a [structure](structures.md) is written down and served. It is JSON Schema 2020-12, the dialect core's serialization module already writes, plus a small agreed set of extension keywords and fixed rules where the standard leaves a choice. It is a library by fago, with validators in PHP and JavaScript that give the same answers on one set of test fixtures.

## A served contract {#served}

A client that wants to send a valid write should learn the rules before it sends, not by being refused. Today core's serialization module describes what a normalizer outputs, and nothing describes what an operation on a config object or an entity accepts. Step 4 composes, for each operation from [step 2](resources-operations.md), a schema of what it accepts from the definitions [step 1](groundwork.md) enriched, and serves it beside the operation. A Tool API tool, a headless form and, in the proof of concept, the OpenAPI document then read the same schema.

The schema of the newsletter settings' "configure" operation, from [Structures](structures.md#declared-in-code), is plain JSON Schema with one extension keyword, `portable-check`, naming the `Email` constraint the server also runs:

```json
--8<-- "tests/fixtures/contracts/first.newsletter.json:27:74"
```

The served contract is never stricter than the validation that judges the write: what validation accepts, the schema accepts. Where a rule cannot be stated as a keyword, the schema stays wider and names the rule for the server to check. Tests run each example's accepted and refused values through validation and through a standard JSON Schema validator.

## Extension keywords

Plain JSON Schema keywords come first. Most of what core's definitions cannot say today has a standard keyword that core's output does not use yet: `maxLength`, `default`, `if`/`then` for a rule between keys, `writeOnly` for a secret. A generic validator reads all of them. A small set needs extension keywords:

| What it is for | Keyword |
|---|---|
| A rule only the server can check, such as a constraint with no standard keyword, and its message | `portable-check`, `x-portable-messages` |
| A group of keys chosen by another key's value | `portable-typeBy` |
| Hints for drawing a form: widget, placeholder, grouping, weight. Written only when a caller asks, so the contract names no widget | `x-portable-ui` |
| Where to ask the server for what the document leaves out, such as an entity lookup | `x-portable-links` |

Which dialect core adopts, and how its validators relate to the one core uses for component props, is an [open question](../open/index.md#schema-language).
