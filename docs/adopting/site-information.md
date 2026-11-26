# Site information

Simple config has a schema and nothing else: no named actions, no access of its own, no validation on write. Rung 1 gives a config object a resource beside its existing form. This example plays core converting its own settings, so the resource declares every key in Portable Schema. The form keeps working as it is.

## Today

Core's site information form edits six keys of `system.site`: the site name, the slogan, the email address, the front page and the two error pages. Its route asks "administer site configuration", and only that route asks it. A Drush command, a config action, a recipe or a Tool API tool that writes `system.site` asks no permission and runs no checks unless its author wrote them.

The form's rules live in its PHP: titles and descriptions, which fields are required, the slogan's length, and in `validateForm()` the check that each page is a path of this site. Config schema types the three pages as plain strings and marks nothing required.

## The change

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
| Optional: a route for a generated form at a second path | 9 |

Code lines leave out blank lines and comments. **Removed: nothing.** Core's form, its route and its config schema are not touched.

## What it gets

One operation, one validation, at every way in:

| Way in | Where |
|---|---|
| Tool API tool | `surface:system.site:configure`, and a read tool |
| Generated form | `/admin/config/system/surface-site-information`, if the optional route is added |

The proof of concept also serves it as `PATCH /surface-api/system.site`; HTTP is not proposed for core now. A write through any of them asks "administer site configuration", runs the same checks, and keeps the keys the resource does not declare as they were. An address that is not an email address is refused at `/mail`, and nothing is written.

Core's form at `/admin/config/system/site-information` saves through `Config::save()` as it does today, and does not run the operation's checks.

Two known gaps: the email format refuses internationalized addresses that core's Email constraint accepts, and a name of only spaces is accepted where core's form trims it first.

## Reading keys you do not own {#declaring-a-key}

A module that does not own a config object reads its keys from config schema instead of copying the owner's rules. The performance example plays a module outside core over `system.performance`. It reads the two aggregation keys and declares only the page cache's maximum age, with the periods core's form offers, because config schema allows any integer:

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
