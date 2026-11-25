# Placing a block

A placed block becomes a resource, `block.placement`, with create, update and delete operations. Its settings key holds whatever the chosen block plugin takes. A plugin that declares its own structure is placed through that structure (rung 2). A plugin that has only config schema has its structure read from that config schema and is placed the same way, with no change to the plugin (rung 0). Both kinds sit in the same resource, side by side, and a caller cannot tell them apart except by how much each one says.

The resource is added once, by the module that owns block placement. No block plugin has to change for it.

## Today

In Drupal core 11.4 a placed block is the config entity `block.block.<id>`. Its theme, region, weight and visibility are described by the `block.block.*` config schema and by core's block form. Each plugin's own settings are described again by the plugin.

Core's branding block is one of the better-described plugins: its config schema is marked fully validatable. Its settings, whether to show the logo, the site name and the slogan, are described in 3 places:[^branding]

- the `block.settings.system_branding_block` config schema, which gives each key its type and a label ("Use site logo");
- `defaultConfiguration()`, which gives each key its default;
- `blockForm()`, which gives each key a different label ("Site logo") and a description.

None of the three can be run from outside the block form. There is no Tool API tool or HTTP call in core that places a block and checks its settings.

## The change

### What the owner of block placement adds, once

The proof of concept adds the placement resource in a submodule, `surface_examples_block`. In core it would sit in the block module. It names the block config entity as its storage, its machine name as its identity, and its operations:

```php
--8<-- "modules/surface_examples_block/src/Resource/BlockPlacementResource.php:35:48"
```

Update and delete are methods on the same class with their own `#[Operation]` attribute, because each names the block it acts on. All three ask "administer blocks", the permission core's block layout asks today. Nothing adds a permission.

The settings key is where the plugin chooses:

```php
--8<-- "modules/surface_examples_block/src/Resource/BlockPlacementResource.php:123:131"
```

`x-surface-variants` says that the value of `settings` depends on the value of `plugin`, and names the class that lists, for each plugin, which structure applies. That class is the whole of rungs 0 and 2 for blocks. A plugin that declares a structure gets it. Any other plugin gets the structure read from its config schema, `block.settings.<plugin id>`, or `block.settings.*` when it has none, with the plugin's own defaults laid over it:

```php
--8<-- "modules/surface_examples_block/src/Variants/BlockPluginStructures.php:115:126"
```

What is added, in the proof of concept:

| File | Lines | Code lines |
|---|---:|---:|
| `src/Resource/BlockPlacementResource.php`: the resource and its operations | 172 | 112 |
| `src/Storage/BlockPlacementResourceStorage.php`: keeps the values on the block entity as core stores them | 323 | 179 |
| `src/Variants/BlockPluginStructures.php`: which structure each block plugin's settings have | 190 | 84 |
| `src/Variants/ConditionPluginStructures.php`: the same for visibility conditions | 214 | 109 |
| `src/Structure/VisibilityConditionStructure.php`: one visibility condition | 50 | 27 |
| Three constraint classes: a region of the chosen theme, or of any installed theme | 194 | 90 |
| `src/Plugin/SurfaceOptionsResolver/ThemeRegionOptions.php`: lists those regions | 81 | 43 |
| `src/Form/BlockPlacementFormCosmetics.php`: the message and the page to return to after the generated form | 65 | 33 |
| `surface_examples_block.routing.yml` and `.services.yml` | 54 | 32 |
| **12 files** | **1,343** | **709** |

"Code lines" leaves out blank lines and comment lines. The example module's `.info.yml` (10 lines) and README are not counted. **Removed: nothing.**

The three routes in `routing.yml` serve a generated form at `/admin/structure/block/surface/add` and beside it. They are optional: the Tool API tools and HTTP need no route. Core's own block form and its routes are not touched.

### What a legacy block adds: nothing

Core's branding block is not touched. Its structure is read from its config schema, and the resource's served schema shows what came of it:

```json
--8<-- "tests/fixtures/block-placement/block.placement.create.full.json:2263:2289"
```

The types and labels are the config schema's. The defaults are the plugin's own `defaultConfiguration()`. Each key is required because the schema is marked fully validatable. The labels and descriptions in `blockForm()` are not read: they live in PHP that nothing else can read, so a caller sees "Use site logo" with no description. That is what rung 0 gives, and it is already enough to place the block and have its settings checked.

On the test site the block layout offers 16 plugins. One declares its structure, and 15 are read from config schema, each named by the schema it came from:

```json
--8<-- "tests/fixtures/block-placement/block.placement.create.full.json:186:208"
```

### What a block that declares its structure adds

The component block in `surface_examples_component_block` embeds a single-directory component. Its config schema cannot say what its props are, because which components a site has is the site's:

```yaml
--8<-- "modules/surface_examples_component_block/config/schema/surface_examples_component_block.schema.yml"
```

So the plugin declares a structure, where each component's props depend on the component chosen:

```php
--8<-- "modules/surface_examples_component_block/src/Structure/ComponentBlockStructure.php:34:51"
```

