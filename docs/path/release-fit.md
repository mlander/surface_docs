# Release fit

Every step is meant to land in a minor release of Drupal core. This is the proof of concept authors' reading of core's change policies; a core committer has not reviewed it yet.

## The new parts are additive

Minor releases may add new APIs and features as long as public APIs stay backward compatible ([Allowed changes](https://www.drupal.org/about/core/policies/core-change-policies/allowed-changes#s-apis)). Each step adds code beside what exists: new classes, attributes and services, and new methods on data definition interfaces not marked `@api` ([Interfaces](https://www.drupal.org/about/core/policies/core-change-policies/bc-policy#Interfaces-non-test)). Stored config does not change, and only a write through an operation is checked more strictly, so a site behaves as it did before.

A generated form changes a form's element tree. Policy allows that in a minor release ([Render arrays](https://www.drupal.org/about/core/policies/core-change-policies/frontend-bc-policy#render-arrays)), but a contributed module that alters the form has to move its alter. That is why each owner switches its forms at its own pace ([What contrib sees](../adopting/contrib.md)).

## Deprecations follow core's schedule

Nothing on the path asks for a deprecation. If core later deprecates an older API, it does so in a minor release and removes the API in the next major release ([How to deprecate](https://www.drupal.org/about/core/policies/core-change-policies/how-to-deprecate)).

## If the new parts start as an experimental module

Experimental modules are added only in minor releases. Before one is added, the [experimental policy](https://www.drupal.org/about/core/policies/core-change-policies/experimental/policy-and-list) asks for no known security or data integrity issues, functional tests of the main use case, documentation with a draft change record, and a roadmap issue for the remaining work. An alpha module may still break its own API; it then moves to beta and stable across minor releases.

Which parts go into an existing core subsystem directly and which start as a module is an [open question](../open/index.md#where-the-parts-land).
