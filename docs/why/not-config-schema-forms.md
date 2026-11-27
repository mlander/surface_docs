# Why not forms from config schema

Config schema looks like the obvious thing to generate forms from: the keys, their types and their labels are there. It is not enough, even for a simple settings form.

Adding one more description to stop data from being described several times can sound backward. But no existing place can be extended to hold what a form, a Tool API tool and validation need, so today each of them is written by hand. Once one description holds it, the others can be read from it.

## What a form needs that config schema does not say

- **Which keys it takes.** `system.site` stores 11 keys and its form edits 6. Config schema lists all 11 and says nothing about which belong to which form.
- **Who may use it.** The permission is on the form's route, not in the schema. Two actions on one config object can need different permissions: the site's notification address is changed on the account settings page, under "administer account settings".
- **How entered values become stored values.** The site email field shows PHP's `sendmail_from` when the stored value is empty. A config entity's machine name is entered once, when it is created. These are rules of the action, not of storage.
- **Rules that depend on who is acting.** The front page must be a path the account saving the form may visit. Config is also written by imports and recipes, where there is no such account, so config schema has no place for this rule. An operation always runs as an account.
- **Choices with labels.** Config schema allows any integer for the page cache's maximum age; core's form offers 14 periods, each with a label. Config schema can check a value against a list, but it gives a form no labels to show.

A form is one way to run an action. Without a description of the action, nothing says which keys a form takes or who may submit it. The same is true of a Tool API tool.

## So the action comes first

An operation states the keys it takes, the permission it needs and how its input maps to what is stored. A form, a Tool API tool and Drush are then each one way to run it, with the same validation.

A module declares the keys it owns in Portable Schema. For config another module owns and has not converted, and for plugins and config with no resource class, each key's type and label are read from config schema as the bridge.

## Not only config

Config schema covers config only. Content entities and plugin settings need the same answers, and today they are written in other places: field definitions, form classes, plugin methods. One description covers all of them. It is written as JSON Schema, which core already uses for component props and which a Tool API tool reads; [Portable Schema](../path/portable-schema.md) adds the few extension keywords plain JSON Schema lacks.

## And forms when wanted

A module gets one validation for every way in and a Tool API tool per operation first. Replacing its hand-written form with a generated one is optional and happens at its own pace ([the adoption ladder](../adopting/index.md)). Automatic form generation will scale from small simple forms to complex, dynamic use cases. Form alters stay available for cosmetic changes, and a headless or React client can draw the same form because it is drawn from Portable Schema.
