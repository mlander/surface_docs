# Example 2: Placing a block

A placed block becomes one resource, `block.placement`, with create, update and delete operations. Its `settings` key holds whatever the chosen block plugin takes. A plugin that declares its structure is placed through that structure (rung 2). A plugin with only config schema has its structure read from that schema and is placed the same way, with no change to the plugin (rung 0).

## Today

A placed block is the config entity `block.block.<id>`, and each plugin describes its own settings. Core's branding block describes its three settings, whether to show the logo, the site name and the slogan, in three places: the `block.settings.system_branding_block` config schema gives types and labels, `defaultConfiguration()` gives defaults, and `blockForm()` gives other labels and descriptions. Only the block form uses them. Core has no Tool API tool that places a block and checks its settings.

## The resource, added once

The module that owns block placement adds the resource; in core that is the block module. It names the block config entity as its storage, the machine name as its identity, and its operations: create, update and delete, with a read added beside them. Update names the block by its machine name and keeps it in its own theme. Each asks "administer blocks", the permission core's block layout asks today:

```php
--8<-- "modules/surface_examples_block/src/Resource/BlockPlacementResource.php:35:87"
```

Its input is every key a placed block has: label, machine name, whether the label shows, the plugin, the plugin's settings, theme, region, weight, status and visibility conditions. The `settings` key depends on the chosen plugin:

```php
--8<-- "modules/surface_examples_block/src/Resource/BlockPlacementResource.php:96:162"
```

The regions offered depend on the theme chosen:

```php
--8<-- "modules/surface_examples_block/src/Resource/BlockPlacementResource.php:167:170"
```

`x-surface-variants` names the class that gives each plugin's structure. A plugin that declares a structure gets it. Any other plugin gets the structure read from its config schema, `block.settings.<plugin id>`, with the plugin's defaults laid over it:

```php
--8<-- "modules/surface_examples_block/src/Variants/BlockPluginStructures.php:115:126"
```

No block plugin changes for this.

## A block with only config schema

Core's branding block is not touched. The resource's served schema shows what is read:

```json
--8<-- "tests/fixtures/block-placement/block.placement.create.full.json:2263:2289"
```

The types and labels come from config schema, the defaults from `defaultConfiguration()`. The labels and descriptions in `blockForm()` are not read, because they live in PHP that nothing else can read. That is enough to place the block and check its settings.

On the test site the block layout offers 16 plugins. One declares its structure, and 15 are read from config schema, each named by the schema it came from:

```json
--8<-- "tests/fixtures/block-placement/block.placement.create.full.json:186:208"
```

## A block that declares its structure

The component block embeds a single-directory component. Its config schema cannot say what the props are, because which components exist depends on the site:

```yaml
--8<-- "modules/surface_examples_component_block/config/schema/surface_examples_component_block.schema.yml"
```

So the plugin declares a structure in which each component's props depend on the component chosen:

```php
--8<-- "modules/surface_examples_component_block/src/Structure/ComponentBlockStructure.php:34:51"
```

and names it on the plugin class:

```php
--8<-- "modules/surface_examples_component_block/src/Plugin/Block/ComponentBlock.php:26:31"
```

The placement resource places it with no code added for it.

## What it gets

Every way in runs the same operation and the same checks. A region of another theme sent for a block in Stark is refused at `/region`: "The stark theme has no region named pre_content." Before it writes, the storage checks the whole block against core's `block.block.*` config schema, so what is stored is what core's block form would store.

Core's block form, its routes, every block plugin and their config schema stay as they are.
