# Example 3: Fields and Tool API tools

A field on a bundle becomes one resource, `field.instance`, with three operations: create a field with a new storage, reuse an existing storage on another bundle, and update a field. Each operation becomes a Tool API tool. The three read one structure, so their inputs agree.

## Today

Tool Belt, the contributed module of ready-made Tool API tools, ships one plugin class per action on fields. `field_add` and `field_update` each declare `label`, `description`, `required` and `settings` in their own attribute, and the copies already differ: `field_add` describes the label as the "human-readable label for the field on this bundle", `field_update` as the "human-readable label for the field". Nothing makes them agree.

For a field type's settings, `field_add` reads the config schema, the only description it can reach. The address module states its field settings in five places: its config schema, `defaultFieldSettings()`, `fieldSettingsForm()` with the labels and allowed values, and two rules in PHP. The Tool API tool offers what config schema says and nothing the form knows.

## The field resource

The field resource is declared once, for every field type; in core it would sit in the field module. Identity, storage and access are on the class:

```php
--8<-- "modules/surface_examples_field/src/Resource/FieldInstanceResource.php:53:58"
```

The three operations are methods on the class:

```php
--8<-- "modules/surface_examples_field/src/Resource/FieldInstanceResource.php:67:73"
```

```php
--8<-- "modules/surface_examples_field/src/Resource/FieldInstanceResource.php:91:97"
```

```php
--8<-- "modules/surface_examples_field/src/Resource/FieldInstanceResource.php:111:115"
```

Each asks `administer %entity_type fields`, the permission Field UI already defines. The keys are declared once, in `defineInputs()`, and every operation reads them:

```php
--8<-- "modules/surface_examples_field/src/Resource/FieldInstanceResource.php:178:200"
```

`settings` depends on `field_type`. A field type whose module declares a settings class uses it. Every other field type has its settings read from its config schema, `field.field_settings.<field type>`, so the Tool API tools can add any field Field UI can.

## The address settings

`surface_examples_address` declares the address settings once:

```php
--8<-- "modules/surface_examples_address/src/Resource/AddressFieldSettingsResource.php:46:77"
```

The `#[Variant]` attribute says: when `field_type` is `address`, the field resource's `settings` are this. The field resource never names the address module, and the address module is not changed. Field UI's address settings form is drawn from the same class.

## Three Tool API tools whose inputs agree

The operations become `surface:field.instance:create`, `surface:field.instance:reuse` and `surface:field.instance:update`, with no tool class written. The label's description is the same in all three, from one line of `defineInputs()`. A change to the structure, such as a reworded description or another field type's settings, reaches all three at once, because none holds a copy.

## Compared with `field_add`

Both documents are the settings input for adding an address field, as Tool API's serializer hands it to a client. The proof of concept's [comparison test](https://git.drupalcode.org/project/surface/-/blob/631b9992/modules/surface_examples_field/COMPARISON.md) generates them.

Tool Belt's `field_add`, read from config schema, the whole `field_overrides` key:

```json
--8<-- "modules/surface_examples_field/COMPARISON.md:611:640"
```

An array of objects with one `override` string each, and nowhere to say which address property it overrides. The deprecated `fields` key is offered as an ordinary one.

`surface:field.instance:reuse`, the start of the same key:

```json
--8<-- "modules/surface_examples_field/COMPARISON.md:350:389"
```

Twelve named properties, each with its label and the three values it takes. The country and language lists are the site's. The deprecated key is gone. A key the settings do not declare, such as `country_code`, is refused by name, and nothing is created.
