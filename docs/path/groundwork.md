---
topic: facts-on-a-definition
---

# Groundwork in core

Core's data definitions cannot state some facts a description needs: a default, example values, a label for each allowed choice, a rule that applies only when another key has a certain value. Step 1 adds them to Typed Data, validation and the Field API.

It comes first because everything after it reads these facts. Each one pays off alone: core already derives JSON Schema from definitions, so a definition that states its default shows it there with no other change.

Three items are in core's queue: defaults ([#3620920](https://www.drupal.org/project/drupal/issues/3620920)), examples ([#3620922](https://www.drupal.org/project/drupal/issues/3620922)), and constraints written as JSON Schema keywords ([#3627330](https://www.drupal.org/project/drupal/issues/3627330)). The rest are drafted in the proof of concept's [core gaps](https://git.drupalcode.org/project/surface/-/blob/3f708be7/docs/core-gaps.md#step-1-facts-on-a-data-definition), where each is working code today.
