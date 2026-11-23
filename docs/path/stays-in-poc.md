# Stays in the proof of concept

These parts work and are tested. They help prove the rest, and none of the five steps needs them. They are not proposed for core now.

## HTTP

An API where the path is the resource and the method is the operation, with a read, a dry run, a narrowing call for in-progress values, `If-Match` on a write and refusals as problem details, plus an OpenAPI 3.1 document of it. Both are submodules of their own, `surface_http` and `surface_openapi`, because a site that only builds forms or only offers Tool API tools has no reason to answer requests under `/surface-api`; core keeps `rest` and `jsonapi` apart from `serialization` the same way ([decision](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/decisions.md#the-http-door-and-the-openapi-document-are-their-own-modules)).

Why not now: how an API for operations relates to JSON:API and REST is not settled ([questions for another day](../open/later.md)). The [served contract](portable-schema.md#served) does go to core in step 4: HTTP is one client of it.

## Staging

A set of writes kept and applied together, or discarded: an agent edits several pages and a person checks them first, or a set of edits must land in one transaction. A stage is a resource of its own, kept in an expirable key-value collection, and multi-step forms are drawn over it ([Staging](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/staging.md)).

Why not now: it is one of the proof of concept's experimental ideas, its stored shape may change in any commit, and only the proof of concept's own ways in read through a stage; listings, Views and queries never see one. How it relates to Workspaces is not worked out beyond the cases its documentation lists.

## React

An example client: a resource's form rendered in React from the served documents alone, written in JavaScript against the HTTP API with no PHP (`surface_examples_react`). It proves that the contract is enough for a client to draw, narrow and check a form the way the server does.

Why not now: it is a demonstration of the contract, not something core needs to ship. A React package is listed as not in the first steps.

## Generator

`drush generate surface:resource` writes a resource's files from an interview, from a config schema entry or from a JSON Schema document, and a test holds its output to the first example byte for byte ([decision](https://git.drupalcode.org/project/surface/-/blob/75a53469/docs/decisions.md#the-generator-writes-what-the-first-page-shows)).

Why not now: it is a development aid built on Drush, which is not part of core, and it is experimental. Adopting needs no generated code: a module that keeps config schema as its source writes nothing.
