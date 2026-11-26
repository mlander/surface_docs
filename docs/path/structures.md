---
topic: structure
---

# Structures

A structure describes a thing's data: each key, its type, its allowed values and its rules, with what a caller needs to send a valid value. A form, validation and a Tool API tool all read the same structure, so they accept and refuse the same values.

## How a structure is made

A module declares in Portable Schema the keys it owns. Until it does, a structure is read from the definitions core already builds: config schema, and field definitions for fields. Reading needs no new system, only the facts of [step 1](groundwork.md).

### Declared in Portable Schema {#declared-in-code}

This is how a module converts its own settings, and how core's common settings forms would be converted ahead of time. Each key carries its title, description, default and checks, written with a builder that produces JSON Schema. The newsletter settings of the first example:

```php
--8<-- "modules/surface_examples_first/src/Resource/NewsletterResource.php:37:63"
```

A declared key is checked against the config schema at its path, so it can only narrow what config schema allows, and config schema keeps being read and written as today. Portable Schema is meant to eventually succeed Typed Data and config schema as the way data is described. That is a long way off.

### Read from config schema

This is the bridge for config another module owns and has not converted, and for plugins and config with no resource class. A mapping becomes a group of keys, a sequence becomes a list, and a type chosen by a sibling key (`[%parent.plugin]`) becomes keys that depend on that sibling. The module writes nothing and changes nothing: a block plugin that has only config schema can already be placed this way.

### Read from field definitions

An entity type already has identity, storage, operations and access, so each bundle's resource is derived from its field definitions, one structure per field. A field's structure is always read, because fields are set up on each site.

## What a structure can say

### Keys that depend on another key {#variants}

A rule can depend on another key's value. "Without a license, at most 100" is a condition from a closed list and an effect that only narrows, written as JSON Schema `if`/`then`. A list can narrow by a sibling, such as a store's regions by its country, and a group of keys can be chosen by a sibling, as a block's settings are chosen by its plugin id.

### Choices

A list of allowed values carries its labels, so the list that validates is the list the form offers and the schema states. Where the site decides the list, such as languages or content types, a class lists it for the site. These lists answer core's `OptionsProviderInterface`, so code that already reads that interface works unchanged.

### Secrets

A key whose stored value is never read back, such as an API key, is marked with JSON Schema's `writeOnly`:

```php
--8<-- "modules/surface_examples/src/Resource/WebhookResource.php:39:42"
```

The form draws a password field that keeps the stored value when left empty, the Tool API tool marks the key write only, and no read returns it.

## Other modules

### Another module

A module adds its own keys to another module's structure in an alter class. It may narrow the owner's rules, never widen them. Its keys are stored under `third_party_settings.<module>`, so the owner's storage and schema never need to know them. Config entities already have this place; [step 3](https://git.drupalcode.org/project/surface/-/blob/3f708be7/docs/core-gaps.md#step-3-third-party-settings-for-simple-config) gives it to simple config.

A module that adds a license to an event registration, limits capacity to 100 without one, and rewords one label:

```php
--8<-- "modules/surface_examples_compliance/src/Alter/RegistrationComplianceAlter.php:34:35"

  // The translation trait, the State key and the constructor are left out.

--8<-- "modules/surface_examples_compliance/src/Alter/RegistrationComplianceAlter.php:56:72"
}
```

The owning class is unchanged and does not know the module exists. Today a form alter changes one form and nothing else that takes the same values, and `hook_config_schema_info_alter()` can loosen any module's rule with no record of who did. Here one alter reaches the form and the Tool API tool, and every narrowing is checked.

### Beside

Data with its own id, storage or permission, such as meta tags, a URL alias or Paragraphs' children, does not fit inside another module's structure: adding its keys there would change the owner's contract for every caller. The direction instead: the module declares a resource of its own that belongs to the other one, and a form combines both resources on one page, each with its own contract. This is not built yet ([open question](../open/index.md#beside)).
