# Site information

Simple config has a schema and nothing else: no named actions, no access of its own, no validation on write. Rung 1 gives a config object a resource beside its existing form. The resource names the operation, the keys that operation takes, and the permission it asks, which is the one the form's route asks today. The form keeps working as it is.

!!! note "Code written for this page"
    The `system.site` code below is written for this page in the proof of concept's API. It is not in the module and has not been run. The same step on core's performance settings, `system.performance`, is in the module and tested; it is shown [further down](#tested-in-the-proof-of-concept-systemperformance).

## Today

In Drupal core 11.4, `system.site` stores 11 keys: `uuid`, `name`, `mail`, `slogan`, `page.403`, `page.404`, `page.front`, `admin_compact_mode`, `weight_select_max`, `default_langcode` and `mail_notification`. The site information form edits 6 of them: the name, the slogan, the email address, and the three pages. The notification address is edited on the account settings page, under a different permission ("administer account settings"). The default language follows the languages page. No form edits the UUID.

The site information form's route asks "administer site configuration". Only that route reads the permission. A Drush command, a config action, a recipe or a Tool API tool that writes `system.site` asks nothing and checks nothing unless its author wrote the check.

What is entered is not always what is stored. The email field shows PHP's `sendmail_from` when the stored value is empty, through a `fromConfig` callback on the form's config target. Config schema cannot say that. An operation can, because its input is its own.

## The change

Two classes in the module that owns the config object. In core they would sit in the system module. The resource names the operation and its permission, `administer site configuration`, which already exists, and declares the six keys the form edits, with the form's titles, descriptions and groups:

```php
#[Resource('system.site',
  label: new TranslatableMarkup('Site information'),
  storage: SiteInformationStorage::class,
)]
#[Operation('configure',
  label: new TranslatableMarkup('Configure site information'),
  description: new TranslatableMarkup('Sets the site name, slogan and email address, and the front page and error pages.'),
  permission: 'administer site configuration',
)]
final class SiteInformationResource implements ResourceInterface {

  public static function defineInputs(BlueprintInterface $inputs): void {
    $details = ArrangementGroup::details('site_information', t('Site details'));
    $front = ArrangementGroup::details('front_page', t('Front page'));
    $errors = ArrangementGroup::details('error_page', t('Error pages'));

    $inputs->add('name', Schema::string()
      ->title(t('Site name'))
      ->required());
    $inputs->describe('name', group: $details);

    $inputs->add('slogan', Schema::string()
      ->title(t('Slogan'))
      ->description(t("How this is used depends on your site's theme.")));
    $inputs->describe('slogan', group: $details);

    $inputs->add('mail', Schema::string()
      ->title(t('Email address'))
      ->description(t('The <em>From</em> address in automated emails sent during registration and new password requests, and other notifications.'))
      ->format('email')
      ->required());
    $inputs->describe('mail', group: $details);

    $inputs->add('front_page', Schema::string()
      ->title(t('Default front page'))
      ->description(t('Specify a relative URL to display as the front page.'))
      ->pattern('^/')
      ->required());
    $inputs->describe('front_page', group: $front);

    $inputs->add('page_403', Schema::string()
      ->title(t('Default 403 (access denied) page'))
      ->description(t('This page is displayed when the requested document is denied to the current user. Leave blank to display a generic "access denied" page.'))
      ->pattern('^(/.*)?$'));
    $inputs->describe('page_403', group: $errors);

    $inputs->add('page_404', Schema::string()
      ->title(t('Default 404 (not found) page'))
      ->description(t('This page is displayed when no other content matches the requested document. Leave blank to display a generic "page not found" page.'))
      ->pattern('^(/.*)?$'));
    $inputs->describe('page_404', group: $errors);
  }

}
```

The storage class names the config object and says where each key is kept in it. The five keys it does not list are kept as they are on every write:

```php
final class SiteInformationStorage extends ConfigObjectResourceStorage {

  public const CONFIG = 'system.site';

  public const STORED_AT = [
    'name' => 'name',
    'slogan' => 'slogan',
    'mail' => 'mail',
    'front_page' => 'page.front',
    'page_403' => 'page.403',
    'page_404' => 'page.404',
  ];

}
```

What is added, written the same way as the tested example:

| File | Code lines, about |
|---|---:|
| `src/Resource/SiteInformationResource.php` | 65 |
| `src/Storage/SiteInformationStorage.php` | 15 |

**Removed: nothing.** Core's form, its route and its config schema are not touched.

The resource is held to core's config schema for `system.site` as core wrote it. When it is built, the storage compares each key with the schema at its path and refuses a resource that would accept a value the schema refuses ([A schema the module did not generate](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/storage.md#a-schema-the-module-did-not-generate)).

Under step 2 as proposed, the resource would not declare these six keys. Its operation would name them and read each from core's config schema, and only a key config schema cannot describe would be declared ([Where an operation's keys come from](../path/resources-operations.md#keys)). The code above is what the proof of concept requires today.

### What the code above leaves out

- **The email fallback.** Showing `sendmail_from` when the stored value is empty would go where the proof of concept translates between what an operation asks for and what is stored ([storage](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/storage.md#a-key-stored-otherwise-than-it-is-asked-for)). No example does that for a value read from PHP's settings yet.
- **The notification address.** It belongs to the account settings page and its permission, so it would be a key of an account settings resource on the same config object. A resource may hold some keys of a config object and leave the rest ([decision](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/decisions.md#a-resource-may-hold-some-keys-of-a-config-object-it-does-not-own)).
- **The path rule.** The form checks that each of the three pages starts with a slash, which the `pattern` above says in plain JSON Schema. It also checks that the path exists and that the current user may visit it. That is a rule that depends on the site, which is rung 2.

## What it gets

One operation, three ways to run it, one validation. These are the ways in the tested example below has; for `system.site` they would be:

| Way in | Where |
|---|---|
| Tool API tool | `surface:system.site:configure`, and a read tool |
| HTTP | `PATCH /surface-api/system.site`, listed in the OpenAPI document |
| Generated form | at a second path, only if a route is added |

A Drush command, a recipe or an agent that writes the site name through the operation asks "administer site configuration" and is checked against the same rules as the form. An email address that is not one, or a front page without a leading slash, is refused at its key, and nothing is written. A write sets the six keys at their paths and keeps the other five byte for byte.

### The hand-written form keeps working

Core's site information form at `/admin/config/system/site-information` is not touched. It saves through `Config::save()` as it does today, and it does not run the operation's checks. Only the new way in is strict: `Config::save()`, a config action and a hand-written form behave as they do today. A form that asks the operation without being generated is step 2's core change, and not yet in the proof of concept.


## Tested in the proof of concept: `system.performance` {#tested-in-the-proof-of-concept-systemperformance}

The same step on core's performance settings is in the module, with a test.

Core's config schema for `system.performance` describes 11 keys, two of them deprecated (`css.gzip`, `js.gzip`). The installed object stores 9. The performance form edits 3: the page cache's maximum age and whether CSS and JavaScript are aggregated. The maximum age is described in 3 places:[^places]

- the config schema, which says it is an integer labeled "Max age";
- the installed default, 0;
- `PerformanceForm::buildForm()`, which gives it a title, a description and a list of 14 periods.

The title, the description and the list live in the form's PHP, where nothing else can read them. The schema allows any integer.

The resource names the operation and its permission:

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

What is added:

| File | Lines | Code lines |
|---|---:|---:|
| `src/Resource/PerformanceResource.php` | 84 | 54 |
| `src/Storage/PerformanceResourceStorage.php` | 84 | 37 |
| **2 files** | **168** | **91** |
| Optional: `surface_examples_performance.routing.yml`, a generated form at a second path | 9 | 9 |

"Code lines" leaves out blank lines and comment lines. The example module's `.info.yml` (9 lines) and README are not counted. **Removed: nothing.** The route is optional: the Tool API tool and the HTTP call need none.

| Way in | Where |
|---|---|
| Tool API tool | `surface:system.performance:configure`, and a read tool |
| HTTP | `PATCH /surface-api/system.performance`, listed in the OpenAPI document |
| Generated form | `/admin/config/development/surface-performance`, if the optional route is added |

A maximum age of 120, which is not one of the 14 periods, is refused at `/max_age` with the code `enum`, and nothing is written. A null is refused too: core's schema does not mark `system.performance` fully validatable, so by core's rule any key may hold nothing, and the resource marks the three keys required. The Tool API tool and the OpenAPI document both carry the 14 periods with core's labels, and the generated form draws the same select, title, description and groups as core's form.

A write sets each declared key at its path and keeps `css.compress`, `js.compress` and `fast_404` byte for byte ([decision](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/decisions.md#a-resource-may-hold-some-keys-of-a-config-object-it-does-not-own)).

The test is `PerformanceSurfaceTest`. It runs the refusals through the Tool API tool. Over HTTP it checks only that the OpenAPI document describes the path and the list; a refusal over HTTP is not yet tested for this resource.

A list of 14 integers is narrower than the schema's "any integer", so the resource passes the check against core's config schema. Where a module owns its config object, a structure can instead generate the config schema (`drush surface:config-schema`), and a test fails when the two drift ([A schema generated from the resource](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/storage.md#a-schema-generated-from-the-resource)).

## Later, if ever

- **Rung 2.** For `system.site`, rung 2 is where the rule that a page exists and may be visited would go. The performance example is already at rung 2 for its list of periods, which config schema cannot hold.
- **Rung 3.** Core's route would point at the operation's form. For the performance example the generated form already matches core's form: the test checks the three elements' types, titles, description and options, and both groups. Whether that is worth a new form id for every module that alters the performance form is the owner's call ([What contrib sees](contrib.md)).
- **Rung 4.** `SiteInformationForm` or `PerformanceForm` would go. Not proposed here.

## Another module's view

**Before.** A module that adds a setting to the site information page alters the form with `hook_form_alter()` and stores the value in a config object of its own. The setting is in no description of the page it appears on.

**After.** Step 3 of the core path gives simple config the third-party settings place config entities have. A module's keys would then be stored with the object they configure, under `third_party_settings.<module>`, and checked by its schema. The proof of concept does this for config objects its examples own ([Keys another module mounts](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/storage.md#keys-another-module-mounts)). Not yet in the proof of concept: the same on a core config object such as `system.site`, whose schema has no such place today.

## What stays as it is

- Stored config. A write through the operation changes the keys it sends and nothing else. No update path, and a config export is unchanged.
- Core's config schema for the object.
- Core's form, its route and its permission. The permissions list does not grow: the operation names the permission the route already asks.

## Open to improve

- **Keys written once.** The code above declares all six keys again, as the proof of concept requires today. Under step 2 as proposed, config schema describes these six well enough to be named and read, and only the form's longer titles would be lost ([Where an operation's keys come from](../path/resources-operations.md#keys)).
- **A config object only a route guarded.** One rule keeps step 2 safe: it stays closed to every other caller until its owner names the permission. Core does not guess it. In the proof of concept a config object has no way in until a resource names an operation and its permission, and an operation whose access check gives no answer is refused ([decision](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/decisions.md#neutral-is-a-refusal-for-an-operations-caller)).
- **The `system.site` code.** It is written for this page and not run. Adding it to the proof of concept with a test would show a key whose shown value differs from its stored one, and a second resource on the same object under another permission.

## Try the tested example

```bash
--8<-- "modules/surface_examples_performance/README.md:16:16"
```

A dry run through the Tool API tool:

```bash
--8<-- "modules/surface_examples_performance/README.md:27:27"
```

[^places]: Counted in Drupal core 11.4, `core/modules/system`. A place counts when it states the type, the label, the default, the allowed values or a rule. Code that only reads the value does not count.
