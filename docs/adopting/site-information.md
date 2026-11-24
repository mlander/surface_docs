# Site information

Simple config has a schema and nothing else: no named actions, no access of its own, no validation on write. Rung 1 gives a config object a resource beside its existing form. The resource names the operation, the keys that operation takes, and the permission it asks, which is the one the form's route asks today. The form keeps working as it is.

## Today

In Drupal core 11.4, `system.site` stores 11 keys: `uuid`, `name`, `mail`, `slogan`, `page.403`, `page.404`, `page.front`, `admin_compact_mode`, `weight_select_max`, `default_langcode` and `mail_notification`. The site information form edits 6 of them: the name, the slogan, the email address, and the three pages. The notification address is edited on the account settings page, under a different permission ("administer account settings"). The default language follows the languages page. No form edits the UUID.

The site information form's route asks "administer site configuration". Only that route reads the permission. A Drush command, a config action, a recipe or a Tool API tool that writes `system.site` asks nothing and checks nothing unless its author wrote the check.

What is entered is not always what is stored. The email field shows PHP's `sendmail_from` when the stored value is empty, through a `fromConfig` callback on the form's config target. Config schema cannot say that. An operation can, because its input is its own.

## The change

Two small classes in the module that owns the config object. In core they would sit in the system module. The resource names the operation and its permission, `administer site configuration`, which already exists:

```php
--8<-- "modules/surface_examples_site/src/Resource/SiteInformationResource.php:32:41"
```

It names the six keys the form edits and reads each one from core's config schema. The rest of the method only places the keys in the form's three groups:

```php
--8<-- "modules/surface_examples_site/src/Resource/SiteInformationResource.php:47:59"
```

The storage class names the config object and says where the three pages are kept in it. The other three keys are kept at their own names:

```php
--8<-- "modules/surface_examples_site/src/Storage/SiteInformationStorage.php:17:33"
```

What is added:

| File | Lines | Code lines |
|---|---:|---:|
| `src/Resource/SiteInformationResource.php` | 61 | 34 |
| `src/Storage/SiteInformationStorage.php` | 33 | 12 |
| **2 files** | **94** | **46** |
| Optional: `surface_examples_site.routing.yml`, a generated form at a second path | 9 | 9 |

"Code lines" leaves out blank lines and comment lines. The example module's `.info.yml` and README are not counted. **Removed: nothing.** Core's form, its route and its config schema are not touched.

Each key's type, label and checks come from `system.schema.yml`, at the path the storage keeps the key at. Nothing about a key is written twice. A key is either read or declared in code, never both, and either way it is held to the config schema at its path ([Keys read from config schema](https://git.drupalcode.org/project/surface/-/blob/d5486fd4/docs/resources.md#keys-read-from-config-schema)).

### What reading costs

Config schema says less than the form, and a read key has only what config schema says:

- **Labels are the schema's.** Here they match core's form. In `system.performance`, the JavaScript key reads as "JavaScript preprocess", shorter than the form's "Aggregate JavaScript files".
- **No descriptions and no defaults.** Config schema has neither.
- **Nothing is required.** Core's `system.site` is not marked fully validatable, so by core's rule any key may hold nothing. Core's form requires the site name; the schema does not.
- **No checks the schema does not state.** Core's form checks that each page starts with a slash, exists, and may be visited. The schema types the three pages as `path`, a string with no check.
- **Email is checked as the portable format.** Core's `email` type carries an Email constraint, read as `format: email`. That format refuses an internationalized local part that core's own check accepts.

A key that needs more is declared in code instead, as the performance example below declares its maximum age. A declared key is held to the schema at its path, so it can only narrow what the schema allows.

### What the example leaves out

