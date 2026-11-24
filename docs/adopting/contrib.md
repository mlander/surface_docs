# What contrib sees

Nothing is forced on a contributed module. No API is removed or deprecated, stored config does not change, and a module that does nothing keeps working as it does today. The first real cost appears only when another module's form is replaced by a generated one, and it arrives one owner at a time.

## Three rules at every step

- **New pieces sit beside existing APIs.** No step removes or deprecates an API, and existing calls keep their signatures. A minor release may add APIs that keep backward compatibility ([allowed changes](https://www.drupal.org/about/core/policies/core-change-policies/allowed-changes#s-apis)).
- **Stored config does not change.** Adopting needs no update path and leaves a config export as it was.
- **Only the new way in is strict.** `Config::save()`, a config action and a hand-written form behave as they do today. The new checks apply to a write made through an operation.

What is new carries no stability promise until core gives it one, as with any experimental code in core ([stability levels](https://www.drupal.org/about/core/policies/core-change-policies/experimental/policy-and-list)). A module adopts when it chooses. [Release fit](../path/release-fit.md) checks each kind of change against core's published policies.

## At each rung

The rungs are the [adoption ladder](index.md). "Owner" is the module whose data it is; "another module" is a contributed module that reads, writes or extends it.

| Rung the owner is on | The owner sees | Another module sees |
|---|---|---|
| 0. Nothing | No change. Its config schema and field definitions are read as they are. | No change. |
| 1. A resource beside the form | One resource class, and for simple config a storage class naming its config object. Its form, route and config schema stay as they are. | No change. Its `hook_form_alter()` still runs on the hand-written form. It may now also call the operation, or read its served schema. |
| 2. An explicit structure | One structure class where config schema cannot say enough. | No change. |
| 3. The generated form | The route points at the operation's form. | **The first real cost.** The form has a new form id and a different element tree, so a `hook_form_alter()` on it has to move. |
| 4. Old code removed | `buildForm()`, `validateForm()`, `submitForm()` and the duplicate defaults go. | Nothing beyond rung 3. |

## By kind of module

### A module with its own settings

No impact until it adopts. Adopting is two files: the description, and one line on the plugin or a route. The [site information](site-information.md) example adds two classes and leaves core's form, route and schema alone. A block plugin adds one structure class and one attribute ([Placing a block](place-block.md)), or nothing at all if its config schema says enough.

### A module that adds a setting to another module's form

Its `hook_form_alter()` keeps working for as long as that form is written by hand, which may be forever. When the owner reaches rung 3, the generated form has a new form id, built from its route name:

```php
--8<-- "src/Form/SurfaceOperationForm.php:367:372"
```

and its elements sit under one `surface` key, named for the structure's keys rather than for the old form's elements. So a `hook_form_system_performance_settings_alter()` would not run on a generated performance form, and an alter that reached for `$form['caching']['page_cache_maximum_age']` would find `$form['surface']['max_age']` instead.

The alter moves to an alter of the description. The proof of concept has one module, `surface_examples_extras`, that adds the same two review settings to content types both ways. The classic way is a form alter on core's content type form, which keeps working beside the other:

```php
--8<-- "modules/surface_examples_extras/src/Hook/NodeTypeFormHooks.php:68:69"
```

Moved, it is a class that names the resource it adds to:

```php
--8<-- "modules/surface_examples_extras/src/Alter/NodeTypeAlter.php:61:62"
```

Moved, the setting also reaches HTTP and the Tool API tool, which a form alter never does. The proof of concept records what a Tool API tool sees of each version. The tool read from the content type resource advertises the alter's settings and refuses a deadline of forty-five days. Tool Belt's content type tool, on the classic side, does not advertise them, and stores forty-five days without asking the schema that would refuse it ([the comparison](https://git.drupalcode.org/project/surface/-/blob/75a53469/modules/surface_examples_node_type_tool/COMPARISON.md)).

This cost arrives one owner at a time, and only for owners who choose rung 3. Core's policy already allows it. The Render and Form APIs are stable, while render arrays, form arrays included, are not ([frontend backward compatibility](https://www.drupal.org/about/core/policies/core-change-policies/frontend-bc-policy#render-arrays)), and a minor release may change them ([allowed changes](https://www.drupal.org/about/core/policies/core-change-policies/allowed-changes#s-functionality-and-frontend)). The policies do not name form IDs. Core would move its own forms one at a time, never in bulk.

### A module that writes another module's config

A recipe, an install hook or a migration keeps working as it does today. If it later writes through the operation, a value the form would have refused is refused there too, before anything is saved.

### A module that describes other modules' data again

A module that writes its own description of another module's data, for OpenAPI, Tool API tools or ECA, can delete its copies and read the served contract instead. The proof of concept did this to itself: its hand-written `surface:field_add` and `surface:field_update` tools were deleted and replaced by tools read from the field resource's operations, with nothing lost ([Fields and Tool API tools](fields-and-tools.md)). Tool Belt's field tools, which each declare a field's label, help text and required flag in their own attribute, are the kind of copy this makes unnecessary. Nothing makes such a module delete them.

### Field widgets

Not changed. A field widget stays a field widget. The widgets a generated form draws are a separate thing.

## One rule that keeps step 2 safe

A config object that only a form's route guarded stays closed to every other caller until its owner names the permission. Core does not guess it. No Tool API tool or HTTP call for such an object exists until its owner declares an operation and names the permission it asks.

## Open to improve

- **Where an alter's keys are stored.** Third-party settings stay the default place. A key that already lives elsewhere, in the owner's schema or in the extending module's own config object, keeps working there. Simple config has no third-party settings place yet; step 3 adds one.
- **Changing an owner's rule.** In the proof of concept another module may add a rule of its own, which runs after the owner's and may only narrow the key further. It cannot loosen, replace or remove the owner's rule. Whether that is enough is to be decided from a survey of how contributed modules change another module's conditional behavior today: `#states` set in `hook_form_alter()`, added or removed validation handlers, config schema alters that change a constraint.
- **Entries inside an owner's list.** A module that adds entries to a list or map the owner stores, as Pathauto does for punctuation, is not covered by a place under its own name.
- **A module's own data beside another's.** Forms that combine resources, with contracts kept separate, is the accepted direction and is not yet in the proof of concept.

These are on [Open questions](../open/index.md).