and names it on the plugin class:

```php
--8<-- "modules/surface_examples_component_block/src/Plugin/Block/ComponentBlock.php:26:31"
```

That is rung 2 for a block: one structure class (53 lines, 22 code lines) and one attribute on the plugin, which extends `TypedBlockBase`. The placement resource places it with no code added for it ([decision](https://git.drupalcode.org/project/surface/-/blob/d5486fd4/docs/decisions.md#a-block-embeds-a-component-through-its-structure)). The component block was written for the proof of concept, so it has no "before" to compare with. Its config schema stays hand-written.

## What it gets

Every way in runs the same operation, so each is refused by the same rule. A region of another theme sent for a block in Stark:

| Way in | What comes back |
|---|---|
| Tool API tool `surface:block.placement:create` | Refused at `/region`: "The stark theme has no region named pre_content." |
| HTTP `PATCH /surface-api/block.placement/{id}` | 422, at `/region`, with the same message |
| Generated form | Once Stark is chosen, the region list offers only Stark's regions, so Form API refuses the value before the operation runs, in Form API's own words: "The submitted value pre_content in the Region element is not allowed." |

The rule is the same everywhere. The words on the form are not yet the same, because Form API checks a select's options first. A machine name already in use is refused at `/id` with the code `taken`, and a dry run checks everything and writes nothing.

Before the write, the storage holds the whole block to core's `block.block.*` config schema and calculates its dependencies as a save would. What is stored is what core's own block form would store.

The tests: `BlockPlacementToolsTest`, `BlockPlacementApiTest`, `BlockPlacementFormTest` and `BlockPlacementResourceTest`, which also pins both served documents.

## Later, if ever

- **Rung 2 for the branding block.** Declaring its structure would carry the form's labels and descriptions to every caller. For three booleans whose rules config schema already states, that is not worth much. Reading the config schema is enough for now.
- **Rung 3 for the block layout.** Pointing core's block form route at the operation's form is possible, but it is not proposed here. Two things stand in the way: a plugin that reads a context, such as the node of the page, is not offered yet, and a block cannot move between themes through the update operation.
- **Rung 4 for a block plugin.** A block that declares its structure no longer needs `defaultConfiguration()`, `blockForm()`, `blockValidate()` or `blockSubmit()`. The proof of concept keeps one block written both ways, [`surface_examples_classic`](https://git.drupalcode.org/project/surface/-/blob/d5486fd4/modules/surface_examples_classic/README.md), and a test holds the two to the same behavior.

## Another module's view

**Before.** A module that adds a setting to blocks alters core's block form with `hook_form_alter()` and stores the value in the block's third-party settings. The setting reaches that form and nothing else.

**After.** It alters the block's structure. The example below adds a badge to the example block in `surface_examples_plugins`, which the build stores under `third_party_settings.surface_examples_extras.badge`, and caps the item count while the block is a grid:

```php
--8<-- "modules/surface_examples_extras/src/Alter/ExampleBlockAlter.php:42:75"
```

The alter changes the structure, not a form, so whatever builds the structure gets the badge: the block's configuration form, its validation, and the placement resource's settings for that block. An alter may add keys under its own module's name, reword an owner's help text, and narrow an owner's rule. It may not widen one ([how another module's keys work](../path/structures.md)).

Not yet in the proof of concept: an alter of a block whose structure is read from config schema, such as the branding block. An alter today names a class that declares a structure, or a derived resource by its id.

## What stays as it is

- Every block plugin. A legacy block needs no change to be placed.
- The `block.block.*` config schema, and each plugin's `block.settings.*` schema.
- Stored config: a block placed through the resource is saved through the block entity and stored as core stores it.
- Core's block layout, its block form, its routes, and the "administer blocks" permission.

## Open to improve

- A plugin that reads a context is not offered, because which context a placed block reads is not decided.
- The update operation keeps a block in its theme. Moving a block between themes is not offered.
- Layout Builder's components are not placements.
- Without JavaScript, the generated create form draws a plugin's settings only after the plugin is chosen.

Each choice and the alternatives set aside are recorded in [A placed block is a resource](https://git.drupalcode.org/project/surface/-/blob/d5486fd4/docs/decisions.md#a-placed-block-is-a-resource).

## Try it

```bash
--8<-- "modules/surface_examples_block/README.md:15:15"
```

Place a component block in Olivero's sidebar as a dry run:

```bash
--8<-- "modules/surface_examples_block/README.md:106:106"
```

Open `/admin/structure/block/surface/add`, choose **Site branding**, and its three settings are drawn from its config schema. The module's [README](https://git.drupalcode.org/project/surface/-/blob/d5486fd4/modules/surface_examples_block/README.md) lists every route, tool and test.

[^branding]: Counted in Drupal core 11.4, `core/modules/system`. A place counts when it states the type, the label, the default, the allowed values or a rule. `blockSubmit()` copies the three values into the configuration and states nothing about them, so it is not counted.
