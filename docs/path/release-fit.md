# Release fit

Every step on the path is meant to land in a minor release of Drupal core. This page checks that claim against core's published change policies, one kind of change at a time.

!!! warning "A first reading, to be confirmed"
    This is a reading of the policy pages by the proof of concept's authors, not a ruling. A core committer has not reviewed it yet. Where the policies do not name a kind of change, the page says so instead of guessing.

The policies read:

- [Allowed changes during the Drupal core release cycle](https://www.drupal.org/about/core/policies/core-change-policies/allowed-changes)
- [Drupal core backend backwards compatibility and internal API policy](https://www.drupal.org/about/core/policies/core-change-policies/bc-policy)
- [Frontend backwards compatibility policy](https://www.drupal.org/about/core/policies/core-change-policies/frontend-bc-policy)
- [Experimental modules and themes: policy and list](https://www.drupal.org/about/core/policies/core-change-policies/experimental/policy-and-list)
- [How to deprecate](https://www.drupal.org/about/core/policies/core-change-policies/how-to-deprecate)

## What a minor release may add

Minor releases bring new functionality and new APIs, as long as they keep backward compatibility for public APIs ([Minor releases](https://www.drupal.org/about/core/policies/core-change-policies/allowed-changes#minor), [APIs](https://www.drupal.org/about/core/policies/core-change-policies/allowed-changes#s-apis)). Patch releases may not add APIs or features. Major releases remove deprecated code and otherwise should not break backward compatibility either.

## Each kind of change on the path

| Change | Where it appears | What the policies say | Fits a minor release? |
|---|---|---|---|
| New classes, attributes and services | Every step | New APIs that keep backward compatibility are allowed in minor releases ([APIs](https://www.drupal.org/about/core/policies/core-change-policies/allowed-changes#s-apis)). | Yes |
| New methods on existing interfaces | Groundwork (defaults, examples, labeled choices on data definitions) | Methods may be added in minor releases to interfaces not marked `@api` or `@internal` ([Interfaces](https://www.drupal.org/about/core/policies/core-change-policies/bc-policy#Interfaces-non-test)). Interfaces marked `@api` get no new methods ([Interfaces marked @api](https://www.drupal.org/about/core/policies/core-change-policies/bc-policy#Interfaces-api)). | Yes, if the interfaces involved are not marked `@api`. Each is to be checked when its issue is written. |
| Constructor changes on services and plugins | Groundwork, resources and operations | Service, plugin and controller constructors are internal unless marked otherwise, and may change in a minor release ([Constructors](https://www.drupal.org/about/core/policies/core-change-policies/bc-policy#constructors)). | Yes |
| New config or config schema keys | Simple config gains a place for another module's keys (step 3) | Not named directly. Configuration elements are part of the API and must stay compatible between releases ([Configuration elements](https://www.drupal.org/about/core/policies/core-change-policies/bc-policy#configuration-elements)). Stored config does not change on this path, so nothing a site already has is affected. | Likely, to be confirmed |
| A new module, marked experimental | The parts that are new to core, if core prefers to take them as a module first | New experimental modules may be added only in minor releases ([Experimental modules](https://www.drupal.org/about/core/policies/core-change-policies/allowed-changes#experimental)), before the alpha deadline ([Path to stable](https://www.drupal.org/about/core/policies/core-change-policies/experimental/policy-and-list#stabilizing)). Alpha modules may break their own APIs; beta modules should not. | Yes, by the policy's own rule |
| A changed form element tree | A module choosing to replace its hand-written form with a generated one | Render arrays, form arrays included, are data structures that are not stable, while the Render and Form APIs themselves are ([Render arrays](https://www.drupal.org/about/core/policies/core-change-policies/frontend-bc-policy#render-arrays)). Render array changes are allowed in minor releases ([Functionality and frontend](https://www.drupal.org/about/core/policies/core-change-policies/allowed-changes#s-functionality-and-frontend)). Form IDs are not named. | Yes for core. For contributed modules that alter the form, this is the one real cost; see below. |
| Plugins and plugin types | Structures for block and condition plugins | Particular plugins are not part of the public API ([Plugins](https://www.drupal.org/about/core/policies/core-change-policies/bc-policy#plugins)). Using an attribute class can be relied on; extending one is not supported ([Attributes](https://www.drupal.org/about/core/policies/core-change-policies/bc-policy#attributes)). | Yes |
| Deprecating an older API later | Once modules use the new pieces, if core chooses | A non-disruptive deprecation in a minor release is scheduled for removal in the next major release ([Deprecations](https://www.drupal.org/about/core/policies/core-change-policies/allowed-changes#s-deprecations)), in the format [How to deprecate](https://www.drupal.org/about/core/policies/core-change-policies/how-to-deprecate) gives. Nothing on this path asks for one. | Yes, when core decides |

## The cost the table does not show

Policy allows a form's structure to change in a minor release. That does not make the change free. A contributed module with a `hook_form_alter()` on a form whose owner switches to a generated form has to move its alter. This is why the generated form is an optional rung of [the adoption ladder](../adopting/index.md), taken by each owner at its own pace, and why core would switch its own forms one at a time, never in bulk. [What contrib sees](../adopting/contrib.md) has the details.

## If the new parts start as an experimental module

The [experimental policy](https://www.drupal.org/about/core/policies/core-change-policies/experimental/policy-and-list) asks, before a module is added, for no known security or data integrity issues, functional test coverage of the main use case, documentation with a draft change record, and a roadmap issue with a time frame, usually two minor releases, for the remaining work. A module then moves from alpha to beta to stable across minor releases.

Which parts would go into an existing core subsystem directly, and which would start as an experimental module, is an [open question](../open/index.md#where-the-parts-land).

## What is not yet checked

- Each interface the groundwork adds methods to, against its `@api` status.
- Whether core would want the config place in step 3 behind a module, or directly in the config system.
- Whether any change counts as disruptive under the allowed-changes page's own test ([Is the change disruptive?](https://www.drupal.org/about/core/policies/core-change-policies/allowed-changes#disruption): behavior existing sites might rely on, or data on existing sites). The path is designed so that none does: stored config is unchanged and only a write through an operation is checked more strictly.
