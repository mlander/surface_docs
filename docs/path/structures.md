---
topic: structure
---

# Structures

A structure is the description of a thing's data: each key, its type, its choices and its rules, with what a caller needs to send a valid value. Most structures are read from the config schema and field definitions a module already has, and a module declares one in code only where those cannot say enough.

## What core gains, and the core change

One description that a form, validation, a Tool API tool and an HTTP client all read, so they accept and refuse the same values. Reading needs no new system: it needs the facts of [step 1](groundwork.md) on the definitions core already builds. Another module's keys are [step 3](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/core-gaps.md#step-3-third-party-settings-for-simple-config): simple config gains the `third_party_settings` place config entities and `theme_settings` already have.

Where a structure lives in core, and under which name, is [open](../open/index.md#where-the-parts-land).

## How a structure is made

### Read from config schema

The default, and a permanent one. A config schema type is read into a structure as it is: a mapping becomes a group of keys, a sequence a list, and a type named through a sibling key (`[%parent.plugin]`) becomes keys that depend on that sibling. The module writes nothing and changes nothing. A block that has only config schema can already be placed through a resource this way, its plugin's defaults laid over the schema (`BlockPluginStructures` in `surface_examples_block`). A module whose rules fit config schema may keep config schema as the source for good.

What the module has: `Reader\ConfigSchemaReader` ([Reading a schema](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/reading-a-schema.md#config-schema)).

### Read from field definitions

An entity type already has identity, storage, operations and access, so a resource for each bundle is derived from its field definitions, one structure per field. A field's structure is always read, because fields are set up on each site. The proof of concept derives `entity.content:node.page` and adds and edits a basic page through it. Multi-value fields, references, images and path aliases are not built, so this part rests on less evidence ([Content entities](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/entities.md#holes)).

### Declared in code

Declaring pays off where the rules are code: a list that depends on another key or on the site, a comparison between two keys, input that is never stored. The description and its logic then sit in one class and are checked together. A settings page's whole description:

```php
--8<-- "modules/surface_examples_first/src/Resource/NewsletterResource.php:37:63"
```

Each key is a JSON Schema written with a builder. The class can generate the config object's schema and install file (`drush surface:config-schema`), and a test fails when the committed files drift from it. In the long term this could make hand-written config schema unnecessary for such a module. Reading and declaring both stay supported.

## What a structure can say

### Keys that depend on another key {#variants}

Three forms, from the most declarative:

- **A rule stated as data.** "Without a license, at most 100": a condition from a closed list (`present`, `equals`, `atMost` and the rest) and an effect that only narrows. Written as `if`/`then` in the schema ([decision](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/decisions.md#a-rule-declared-as-data)).
- **A list narrowed by a sibling.** A static method returns the narrower list for the sibling's value. The schema states every case it can list:

    ```php
    --8<-- "modules/surface_examples_first/src/Resource/StoreResource.php:36:60"
    ```

- **A group of keys chosen by a sibling.** A block's settings chosen by its plugin id, as core stores them beside the plugin id. Read from config schema's `[%parent.key]` types or declared per value.

### Choices

A list of allowed values carries its labels, so the list that validates is the list a form offers and the schema states. Where the site decides the list (languages, content types, rooms of a venue), a class lists it for the site through the constraint that names the kind. The lists answer core's `OptionsProviderInterface`, so code that reads that interface needs no knowledge of the proof of concept ([decision](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/decisions.md#our-options-answer-cores-question)).

### Secrets

A key whose stored value is never read back (an API key, a password) is one keyword, JSON Schema's `writeOnly`:

```php
--8<-- "modules/surface_examples/src/Resource/WebhookResource.php:39:42"
```

The form draws a password field and keeps the stored value when left empty, the Tool API tool marks it write only, and no read at any depth returns it ([decision](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/decisions.md#a-secret-is-not-served-at-any-depth)). Whether core wants secrets in this form, and where they are encrypted, is not decided.

## Other modules

### Another module

A module adds its own keys to another module's structure in an alter class, and may only narrow what the owner allows, never widen it. Its keys are stored under `third_party_settings.<module>`, so the owner's storage and schema never need to know them ([decision](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/decisions.md#where-an-alters-keys-live)). The rule enforced is ownership: each key has one known owner, and only its owner may widen it. Where the keys are stored is not enforced; third-party settings, a key in the owner's schema and the module's own config object all keep working. A module that adds a license to an event registration, lifts the capacity rule with it, and rewords one label:

```php
--8<-- "modules/surface_examples_compliance/src/Alter/RegistrationComplianceAlter.php:34:35"

  // The translation trait, the State key and the constructor are left out.

--8<-- "modules/surface_examples_compliance/src/Alter/RegistrationComplianceAlter.php:56:72"
}
```

The owning class is unchanged and does not know the module exists. Today a form alter changes one form and nothing else that takes the same values, and `hook_config_schema_info_alter()` can loosen any module's rule with no record of who did. Here the same alter reaches the form, the Tool API tool and HTTP, and every narrowing is checked ([Typed Data at the edges](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/on-typed-data.md#why-each-part-is-not-core-alone)).

### Beside

Not built. Adding keys changes the owner's endpoints: a cached schema goes stale, a Tool API tool's input grows with every module enabled, and a tightened rule refuses a call that worked before the install. The direction accepted for data with its own id, storage or permission (meta tags, a URL alias, Paragraphs' children): a module declares a resource of its own that belongs to the other one. Forms combine the two resources on one page, and each keeps its own contract. An alter stays for settings stored inside the owner's object and for changing the owner's rules. A first survey of contributed modules found that one rule does not decide every case: data kept in the owner's own row and revision (Metatag, Scheduler) needs its own answer, and Paragraphs' children have a lifecycle their parent owns. See [the open question](../open/index.md#beside).

## Considered and set aside

- **Copying a config object's keys from its schema into a class.** Each key would be written twice. A module keeps config schema as the source, or declares in code and generates the schema ([decision](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/decisions.md#a-config-object-is-described-by-its-resource)).
- **A constraint of the author's own first.** A keyword is read by every client, a constraint with no keyword only by the server. The order is a keyword, then a list the site decides, then code ([decision](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/decisions.md#a-rule-is-a-keyword-first-a-list-second-code-last)).
- **Every Typed Data type.** Types a JSON Schema document cannot state (`binary`, `language`, `any`) are refused, so the schema is exactly as wide as what validation accepts ([decision](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/decisions.md#one-table-of-leaf-types-read-by-the-blueprint-the-emitter-and-the-reader)).
- **Declarations that read services or site state.** A declaration is static, so it takes no values and can be read without building anything; a rule that reads the site is marked as settled at run time ([decision](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/decisions.md#a-resource-or-structure-is-static)).

## Open to improve

- The PHP API for declaring keys. The proof of concept also tries writing a description directly as a schema, and declaring keys as class properties; both are experimental.
- [Who owns a rule that depends on current values](../open/index.md#current-values), [whether another module may change a rule its owner declared](../open/index.md#owner-rules), and [entries a module adds inside a list its owner stores](../open/index.md#entries), such as Pathauto's punctuation.
- Gaps the adopter ports found: a fixed state for one option in a list, a default read from a sibling key, and keys listed from the site costing a class of their own ([core gaps](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/core-gaps.md#what-this-module-is-evidence-for-and-what-it-is-not)).
- Removing another module's keys from a simple config object when it is uninstalled: a simple config object records no dependencies.

## Validation cases

Blocks, conditions and actions (adoption group A), formatters (B), field types (C), workflow types (D), the content type and placed blocks (E), the content type alter in `surface_examples_extras`, and the Honeypot and Pathauto ports. Cases per form are on [How each piece is validated](validation.md#structures).

## Ready when

- [ ] Every block and condition plugin in core reads into a structure from its config schema with no change to the plugin.
- [ ] An alter reaches the form, the Tool API tool and HTTP alike, and a widening is refused.
- [ ] A decision on resources beside, with Metatag and Paragraphs tried.
- [ ] The Typed Data and configuration system maintainers have reviewed the reading and step 3.

## How to help

- Run the config schema reader over a contributed module's schema and report what it cannot read.
- Try the resources beside direction on Metatag or the URL alias, on paper first.
- Collect how contributed modules change another module's rules today, for the owner-rules question.
- Propose a smaller PHP API for declaring keys.
