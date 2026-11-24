# Why not forms from config schema

A form looks like the obvious thing to generate from config schema: the keys, their types and their labels are all there. It does not work, not even for a simple settings form.

## What a form needs that config schema does not say

- **Which keys it takes.** `system.site` stores 11 keys and its form edits 6. Config schema lists all 11 and says nothing about which belong to which form.
- **Who may use it.** The permission is on the form's route, not in the schema. Two actions on one config object can need different permissions.
- **How entered values become stored values.** A field that shows a fallback when the stored value is empty, or a key that is entered once and never again, are rules of the action, not of storage.
- **Rules that depend on the site.** A path that must exist, a choice list that is whatever the site has.

A form is one way to run an action. Without a description of the action, nothing says which keys the form takes or who may submit it. The same is true of an HTTP endpoint and a Tool API tool.

## So the action comes first

An operation states the keys it takes, the permission it needs and how its input maps to what is stored. A form, a Tool API tool and an HTTP call are then each one way to run it, with the same validation. Config schema stays the source of the keys' types and labels where it is enough, which for most static settings it is.

## And forms when wanted

A module gets the rest first: one validation for every way in, a Tool API tool, a published description. Replacing its hand-written form with one read from the description is optional, and happens at its own pace ([the adoption ladder](../adopting/index.md)).
