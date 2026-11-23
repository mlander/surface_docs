# Site information

Simple config has a schema and nothing else: no named actions, no access of its own, no validation on write. Rung 1 gives a config object a resource beside its existing form. The resource names the operation, the keys that operation takes, and the permission it asks, which is the one the form's route asks today. The form keeps working as it is.

!!! warning "Not yet in the proof of concept: a `system.site` resource"
    The proof of concept has no resource for `system.site`. The closest example it has is core's performance settings, `system.performance`, which takes the same step on a config object core owns. The code on this page is that example. The `system.site` facts below are verified against core 11.4, and what a `system.site` resource would declare is described in words, not shown as code.

## Today

### `system.site`

In Drupal core 11.4, `system.site` stores 11 keys: `uuid`, `name`, `mail`, `slogan`, `page.403`, `page.404`, `page.front`, `admin_compact_mode`, `weight_select_max`, `default_langcode` and `mail_notification`. The site information form edits 6 of them: the name, the slogan, the email address, and the three pages. The notification address is edited on the account settings page, under a different permission ("administer account settings"). The default language follows the languages page. No form edits the UUID.

The site information form's route asks "administer site configuration". Only that route reads the permission. A Drush command, a config action, a recipe or a Tool API tool that writes `system.site` asks nothing and checks nothing unless its author wrote the check.

What is entered is not always what is stored. The email field shows PHP's `sendmail_from` when the stored value is empty, through a `fromConfig` callback on the form's config target. Config schema cannot say that. An operation can, because its input is its own.

### `system.performance`

Core's config schema for `system.performance` describes 11 keys, two of them deprecated (`css.gzip`, `js.gzip`). The installed object stores 9. The performance form edits 3: the page cache's maximum age and whether CSS and JavaScript are aggregated. The maximum age is described in 3 places:[^places]

- the config schema, which says it is an integer labeled "Max age";
- the installed default, 0;
- `PerformanceForm::buildForm()`, which gives it a title, a description and a list of 14 periods.

The title, the description and the list live in the form's PHP, where nothing else can read them. The schema allows any integer.

## The change

Two classes in the module that owns the config object. In core they would sit in the system module. The resource names the operation and its permission, `administer site configuration`, which already exists:

```php
--8<-- "modules/surface_examples_performance/src/Resource/PerformanceResource.php:29:39"
```

It declares the three keys the operation takes, with the title, description and list of periods core's form gives them:

```php
--8<-- "modules/surface_examples_performance/src/Resource/PerformanceResource.php:53:82"
```

The storage class names the config object and says where each key is kept in it:

```php
--8<-- "modules/surface_examples_performance/src/Storage/PerformanceResourceStorage.php:26:40"
```

Most of the storage class is one thing core's form does after it saves: delete the aggregated CSS and JavaScript files, so that this happens whichever way the write came in.

```php
--8<-- "modules/surface_examples_performance/src/Storage/PerformanceResourceStorage.php:78:82"
```

A storage class with nothing to do after the write is the config object's name and no more:

```php
--8<-- "modules/surface_examples_first/src/Storage/NewsletterStorage.php:12:19"
```

What is added:

| File | Lines | Code lines |
|---|---:|---:|
| `src/Resource/PerformanceResource.php` | 84 | 54 |
| `src/Storage/PerformanceResourceStorage.php` | 84 | 37 |
| **2 files** | **168** | **91** |
| Optional: `surface_examples_performance.routing.yml`, a generated form at a second path | 9 | 9 |

"Code lines" leaves out blank lines and comment lines. The example module's `.info.yml` (9 lines) and README are not counted. **Removed: nothing.** The route is optional: the Tool API tool and the HTTP call need none.

The resource is held to core's config schema as core wrote it. When it is built, the storage compares each key with the schema at its path and refuses a resource that would accept a value the schema refuses ([A schema the module did not generate](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/storage.md#a-schema-the-module-did-not-generate)). A list of 14 integers is narrower than "any integer", so it passes. Where a module owns its config object, a structure can instead generate the config schema (`drush surface:config-schema`), and a test fails when the two drift ([A schema generated from the resource](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/storage.md#a-schema-generated-from-the-resource)).

### For `system.site`, in words

