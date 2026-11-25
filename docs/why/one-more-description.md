# One more description

Adding a description to stop data from being described several times sounds backward. But the existing places cannot be extended to hold everything a form, a Tool API tool and validation need, so today each of them is written by hand. Once one description holds everything, the others can be read from it.

## What the existing places cannot hold

Config schema states a setting's type, label, limits and allowed values. Three things remain, and they are about actions, not storage.

- **Which actions exist.** `system.site` stores 11 keys. The site information form edits 6 of them, the notification address is changed on the account settings page under a different permission, and no form edits the UUID. Config schema lists the keys. It does not say which actions exist, which keys each takes, or who may run it. A resource and its operations say that.
- **How input maps to storage.** The site email field shows PHP's `sendmail_from` when the stored value is empty. A config entity's machine name is entered once, when it is created. An operation states its own input and how that input maps to what is stored.
- **Rules that depend on the site or on other values.** The front page must be a path that exists and that the current user may visit. A list of roles is whatever the site has. A key may apply only when another key has a certain value. A structure declared in Portable Schema states these rules beside the types.

A module declares in Portable Schema the keys it owns. For config another module owns and has not converted, and for plugins and config with no resource class, the keys are read from config schema, which does not change.

## Not only config

Config schema covers config only. Content entities and plugin settings need the same three answers, and today they are written in other places: field definitions, form classes, plugin methods. One description covers all of them.

## What it is written in

A structure is written as JSON Schema, which core already uses for component props and which a Tool API tool reads. [Portable Schema](../path/portable-schema.md) adds the few extension keywords that plain JSON Schema lacks.
