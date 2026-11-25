# What contrib sees

Nothing changes for a contributed module until it, or the module whose data it uses, chooses to adopt. No API is removed or deprecated, stored config does not change, and form alters keep working on every hand-written form.

Only the new way in is strict. `Config::save()`, a config action and a hand-written form behave as they do today. A config object gets no new way in until its owner declares an operation and names the permission it asks.

## At each rung

"Owner" is the module whose data it is. "Another module" reads, writes or extends it.

| Owner's rung | The owner | Another module |
|---|---|---|
| 0. Nothing | No change. | No change. |
| 1. A resource beside the form | Adds a resource class. Its form, route and config schema stay. | No change. Its `hook_form_alter()` still runs. It may also call the operation. |
| 2. An explicit structure | Declares a plugin's settings in Portable Schema. | No change. |
| 3. The generated form | Points its route at the operation's form. | The form has a new form id and element tree, so a `hook_form_alter()` on it has to move. |
| 4. Old code removed | Deletes the form's build, validate and submit methods. | Nothing beyond rung 3. |

## When a form alter has to move

Rung 3 is optional, and its cost arrives one owner at a time. Core's policy allows form arrays to change in a minor release ([frontend backward compatibility](https://www.drupal.org/about/core/policies/core-change-policies/frontend-bc-policy#render-arrays)), and core would move its own forms one at a time.

The generated form's id comes from its route name:

```php
--8<-- "src/Form/SurfaceOperationForm.php:367:372"
```

The alter moves to an alter of the structure. The proof of concept adds the same two settings to content types both ways. The form alter, which keeps working:

```php
--8<-- "modules/surface_examples_extras/src/Hook/NodeTypeFormHooks.php:68:69"
```

Moved, it is a class that names the resource it adds to:

```php
--8<-- "modules/surface_examples_extras/src/Alter/NodeTypeAlter.php:61:62"
```

Moved, the setting also reaches the Tool API tool, which a form alter never does.

## A module that copies another module's definitions

A module that writes its own copy of another module's data definitions, for Tool API tools or ECA, can read the operation's contract instead and delete the copy ([Fields and Tool API tools](fields-and-tools.md)). Nothing makes it do so.
