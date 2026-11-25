# One more description

Adding a description to stop data being described several times sounds backward. It is the only way out: the existing places cannot be grown to hold everything, so as long as each of them is the source, each has to be written by hand. Once one description holds everything, the others can be read from it.

## What the existing places can hold

A setting's label, description, limits and allowed values can be written in config schema. A structure not converted yet is read from config schema as it is, and nothing about config schema changes.

Three things remain, and none of them is about storage. They are about what someone may do.

### A stored object is not an action

`system.site` stores 11 keys. The site information form edits 6 of them. The default language is changed on the languages page. The notification address is changed on the account settings page, under a different permission. No form edits the UUID. Config schema lists keys. It does not say which actions exist, which keys each takes, or who may run it.

That is what a resource and its operations say.

### What a person enters is not always what is stored

The site email field shows PHP's `sendmail_from` when the stored value is empty. A machine name can be entered when a config entity is created, and never after. Core's config targets have `fromConfig` and `toConfig` callbacks for this reason.

That is what an operation says: its own input, and how it maps to what is stored.

### Some choices and rules depend on the site or on other values

The front page must be a path that exists and that the current user may visit. A list of roles or content types is whatever the site has. A key may apply only when another key has a certain value.

That is what a structure declared in code can say, beside what config schema already says.

## The same three answers for everything

Config schema covers config only. A content entity and a plugin's settings need the same three answers, and today they are written in yet other places: field definitions, form classes, plugin methods. One description covers all of them.

## What it is written in

A structure is written down as JSON Schema, which is already the language core uses for component props and the language a Tool API tool and an HTTP client read. [Portable Schema](../path/portable-schema.md) fixes the small set of extension keywords that plain JSON Schema lacks.
