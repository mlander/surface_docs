# Why not forms from config schema

A form looks like the obvious thing to generate from config schema: the keys, their types and their labels are there. It does not work, even for a simple settings form.

## What a form needs that config schema does not say

- **Which keys it takes.** `system.site` stores 11 keys and its form edits 6. Config schema lists all 11 and says nothing about which belong to which form.
- **Who may use it.** The permission is on the form's route, not in the schema. Two actions on one config object can need different permissions.
- **How entered values become stored values.** A field that shows a fallback when the stored value is empty, or a key that is entered once and never changed, is a rule of the action, not of storage.
- **Rules that depend on the site.** A path that must exist, a choice list that is whatever the site has.

A form is one way to run an action. Without a description of the action, nothing says which keys a form takes or who may submit it. The same is true of a Tool API tool.

## So the action comes first

An operation states the keys it takes, the permission it needs and how its input maps to what is stored. A form, a Tool API tool and Drush are then each one way to run it, with the same validation.

A module declares the keys it owns in Portable Schema. For config another module owns and has not converted, and for plugins and config with no resource class, each key's type and label are read from config schema as the bridge.

## And forms when wanted

A module gets one validation for every way in and a Tool API tool per operation first. Replacing its hand-written form with a generated one is optional and happens at its own pace ([the adoption ladder](../adopting/index.md)). Automatic form generation will scale from small simple forms to complex, dynamic use cases. Form alters stay available for cosmetic changes, and a headless or React client can draw the same form because it is drawn from Portable Schema.
