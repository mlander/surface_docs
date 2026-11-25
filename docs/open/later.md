# Questions for another day

None of these has to be answered for the steps. They are listed so that nothing decided now closes them off.

- **Config schema and Typed Data.** The long-term goal is for Portable Schema to succeed both as the way data is described. That is a long way off. Until then config schema can be generated from a declared structure, so it becomes a file nobody writes by hand, and both keep being read. Field values are Typed Data objects, and that is a question for the Field API, apart from this path.
- **Field widgets.** Whether they and the elements a generated form uses grow toward one shared contract, or are joined by a bridge.
- **HTTP.** How an API for operations relates to JSON:API and REST.
- **Recipes.** Whether a config action and a recipe input read an operation's description.
- **Reading JSON Schema back into data definitions.** The other direction from writing one ([#3627345](https://www.drupal.org/project/drupal/issues/3627345)). With both, a component's props, a tool's input and a config object go through the same code. The proof of concept has a reader that does this today.
