# Open questions

The steps need these answered. Each is open to proposals.

## The schema language {#schema-language}

Most of what core's JSON Schema output lacks can be said with plain JSON Schema keywords, and a small set needs agreed extension keywords, such as a rule only the server can check. [Portable Schema](../path/portable-schema.md) fixes that set, with validators in PHP and JavaScript that give the same answers. Which dialect core adopts, and how it relates to the validator core uses for component props, is open. So is its PHP validator's license: it builds on opis/json-schema, which is Apache-2.0, and Portable Schema's README says core would need a GPLv2-compatible base.

## Where the parts land {#where-the-parts-land}

Which parts go into an existing core subsystem directly, which start as an [experimental module](../path/release-fit.md#if-the-new-parts-start-as-an-experimental-module), and under which names. What is new should stay small, and core's existing APIs should read from it.

## Resources for config entity types {#config-entities}

A content entity type's resource can be derived from its field definitions, because a field definition says which values are computed or read only. Config schema has no such marker, so it cannot tell a key code sets from a key a caller sets. Open: whether core attaches a resource class to a config entity type as a handler beside its form and access handlers, and whether [step 1](../path/groundwork.md) adds that marker so the resource can be derived.

## Rules that depend on current values {#current-values}

Some rules depend on what is stored now, such as a choice list that narrows when another key changes. Who owns such a rule, the operation or the data definition, is open.

## A module's own data beside another's {#beside}

How a module adds its own data to another module's thing without changing that thing's operations. The direction explored: a form combines resources, each keeps its own contract, and a declared relation says which belongs to which ([Structures](../path/structures.md#beside)).

## Changing a rule the owner declared {#owner-rules}

Another module may add a rule that narrows a key further, but it cannot loosen, replace or remove the owner's rule. Whether that is enough will be decided from how contributed modules change other modules' forms and validation today.

## Entries inside a list the owner stores {#entries}

Some modules add entries to a list the owner stores, as Pathauto does for punctuation settings. The entries belong inside the owner's key, so a place under the extending module's own name does not cover this case.

## Recording who ran what {#observability}

Every way in runs an operation through one place, so one place can record who ran what, through which way in, and what was refused. What that place records itself, and what it leaves to logging and other modules, is open.
