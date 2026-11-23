---
topic: facts-on-a-definition
---

# Groundwork in core

Small additive changes to Typed Data, validation and the Field API, so that a data definition can state what it cannot state today. They are not a concept of their own: they are what structures, resources and Portable Schema read from, and each one pays off alone, because core already has code that reads definitions.

## What core gains, and the core change

Step 1 of the proof of concept's [core gaps](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/core-gaps.md#step-1-facts-on-a-data-definition), in its order. Each item uses only the items above it. Items 1.4 and 1.5 each hold two changes.

1. **[A typed data prototype keyed by its definition.](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/core-gaps.md#11-a-typed-data-prototype-keyed-by-its-definition)** A correctness fix: two definitions of one type that differ only in their constraints stop sharing one cached prototype. Drafted, not filed.
2. **[Constraints as JSON Schema keywords.](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/core-gaps.md#12-constraints-as-json-schema-keywords)** The serialization module's schema writes `maxLength`, `minimum` and the rest from a definition's constraints. [#3627330](https://www.drupal.org/project/drupal/issues/3627330), "Validation constraints do not contribute to the JSON Schema".
3. **[A setter contract.](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/core-gaps.md#13-a-setter-contract)** An interface for the setters the core definition classes already share, so code that tightens a definition need not name a class. Drafted, not filed.
4. **[Default values and example values.](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/core-gaps.md#14-default-values-and-example-values)** Plain metadata on a definition, read by schemas and by `#placeholder`. [#3620920](https://www.drupal.org/project/drupal/issues/3620920) for defaults and [#3620922](https://www.drupal.org/project/drupal/issues/3620922) for examples.
5. **[Two constraints core is missing.](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/core-gaps.md#15-two-constraints-core-is-missing)** `LanguageExists`, beside `PluginExists` (drafted, not filed), and `UniqueItems` for a list whose items must differ (not drafted).
6. **[Labels on `Choice`.](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/core-gaps.md#16-labels-on-choice)** A `Choice` that carries the label of each allowed value, so the list that validates is the list a form offers. Drafted, not filed.
7. **[What narrowing means.](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/core-gaps.md#17-what-narrowing-means)** A conservative check of whether one definition allows no more than another. Not drafted.
8. **[Conditions that only narrow.](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/core-gaps.md#18-conditions-that-only-narrow)** "When pricing is paid, the ticket needs a price" declared on a definition, enforced by validation and written as `if`/`then`. Drafted, not filed.
9. **[Which siblings a definition depends on.](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/core-gaps.md#19-which-siblings-a-definition-depends-on)** A stored list of the sibling keys that narrow a definition, with no behavior beyond storing it. Drafted, not filed.
10. **[Field defaults and field access without an entity.](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/core-gaps.md#110-field-defaults-and-field-access-without-an-entity)** Asking a field's default and access for a bundle without building a throwaway entity. Drafted, not filed.
11. **[The global `t()` in static context.](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/core-gaps.md#111-the-global-t-in-static-context)** A change to the coding standards, not to core's code: `t()` as the sanctioned spelling in static declarations. Drafted, not filed.

Every new fact also appears in the JSON Schema core already derives. The [Rosetta tracker](https://mglaman.github.io/rosetta-tracker/) follows the related core issues.

## What exists in the proof of concept

Each item is working code there today, written so that it calls core's own method once core has one:

- Defaults and examples are stored on core's definition under the array keys the drafts propose, through one class, `DefinitionMetadata`.
- One table maps ten constraints to their keywords and back (`Contract\ConstraintKeywords`).
- `LabeledChoice` is a subclass of the same Symfony class core registers as `Choice`, so code that checks `instanceof` recognizes it.
- The narrowing check (`Refinement\Narrowing`), declared conditions (`Refinement\Condition`), and `LanguageExists` and `UniqueItems` as constraint plugins.
- One class runs core's constraints (`ConstraintRunner`), and `TypedDataFootprintTest` fails when another file starts to use Typed Data ([Typed Data at the edges](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/on-typed-data.md#what-stays-typed-data-at-the-edges)).

Tests pin each one: `RefinementIsolationTest` (1.1), `LabeledChoiceTest` (1.6), `NarrowingTypesTest` and `NarrowingInsideMapsTest` (1.7), `DeclaredNarrowingTest` (1.8).

## Considered and set aside

- **`new TranslatableMarkup()` in static declarations.** It builds the same lazy object `t()` returns, at twenty-two more characters a label, so 1.11 asks the standards to name `t()` instead ([decision](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/decisions.md#a-resource-or-structure-is-static)).
- **Matching `Choice` by plugin id.** Set aside for a subclass, because code that matches the id misses a subclass. The contributed Tool API matches by id today, so `LabeledChoice` does not reach its schema there.
- **Comparing two patterns, or a contributed constraint's options, when checking narrowing.** Set aside: the check keeps or refuses them, because a wrong "narrower" is worse than a refused change.
- **Writing every `Regex` as `pattern`.** Set aside: only patterns PHP and JavaScript read alike are written, and the rest are named as checked on the server ([decision](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/decisions.md#a-pattern-both-engines-read-alike)).
- **Config schema dynamic types for conditions.** They swap a whole type. They cannot add a constraint or make a key required, and nothing can write `if`/`then` from them.

## Open to improve

- The default value's method names collide with `BaseFieldDefinition::getDefaultValue()`, which takes an entity and means something else. The draft has to pick names.
- The constraint table is closed. A plugin type, a service tag or an optional interface on the constraint class would let a contributed constraint state its own keywords.
- How the labels on a `Choice` are translated in config schema YAML.
- Item 1.10 rests on less evidence than the others, because the entity side is paused.

## Validation cases

The menu block's levels and other block, condition and action settings (adoption group A), the content type's preview mode, whose labels live only in an enum today (group E), simple config forms (group F), and field types for 1.1 and 1.10 (group C). See [How each piece is validated](validation.md#groundwork-in-core).

## Ready when

- [ ] Each item has a core issue with a core-only reproduction where it fixes a bug.
- [ ] Each item's change is a patch against core, with tests, and the proof of concept calls core's method in place of its own.
- [ ] Each interface the items add methods to is checked against its `@api` status ([Release fit](release-fit.md)).
- [ ] The Typed Data, validation, Field API and serialization maintainers have reviewed the items in their subsystem.

## How to help

- Review the three open issues and their patches.
- File one of the drafted items, starting with 1.1, which comes with a core-only reproduction.
- Propose method names for the default value that do not collide with `BaseFieldDefinition`.
- Draft `UniqueItems` or the narrowing check (1.7), the two items with no draft.
