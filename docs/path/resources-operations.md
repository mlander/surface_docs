---
topic: resource
---

# Resources and operations

A resource is a thing with identity and storage: a config object, a placed block, a content type, a node. An operation is a named action on it, with its input, a permission and its checks. A form, a Tool API tool, an HTTP call and Drush are each one way to run an operation, and all of them run the same checks.

Entity types already have most of this: operations, access per field, validation on write. A simple config object has none of it. Its form class holds the checks and its route holds the permission, so a Drush command, a config action or an agent that writes the same settings asks no permission and runs no validation unless its author wrote them. Step 2 gives a config object named operations, each with a permission, and validates a write through one against its config schema before it saves.

## Operations

A resource sits beside the forms a module already has. Each form is one operation, and the forms keep working at their own routes. Two shapes cover most of core.

**A collection** holds many things, each with an id, such as placed blocks. Its operations are the standard ones: create, update and delete, and a read of the current values.

| Core's form today | Operation | Tool API tool | HTTP, in the proof of concept |
|---|---|---|---|
| `/admin/structure/block/add/{plugin_id}/{theme}` | create | `surface:block.placement:create` | `POST /surface-api/block.placement` |
| `/admin/structure/block/manage/{block}` | update | `surface:block.placement:update` | `PATCH /surface-api/block.placement/{id}` |
| `/admin/structure/block/manage/{block}/delete` | delete | `surface:block.placement:delete` | `DELETE /surface-api/block.placement/{id}` |
| | read | `surface:block.placement:read` | `GET /surface-api/block.placement/{id}` |

**A singleton** is one thing with no id, such as a config object. It has a read and one update, named `configure`.

| Core's form today | Operation | Tool API tool | HTTP, in the proof of concept |
|---|---|---|---|
| `/admin/config/system/site-information` | configure | `surface:system.site:configure` | `PATCH /surface-api/system.site` |
| | read | `surface:system.site:read` | `GET /surface-api/system.site` |

Any operation also runs from the command line. The proof of concept adds one Drush command that runs an operation as an account, through the same checks. Without `--values` it only says whether the account may run the operation and which keys it takes:

```bash
drush surface:run system.site configure --uid=1 --values='{"slogan":"Built with Drupal"}' --dry-run
```

Operations are declared on the resource's class with attributes, as plugins and hooks are. The placed block's resource and its create operation:

```php
--8<-- "modules/surface_examples_block/src/Resource/BlockPlacementResource.php:35:48"
```

A singleton's, the newsletter settings of the first example:

```php
--8<-- "modules/surface_examples_first/src/Resource/NewsletterResource.php:18:27"
```

The read is derived from the update. Whether core names a config object's operations on a PHP class, as here, or in its config schema is open.

### Where an operation's keys come from {#keys}

- **Declared by the module that owns the config.** Each key is declared in Portable Schema with its title, description, default and checks ([Structures](structures.md#declared-in-code)). Core's common settings forms would be converted ahead of time. A declared key is checked against the config schema at its path, so it can only narrow what config schema allows.
- **Read where the owner has not converted.** A resource over another module's config names the keys it takes, and each key's type, label and constraints are read from that module's config schema. Declaring them would copy rules the resource does not own. This is the bridge until the owner converts, and config schema is not changed.

## Access

An operation names a permission that already exists, usually the one the form's route asks today. None are created. Beyond the permission, an access class may answer per key: open, locked (shown but fixed), or left out, as field access does per field. A resource over another module's things asks that module's access each time, so node grants and workflow modules still apply.

## Validation

A write through an operation validates the whole config object, the new values over the stored ones, against its config schema before anything is saved. Only the new way in is strict: `Config::save()`, a config action and a hand-written form behave as they do today.

## Storage

Storage stays where it is: a config object, a config entity saved through its own `save()`, a plugin's configuration, a content entity. Adopting needs no update path and leaves a config export as it was.

## Forms

Generated forms are step 5 and optional. A hand-written form can keep running the operation, and a module replaces it with a generated one at its own pace, or never. Automatic form generation will scale from small simple forms to complex, dynamic use cases, and form alters stay available for cosmetic changes. Because a form is drawn from the [Portable Schema](portable-schema.md) document, a headless client or a React app can draw the same form.

## Widgets

Field widgets are not changed. A generated form chooses its own elements from each key's schema. Whether the two grow toward one shared contract is a [question for another day](../open/later.md).
