# Fields and Tool API tools

A field on a bundle becomes one resource, `field.instance`, with three operations: create a field with a new storage, reuse an existing storage on another bundle, and update a field. Each operation is published as a Tool API tool. The three share one structure, so their inputs agree, and one change to that structure reaches all three tools at once. The address field type's settings show what that structure can say that config schema cannot.

## Today

A field's label, help text and required flag are described by core's `field_config_base` config schema and by Field UI's `FieldConfigEditForm`. Tool Belt, the contributed module of ready-made Tool API tools, describes them again.[^toolbelt] It ships one plugin class per action on fields: `field_add`, `field_update` and `field_delete`, and `field_storage_add`, `field_storage_update` and `field_storage_delete`. `field_add` and `field_update` each declare `label`, `description`, `required` and `settings` in their own attribute. On a site with Tool Belt, a field's label is described in 4 places. The two tool copies already differ: `field_add` describes the label as the "human-readable label for the field on this bundle", `field_update` as the "human-readable label for the field". Nothing makes them agree.

A field type's own settings are described by the field type. The address module (2.0.4) describes its field settings in 5 places:[^address]

- the `field.field_settings.address` config schema: three types, and a fourth, deprecated key;
- `AddressItem::defaultFieldSettings()`: the defaults;
- `AddressItem::fieldSettingsForm()`: the labels, the descriptions, and the three values an override takes;
- `AddressItem::fieldOverridesValidate()`: a rule, that an empty override is dropped;
- `AddressItem::getFieldOverrides()`: a rule, that the deprecated `fields` key overrules `field_overrides` whenever it is set.

Tool Belt's `field_add` reads the settings input from the config schema, the one description it can reach. So the tool offers what the config schema says, and nothing the form knows.

## The change

### The field, once

`surface_examples_field` declares the field resource. In core it would sit in the field module, once, for every field type. Identity, storage and access are on the class:

```php
--8<-- "modules/surface_examples_field/src/Resource/FieldInstanceResource.php:54:59"
```

The three operations are methods on the same class, because each knows a different part of the field:

```php
--8<-- "modules/surface_examples_field/src/Resource/FieldInstanceResource.php:68:74"
```

```php
--8<-- "modules/surface_examples_field/src/Resource/FieldInstanceResource.php:93:99"
```

```php
--8<-- "modules/surface_examples_field/src/Resource/FieldInstanceResource.php:115:119"
```

Each asks `administer %entity_type fields`, the permission Field UI already defines per entity type. The keys are declared once, in `defineInputs()`, and every operation reads them:

```php
--8<-- "modules/surface_examples_field/src/Resource/FieldInstanceResource.php:189:211"
```

The `settings` key depends on the value of `field_type`. A field type whose module declares a settings class uses it. Every other field type offered in Field UI has its settings read from its config schema, `field.field_settings.<field type>`, with the field type's own defaults, so the tools can add any field Field UI can.

### The address field's settings

`surface_examples_address` declares the address settings once, as the settings for the address field type:

```php
--8<-- "modules/surface_examples_address/src/Resource/AddressFieldSettingsResource.php:46:77"
```

`#[Variant(of: FieldInstanceResource::class, at: 'settings', for: 'address')]` says: when `field_type` is `address`, the field resource's `settings` are this. The field resource never names the address module. The country and language lists are named as constraints, `Country` and `LanguageExists`, and listed live. The deprecated `fields` key is not offered, and every write through the resource stores it empty, so it can no longer overrule `field_overrides`.

The address module is not changed. `surface_examples_address` swaps the field type's item class in `hook_field_info_alter()`, so Field UI draws the address settings from the same class.

### Counts

| Module | Files | Lines | Code lines |
|---|---:|---:|---:|
| `surface_examples_field`: the field and storage resources, their storage and access classes, settings read from config schema for every other field type | 8 | 1,050 | 541 |
| `surface_examples_address`: the address settings, their storage, the item class swap | 5 | 459 | 189 |

"Code lines" leaves out blank lines and comment lines. Each module's `.info.yml` (10 lines) and README are not counted. **Removed: nothing.** The address module, core's field module and Field UI are not changed.

## What it gets

### One resource, three tools, one structure

The three operations become `surface:field.instance:create`, `surface:field.instance:reuse` and `surface:field.instance:update`. The field storage's update operation becomes `surface:field.storage:update`. No tool class is written for any of them.

