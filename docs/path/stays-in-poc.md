# Stays in the proof of concept

These parts work and help prove the rest, but none of the five steps needs them. They are not proposed for core now.

## Staging

A set of writes kept together, then applied or discarded, so a person can check an agent's edits before they land. It is experimental, and how it relates to Workspaces is not worked out.

## React

An example client that draws a resource's form in React from the served documents alone. It shows the contract is enough for a client to draw and check a form; core does not need to ship it.

## Generator

A Drush command that writes a resource's files from a config schema entry or a JSON Schema document. It is a development aid built on Drush, which is not part of core, and adopting needs no generated code.