- **The email fallback.** Core's form shows PHP's `sendmail_from` when the stored value is empty. That belongs where the proof of concept translates between what an operation asks for and what is stored ([storage](https://git.drupalcode.org/project/surface/-/blob/d5486fd4/docs/storage.md#a-key-stored-otherwise-than-it-is-asked-for)). No example does that for a value read from PHP's settings yet.
- **The notification address.** It belongs to the account settings page and its permission, so it would be a key of an account settings resource on the same config object. A resource may hold some keys of a config object and leave the rest ([decision](https://git.drupalcode.org/project/surface/-/blob/d5486fd4/docs/decisions.md#a-resource-may-hold-some-keys-of-a-config-object-it-does-not-own)).

## What it gets

One operation, three ways to run it, one validation:

| Way in | Where |
|---|---|
| Tool API tool | `surface:system.site:configure`, and a read tool |
| HTTP | `PATCH /surface-api/system.site`, listed in the OpenAPI document |
| Generated form | `/admin/config/system/surface-site-information`, if the optional route is added |

A Drush command, a recipe or an agent that writes the site name through the operation asks "administer site configuration" and is checked against the same rules as every other way in. An email address that is not one is refused at `/mail` with the code `invalid_format`, through the Tool API tool and with a 422 over HTTP, and nothing is written. A write sets the keys it sends at their paths and keeps `uuid`, `admin_compact_mode`, `weight_select_max`, `default_langcode` and `mail_notification` as they were.

The test is `SiteInformationSurfaceTest`. It checks the six keys against core's schema, the email refusal through the Tool API tool and over HTTP, a write that keeps the keys it does not read, the OpenAPI document, and the generated form's three groups.

### The hand-written form keeps working

Core's site information form at `/admin/config/system/site-information` is not touched. It saves through `Config::save()` as it does today, and it does not run the operation's checks. Only the new way in is strict: `Config::save()`, a config action and a hand-written form behave as they do today. A form that asks the operation without being generated is step 2's core change, and not yet in the proof of concept.

## Declaring a key: `system.performance` {#declaring-a-key}

Core's performance settings show the other half: a key config schema cannot describe well enough is declared in code, beside keys that are read.

Core's config schema for `system.performance` describes 11 keys, two of them deprecated (`css.gzip`, `js.gzip`). The installed object stores 9. The performance form edits 3: the page cache's maximum age and whether CSS and JavaScript are aggregated. The maximum age is described in 3 places:[^places]

- the config schema, which says it is an integer labeled "Max age";
- the installed default, 0;
- `PerformanceForm::buildForm()`, which gives it a title, a description and a list of 14 periods.

The title, the description and the list live in the form's PHP, where nothing else can read them. The schema allows any integer.

The resource names the operation and its permission:

```php
--8<-- "modules/surface_examples_performance/src/Resource/PerformanceResource.php:36:46"
```

It declares the maximum age with the title, description and list of periods core's form gives it, and reads the two aggregation keys from core's schema:

```php
--8<-- "modules/surface_examples_performance/src/Resource/PerformanceResource.php:60:83"
```

The storage class names the config object and says where each key is kept in it:

```php
--8<-- "modules/surface_examples_performance/src/Storage/PerformanceResourceStorage.php:26:40"
```

Most of the storage class is one thing core's form does after it saves: delete the aggregated CSS and JavaScript files, so that this happens whichever way the write came in.

```php
--8<-- "modules/surface_examples_performance/src/Storage/PerformanceResourceStorage.php:78:82"
```

What is added:

| File | Lines | Code lines |
|---|---:|---:|
| `src/Resource/PerformanceResource.php` | 85 | 47 |
| `src/Storage/PerformanceResourceStorage.php` | 84 | 37 |
| **2 files** | **169** | **84** |
| Optional: `surface_examples_performance.routing.yml`, a generated form at a second path | 9 | 9 |

| Way in | Where |
|---|---|
| Tool API tool | `surface:system.performance:configure`, and a read tool |
| HTTP | `PATCH /surface-api/system.performance`, listed in the OpenAPI document |
| Generated form | `/admin/config/development/surface-performance`, if the optional route is added |

A maximum age of 120, which is not one of the 14 periods, is refused at `/max_age` with the code `enum`, and nothing is written. The maximum age is declared required, so a null is refused too. The two read keys are not: core's schema does not mark `system.performance` fully validatable, so a null clears one, as core's rule allows. The Tool API tool and the OpenAPI document both carry the 14 periods with core's labels. The generated form draws the same select, description and groups as core's form, with the JavaScript key under the schema's shorter label.

A write sets each key at its path and keeps `css.compress`, `js.compress` and `fast_404` byte for byte. The test is `PerformanceSurfaceTest`. It runs the refusals through the Tool API tool. Over HTTP it checks only that the OpenAPI document describes the path and the list; a refusal over HTTP is not yet tested for this resource.

A list of 14 integers is narrower than the schema's "any integer", so the declared key passes the check against core's config schema. A module that owns its config object may instead declare every key and generate its config schema from them (`drush surface:config-schema`), with a test that fails when the two drift. A resource with read keys is not generated from, so generating stays a choice the module makes ([A schema generated from the resource](https://git.drupalcode.org/project/surface/-/blob/d5486fd4/docs/storage.md#a-schema-generated-from-the-resource)).

## Later, if ever

- **Rung 2.** For `system.site`, the site name would be declared required, and the rule that a page exists and may be visited would be declared. The performance example is already at rung 2 for its maximum age.
- **Rung 3.** Core's route would point at the operation's form. Whether that is worth a new form id for every module that alters the form is the owner's call ([What contrib sees](contrib.md)).
- **Rung 4.** `SiteInformationForm` or `PerformanceForm` would go. Not proposed here.

## Another module's view

**Before.** A module that adds a setting to the site information page alters the form with `hook_form_alter()` and stores the value in a config object of its own. The setting is in no description of the page it appears on.

**After.** Step 3 of the core path gives simple config the third-party settings place config entities have. A module's keys would then be stored with the object they configure, under `third_party_settings.<module>`, and checked by its schema. The proof of concept does this for config objects its examples own ([Keys another module mounts](https://git.drupalcode.org/project/surface/-/blob/d5486fd4/docs/storage.md#keys-another-module-mounts)). Not yet in the proof of concept: the same on a core config object such as `system.site`, whose schema has no such place today.

## What stays as it is

- Stored config. A write through the operation changes the keys it sends and nothing else. No update path, and a config export is unchanged.
- Core's config schema for the object.
- Core's form, its route and its permission. The permissions list does not grow: the operation names the permission the route already asks.

## Open to improve

- **Labels and descriptions for read keys.** A read key shows config schema's short label and no description until the module declares it. Whether a key can be read and given a label of its own, without being declared, is open.
- **Email checked more strictly than core.** The portable `format: email` refuses addresses core's Email constraint accepts.
- **A config object only a route guarded.** One rule keeps step 2 safe: it stays closed to every other caller until its owner names the permission. Core does not guess it. In the proof of concept a config object has no way in until a resource names an operation and its permission, and an operation whose access check gives no answer is refused ([decision](https://git.drupalcode.org/project/surface/-/blob/d5486fd4/docs/decisions.md#neutral-is-a-refusal-for-an-operations-caller)).

## Try it

```bash
--8<-- "modules/surface_examples_site/README.md:32:32"
```

A dry run through the Tool API tool:

```bash
--8<-- "modules/surface_examples_site/README.md:43:43"
```

[^places]: Counted in Drupal core 11.4, `core/modules/system`. A place counts when it states the type, the label, the default, the allowed values or a rule. Code that only reads the value does not count.