Because the operations read one structure, their inputs agree. The label is "The human readable label for the field on this bundle." in all three tools, from one line of `defineInputs()`. Where an operation takes less, it says so against the same structure: update knows which field it edits, so the entity type, bundle, machine name and field type are fixed, and an update tool requires no key at its own input ([decision](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/decisions.md#required-is-the-resources-and-an-update-tool-requires-nothing-at-its-door)).

One change to the structure reaches all of them. Reword the label's description, add a rule to the machine name, or let another module add a field type's settings, and the create, reuse and update tools change together, because none of them holds a copy. The address settings arrive that way: the address example adds one class, and all three tools offer the address settings.

### What the tool offers

Both documents below are the settings input of a tool that adds an existing address storage's field to a bundle, as the Tool API's own serializer hands it to a client. They are generated by the proof of concept's comparison test, not written by hand ([COMPARISON.md](https://git.drupalcode.org/project/surface/-/blob/75a53469/modules/surface_examples_field/COMPARISON.md)).

From the config schema, Tool Belt's `field_add`, the whole `field_overrides` key:

```json
--8<-- "modules/surface_examples_field/COMPARISON.md:611:640"
```

An array of objects, each with one `override` string, and nowhere to say which address property it overrides. The deprecated `fields` key is offered as an ordinary one.

From the resource, `surface:field.instance:reuse`, the start of the same key:

```json
--8<-- "modules/surface_examples_field/COMPARISON.md:350:389"
```

Twelve named properties, each with its label and the three values it takes. The country list is the site's, live, and the language list is the site's languages. The deprecated key is gone.

### The same input, refused

An override of `mandatory` for the organization is refused, the message naming `field_overrides` and `organization`, and nothing is created. A key the settings do not declare, such as `country_code`, is refused by name. A dry run checks everything, including the storage's own checks, and writes nothing. These are tested through the Tool API tools (`FieldToolsTest`). Field UI's settings form for an address field is drawn from the same class (`FieldUiAddressSettingsTest`).

Not yet in the proof of concept: a test of the field resource over HTTP, and a delete operation. Tool Belt's `field_delete` has no counterpart yet.

## Later, if ever

- **Field UI's own field form.** Only the address settings part of Field UI's form is drawn from the description. The rest of `FieldConfigEditForm` stays hand-written. Replacing it is not proposed here.
- **Storage settings in Field UI.** The storage resource describes storage settings, and the tools set them, such as a string's `max_length`. Field UI has no form drawn from them yet.
- **Field widgets.** They are not changed. A widget collecting a field's values stays a widget; the widgets a generated form uses are a separate thing.

## Another module's view

**Before.** The address module's settings are described in its own item class, and a tool built elsewhere can only read the config schema. To offer better settings in a tool, a tool author would write them again, in each tool.

**After.** The address settings class declares itself the settings for one field type of another module's resource, with one attribute. It is found by its attribute, and skipped on a site without the field resource. Every tool and form built from the field resource offers it. A third module could add a field type's settings the same way, without touching the field resource or any tool.

## What stays as it is

- Stored config: `field.field.*` and `field.storage.*` are saved by their entities, as Field UI saves them. Address settings are stored in the layout the address module reads, so `AddressItem::getAvailableCountries()` and `getFieldOverrides()` read a field the same way whichever form or tool configured it.
- Core's field config schema, and the address module's.
- The address module's code. Field UI's routes and permissions.
- Field widgets.
- Tool Belt. Its tools keep working beside these. A module that describes other modules' data again for Tool API tools could delete its copies and read the resource instead ([What contrib sees](contrib.md)).

## Open to improve

- The tools found gaps in the Tool API that the proof of concept did not work around. They are listed in [Notes for the Tool API](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/tools.md#notes-for-the-tool-api) and summarized in [core gaps](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/core-gaps.md). One example: a `Regex` with the `D` modifier is not carried into the tool's schema, so the machine name's pattern is checked when the tool runs, but not stated to the caller in advance.
- How a list of field types longer than the site's limit is served: past it, `settings` is stated open and fetched per field type.
- Parameters name a field by its parts, never by a composite id such as `node.article.body` ([decision](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/decisions.md#a-parameter-is-identity-the-caller-knows)). Whether that suits every caller is open.

The comparison and its reasoning are in the proof of concept's [adoption notes](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/adoption.md#the-tool-api-ab). The wider argument is on [Why not Tool API](../why/not-tool-api.md).

## Try it

```bash
--8<-- "modules/surface_examples_field/README.md:156:158"
```

`drush tool:info surface:field.instance:reuse` prints the inputs. With Tool Belt installed on the same site, `drush tool:info tool_belt:field_add` prints the other side.

[^toolbelt]: Tool Belt 1.0.x at commit `4216489c`, `modules/tool_belt_entity/src/Plugin/tool/Tool`. Core 11.4. A place counts when it states the type, the label, the default, the allowed values or a rule. Code that only reads the value does not count. The field label's 4: the `field_config_base` config schema, `FieldConfigEditForm`, and the `field_add` and `field_update` attributes.

[^address]: Address 2.0.4, `src/Plugin/Field/FieldType/AddressItem.php` and `config/schema/address.schema.yml`. The country parts of the defaults and the form sit in `AvailableCountriesTrait`, which the two methods call; they are counted with the methods.
