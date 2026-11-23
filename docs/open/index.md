# Open questions

The steps need these answered. Each is open to proposals; follow [Proposing a change](proposing-a-change.md) where a question touches something already decided.

## The schema language {#schema-language}

Most of what is missing can be said with plain JSON Schema keywords core's output does not use yet. A small set needs agreed extension keywords: a rule only the server can check, a value chosen by another key, hints for drawing a form. [Portable Schema](../path/portable-schema.md) by fago fixes that set, with validators in PHP and JavaScript that give the same answers. Core validates component props with a different library. Which dialect core adopts, and how its validators relate, is open.

## Where the parts land {#where-the-parts-land}

Which parts go into an existing core subsystem directly, which start as an experimental module, and under which names. What is new should stay small, and core's existing APIs should read from it.

## Rules that depend on current values {#current-values}

Who owns a rule that depends on what is stored now, such as a choice list that narrows when another key changes.

## A module's own data beside another's {#beside}

How a module adds its own data to another module's thing without changing that thing's endpoints. The direction being explored: a form may combine resources, each keeps its own contract, and a declared relation says which belongs to which. See [Structures](../path/structures.md#beside).

## Changing a rule the owner declared {#owner-rules}

In the proof of concept, another module may add a rule of its own that only narrows a key further. It cannot loosen, replace or remove the owner's rule. Whether that is enough is to be decided from a survey of how contributed modules change other modules' behavior today: `#states` set in `hook_form_alter()`, validation handlers added or removed, config schema alters that change a constraint.

## Entries inside a list the owner stores {#entries}

A module that adds entries to a list or map the owner itself stores, as Pathauto does for punctuation. The entries belong inside the owner's key, so a place under the extender's own name does not cover it.

## Recording who ran what {#observability}

Every way in runs an operation through one place, so there is one place to record who ran what, through which way in, and what was refused. What that place records itself, and what it leaves to logging and to other modules, is not settled.
