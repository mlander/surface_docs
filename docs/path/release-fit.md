# Release fit

Every step on the path is meant to land in a minor release of Drupal core. This page checks that claim against core's published change policies, one kind of change at a time.

!!! warning "A first reading, to be confirmed"
    This is a reading of the policy pages by the proof of concept's authors, not a ruling. A core committer has not reviewed it yet. Where the policies do not name a kind of change, the page says so instead of guessing.

The policies read:

- [Allowed changes during the Drupal core release cycle](https://www.drupal.org/about/core/policies/core-change-policies/allowed-changes)
- [Drupal core backend backwards compatibility and internal API policy](https://www.drupal.org/about/core/policies/core-change-policies/bc-policy)
- [Frontend backwards compatibility policy](https://www.drupal.org/about/core/policies/core-change-policies/frontend-bc-policy)
- [Experimental modules and themes: policy and list](https://www.drupal.org/about/core/policies/core-change-policies/experimental/policy-and-list)

## What a minor release may add

Minor releases bring new functionality and new APIs, as long as they keep backward compatibility for public APIs. Patch releases may not add APIs or features. Major releases remove deprecated code and otherwise should not break backward compatibility either.

## Each kind of change on the path

| Change | Where it appears | What the policies say | Fits a minor release? |
|---|---|---|---|
| New classes, attributes and services | Every step | New APIs that keep backward compatibility are allowed in minor releases. | Yes |
| New methods on existing interfaces | Groundwork (defaults, examples, labeled choices on data definitions) | Methods may be added in minor releases to interfaces not marked `@api` or `@internal`. Interfaces marked `@api` get no new methods. | Yes, if the interfaces involved are not marked `@api`. Each is to be checked when its issue is written. |
| Constructor changes on services and plugins | Groundwork, resources and operations | Service, plugin and controller constructors are internal unless marked otherwise, and may change in a minor release. | Yes |
| New config or config schema keys | Simple config gains a place for another module's keys (step 3) | Not named by the policies. Config that sites provide must stay compatible between releases. Stored config does not change on this path, so nothing a site already has is affected. | Likely, to be confirmed |
| A new module, marked experimental | The parts that are new to core, if core prefers to take them as a module first | New experimental modules may be added only in minor releases, before the alpha deadline. Alpha modules may break their own APIs; beta modules should not. | Yes, by the policy's own rule |
| A changed form ID or form element tree | A module choosing to replace its hand-written form with a generated one | Form and render array structures are not covered by backward compatibility and may change in minor releases. | Yes for core. For contributed modules that alter the form, this is the one real cost; see below. |
| Plugins and plugin types | Structures for block and condition plugins | Particular plugins are not part of the public API. Using an attribute class can be relied on; extending one is not supported. | Yes |

## The cost the table does not show

Policy allows a form's structure to change in a minor release. That does not make the change free. A contributed module with a `hook_form_alter()` on a form whose owner switches to a generated form has to move its alter. This is why the generated form is the last rung of [the adoption ladder](../adopting/index.md), taken by each owner at its own pace, and why core would switch its own forms one at a time, never in bulk. [What contrib sees](../adopting/contrib.md) has the details.

## If the new parts start as an experimental module

The experimental policy asks, before a module is added, for no known security or data integrity issues, functional test coverage of the main use case, documentation with a draft change record, and a roadmap issue with a time frame, usually two minor releases, for the remaining work. A module then moves from alpha to beta to stable across minor releases.

Which parts would go into an existing core subsystem directly, and which would start as an experimental module, is an [open question](../open/index.md#where-the-parts-land).

## What is not yet checked

- Each interface the groundwork adds methods to, against its `@api` status.
- Whether core would want the config place in step 3 behind a module, or directly in the config system.
- Whether any change counts as disruptive under the allowed-changes page's own test (behavior existing sites might rely on, or data on existing sites). The path is designed so that none does: stored config is unchanged and only a write through an operation is checked more strictly.