Not yet in the proof of concept. The same two classes would declare one operation, "update the site information", taking the six keys the form edits, stored at their paths (`page.front` and the two error pages), asking "administer site configuration". The email key's fallback to `sendmail_from` would go where the proof of concept translates between what an operation asks for and what is stored ([storage](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/storage.md#a-key-stored-otherwise-than-it-is-asked-for)); no example does that for a value read from PHP's settings yet. The notification address would be a second operation with its own permission, or left to the account settings resource. The UUID would be in no operation. The front page check, a path that exists and that the current user may visit, is a rule that depends on the site, which is rung 2.

## What it gets

One operation, three ways to run it, one validation:

| Way in | Where |
|---|---|
| Tool API tool | `surface:system.performance:configure`, and a read tool |
| HTTP | `PATCH /surface-api/system.performance`, listed in the OpenAPI document |
| Generated form | `/admin/config/development/surface-performance`, if the optional route is added |

A maximum age of 120, which is not one of the 14 periods, is refused at `/max_age` with the code `enum`, and nothing is written. A null is refused too: core's schema does not mark `system.performance` fully validatable, so by core's rule any key may hold nothing, and the resource marks the three keys required. The Tool API tool and the OpenAPI document both carry the 14 periods with core's labels, and the generated form draws the same select, title, description and groups as core's form.

A write sets each declared key at its path and keeps `css.compress`, `js.compress` and `fast_404` byte for byte ([decision](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/decisions.md#a-resource-may-hold-some-keys-of-a-config-object-it-does-not-own)).

The test is `PerformanceSurfaceTest`. It runs the refusals through the Tool API tool. Over HTTP it checks only that the OpenAPI document describes the path and the list; a refusal over HTTP is not yet tested for this resource.

### The hand-written form keeps working

Core's performance form at `/admin/config/development/performance` is not touched. It saves through `Config::save()` as it does today, and it does not run the operation's checks. Only the new way in is strict: `Config::save()`, a config action and a hand-written form behave as they do today. A form that asks the operation without being generated is step 2's core change, and not yet in the proof of concept.

## Later, if ever

- **Rung 2.** This example already declares its keys, because the list of periods and the form's words are not in config schema. For `system.site`, rung 2 is where the front page rule would go.
- **Rung 3.** Core's route would point at the operation's form. The generated form already matches core's form: the test checks the three elements' types, titles, description and options, and both groups. Whether that is worth a new form id for every module that alters the performance form is the owner's call ([What contrib sees](contrib.md)).
- **Rung 4.** `PerformanceForm` would go. Not proposed here.

## Another module's view

**Before.** A module that adds a setting to the performance page alters the form with `hook_form_alter()` and stores the value in a config object of its own. The setting is in no description of the page it appears on.

**After.** Step 3 of the core path gives simple config the third-party settings place config entities have. A module's keys would then be stored with the object they configure, under `third_party_settings.<module>`, and checked by its schema. The proof of concept does this for config objects its examples own ([Keys another module mounts](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/storage.md#keys-another-module-mounts)). Not yet in the proof of concept: the same on a core config object such as `system.performance`, whose schema has no such place today.

## What stays as it is

- Stored config. A write through the operation changes the keys it sends and nothing else. No update path, and a config export is unchanged.
- Core's config schema for the object.
- Core's form, its route and its permission. The permissions list does not grow: the operation names the permission the route already asks.

## Open to improve

- **Keys written once.** The resource lists its keys again, held to the schema. Step 2 proposes reading them from the config object's schema; see [Adopting it](index.md#open-to-improve).
- **A config object only a route guarded.** One rule keeps step 2 safe: it stays closed to every other caller until its owner names the permission. Core does not guess it. In the proof of concept a config object has no way in until a resource names an operation and its permission, and an operation whose access check gives no answer is refused ([decision](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/decisions.md#neutral-is-a-refusal-for-an-operations-caller)).
- **A `system.site` example.** It would show two operations on one object under two permissions, a key whose shown value differs from its stored one, and a rule that depends on the site.

## Try it

```bash
--8<-- "modules/surface_examples_performance/README.md:16:16"
```

A dry run through the Tool API tool:

```bash
--8<-- "modules/surface_examples_performance/README.md:27:27"
```

[^places]: Counted in Drupal core 11.4, `core/modules/system`. A place counts when it states the type, the label, the default, the allowed values or a rule. Code that only reads the value does not count.
