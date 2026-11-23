# How each piece is validated

Every piece is validated the same way:

1. **Retrofit a fixed set of real cases.** Each case is code that exists in core or a contributed module, from the proof of concept's [adoption page](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/adoption.md), which groups core's forms A to H by the shape of their settings. The original module stays untouched; the retrofit is added beside it.
2. **Measure.** Files and lines added and removed; the number of places the same data is described, before and after; whether a config export changes (it must not); and whether one refused value is refused with the same message from the form, the Tool API tool, Drush and HTTP.
3. **Ask the subsystem's maintainers to review.** The maintainers of the subsystem the piece changes, as core's `MAINTAINERS.txt` lists them.

A piece is ready when its cases pass and its maintainers have reviewed it. The case list is fixed in advance so that a piece is not judged only by the cases that suit it.

## The groups

| Group | The shape | In the proof of concept |
|---|---|---|
| A | `ConfigurableInterface` plus the `PluginFormInterface` triple: conditions, actions, image effects, blocks | Built. Blocks, conditions and actions ported. |
| B | A settings form the host collects itself: field formatters and widget settings | Built. Formatters ported. |
| C | Field types: storage and instance settings on one plugin | Half built. Address instance settings ported; storage settings described, with no Field UI host. |
| D | A form class per operation: blocks, workflow types | Built. One generic form class. |
| E | Config entity forms | Built for two: content types and placed blocks. |
| F | `ConfigFormBase` with `#config_target` | Storage built. No core form ported, and `#config_target` is not read. |
| G | Field widgets collecting content | Designed, not built. |
| H | Views plugins, menu link forms, image toolkits, Migrate, inline blocks | Out of scope for now. |

Two contributed settings forms were also ported outside the proof of concept's repository, with both originals untouched: Honeypot's and Pathauto's ([the log](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/adopters-2026-10-19.md)).

## Cases per piece

### Groundwork in core {#groundwork-in-core}

- The menu block's number of levels, described in 6 places in core 11.4 (group A): defaults, examples and constraints as keywords.
- The content type's preview mode, whose labels live only in the `NodePreviewMode` enum (group E): labels on `Choice`.
- Two unsaved field configs of one field type in one request (group C): the prototype cache.
- An add form for a bundle with no stub entity (group C and the entity side): field defaults and access without an entity.
- Honeypot's `#states` dependency, as a declared condition.

### Structures {#structures}

- Every core block plugin with only config schema, read and placed through a resource (groups A and E, `surface_examples_block`).
- A condition and an action plugin's settings (group A), a formatter's settings (group B).
- The address field type's instance settings, and storage settings read from config schema for every field type the UI offers (group C).
- One generic form that a plugin lists under any of its named operations (group D).
- Content type settings another module adds, once through an alter and once through a form alter (`surface_examples_extras`).
- Pathauto's settings: keys listed from the site, and entries added to a list the owner stores.
- For resources beside, not built: Metatag, the URL alias, Paragraphs.

### Resources and operations {#resources-and-operations}

- The content type create and update operations, and a placed block (group E).
- Simple config: the first example's settings and `system.performance` (group F); a core settings form with `#config_target` is the next case.
- Honeypot's three form-only validation rules and its permission, held at every way in.
- Generated forms: the same cases drawn with no form class (groups D and E).

### Portable Schema {#portable-schema}

- Every example's committed contract baseline, held to the matrix tests: accepted and refused values through validation and both documents with a standard validator.
- The field tools against Tool Belt's `field_add` on the address field type.
- A content type setting another module added, through a Tool API tool that names no key of it.
- The React client, drawing every example from the documents alone.

## What the evidence is today

The ports so far were made by agents and checked by tests and by automated reviews. No person outside the project has run a retrofit yet, and a level on this site is set only by a person ([the maturity levels](../about/maturity.md)). Running one of the cases above by hand is the most useful review a piece can get.
