# Example 1: Site information

Site information is a basic settings form: one config object, edited by one form behind one permission. Simple config like this has a schema and nothing else: no named actions, no access of its own, no validation on write. Rung 1 gives it a resource beside its existing form. This example plays core converting its own settings, so the resource declares every key in Portable Schema. The form keeps working as it is.

## Today

Core's site information form edits six keys of `system.site`: the site name, the slogan, the email address, the front page and the two error pages. Its route asks "administer site configuration", and only that route asks it. A Drush command, a config action, a recipe or a Tool API tool that writes `system.site` asks no permission and runs no checks unless its author wrote them.

The form's rules live in its PHP: titles and descriptions, which fields are required, the slogan's length, and in `validateForm()` the check that each page is a path of this site. Config schema types the three pages as plain strings and marks nothing required.

## The change

In core, two classes would sit beside the files the system module has today:

| File in `core/modules/system` | What it holds | With the change |
|---|---|---|
| `src/Form/SiteInformationForm.php` | The form: labels, required fields, checks | Unchanged |
| `system.routing.yml` | The form's route and its permission | Unchanged until [rung 3](#generated-form) |
| `config/schema/system.schema.yml` | The keys' types | Unchanged |
| `config/install/system.site.yml` | The install values | Unchanged |
| `src/Resource/SiteInformationResource.php` | The keys, the operations and their permission | Added |
| `src/Storage/SiteInformationStorage.php` | Where each key is stored | Added |

In the proof of concept the two classes live in the example module `surface_examples_site`.

!!! question "TBD"
    The directory and class names are the proof of concept's; core's are open.

The resource names the config object, the operation and its permission, which already exists:

```php
--8<-- "modules/surface_examples_site/src/Resource/SiteInformationResource.php:40:49"
```

Each key is declared once, with what core's form gives it. The first four:

```php
--8<-- "modules/surface_examples_site/src/Resource/SiteInformationResource.php:67:94"
```

The storage class names the config object and where the three pages are kept in it:

```php
--8<-- "modules/surface_examples_site/src/Storage/SiteInformationStorage.php:17:33"
```

Each declared key is held to core's config schema at its path when the resource is built, so it can only narrow what the schema allows. Core's `label` type refuses control characters, so the name and the slogan state that check too. The check that each page is a path of this site the account can open is core's own `ValidPath` constraint, the one path aliases use.

What is added:

| File | Code lines |
|---|---:|
| The resource | 78 |
| The storage | 12 |
| **Total** | **90** |
| Optional, at rung 3: the route points at the generated form ([below](#generated-form)) | 3 |

!!! note "Removed: nothing"
    Core's form, its route and its config schema are not touched. Code lines leave out blank lines and comments.

## What it gets

Two operations. The resource declares `configure`, and a `read` is added beside it that returns the stored values and asks the same permission, so an account that may not change the settings may not read them either. Each runs the same way at every way in:

| What | Where |
|---|---|
| Tool API tool | `surface:system.site:configure` and `surface:system.site:read` |
| Drush | `drush surface:run system.site configure` |
| HTTP | `PATCH /surface-api/system.site` and `GET /surface-api/system.site` (TBD) |
| OpenAPI | Both endpoints, with the schema of what `configure` accepts, in `/surface-api/openapi.json` (TBD) |
| Generated form | `/admin/config/system/site-information`, once its route points at the generated form ([below](#generated-form)) |

!!! question "TBD"
    HTTP and OpenAPI are assumed. Where they live, in core or in a module, is [open](../open/later.md), and the paths shown are the proof of concept's.

A write through any of them asks "administer site configuration", runs the same checks, and keeps the keys the resource does not declare as they were. An address that is not an email address is refused at `/mail`, and nothing is written.

Until its route is swapped, core's form at `/admin/config/system/site-information` saves through `Config::save()` as it does today, and does not run the operation's checks.

## Swapping in the generated form {#generated-form}

Rung 3 points the form's route at the operation. The form is then built from the resource on each request: the declared titles, descriptions, defaults and groups, saved through the operation's checks. On core's own route, one line changes and two are added:

```diff
 system.site_information_settings:
   path: '/admin/config/system/site-information'
   defaults:
-    _form: '\Drupal\system\Form\SiteInformationForm'
+    _form: '\Drupal\surface\Form\SurfaceOperationForm'
+    _surface_resource: 'Drupal\surface_examples_site\Resource\SiteInformationResource'
+    _surface_operation: 'configure'
     _title: 'Basic site settings'
   requirements:
     _permission: 'administer site configuration'
```

The proof of concept puts the same defaults on a second route, `/admin/config/system/surface-site-information`, so core's form stays as it is. With the route swapped, `SiteInformationForm` can be deleted at rung 4.

!!! question "TBD"
    The form class and route key names are the proof of concept's; core's are open.

## Before the owner converts {#declaring-a-key}

Core would convert its own settings as above. Until it does, another module can still put a resource over a core config object, for example to offer it as Tool API tools. That module reads the keys from core's config schema, so it gets core's types, labels and checks without copying them. It is a bridge: once core declares the keys, the module uses core's resource instead.

The performance example is such a module, over `system.performance`. It reads the two aggregation keys. Config schema allows any integer for the page cache's maximum age, so it declares that one key with the periods core's form offers. A declared key is held to config schema at its path, so it can only narrow what core allows:

```php
--8<-- "modules/surface_examples_performance/src/Resource/PerformanceResource.php:70:80"
```

## Try it

```bash
--8<-- "modules/surface_examples_site/README.md:17:17"
```

A dry run through the Tool API tool:

```bash
--8<-- "modules/surface_examples_site/README.md:28:28"
```
