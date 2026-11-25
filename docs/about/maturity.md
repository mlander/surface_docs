# The maturity levels

Some parts of the proof of concept were designed, reviewed and tested at length. Others were written quickly to prove something can be done. Each talking point on the [board](../board.md) carries two marks, so a reader knows how much weight it can bear.

## How solid it is

| Level | What it means | What moves it up |
|---|---|---|
| <span class="level level-settled">Settled</span> | Designed with recorded decisions, reviewed by a person other than its author, and tested end to end. | Nothing. A change goes through a [proposal](../open/proposing-a-change.md). |
| <span class="level level-working">Working</span> | Built and tested end to end. The design has not been reviewed by another person. | A review by a person, and a decision record. |
| <span class="level level-sketch">Sketch</span> | In the code, mostly generated and not reviewed. It proves that something is possible. | A design pass, then tests that pin it. |
| <span class="level level-question">Question</span> | Not built. A stated question. | A design proposal. |

A person sets each level; automated reviews and test counts are only evidence for that person. Until then a part shows <span class="level level-unrated">Not yet rated</span>, possibly with a level proposed from that evidence.

## Where it is headed

- **Core, step 1 to 5.** At that step of the [path into core](../path/index.md).
- **Stays in the proof of concept.** Working, but not proposed for core.
- **Later.** Proposed for core after the five steps, once a question is settled.
- **Not decided.**

The two marks are separate because they answer different questions: staging is working code not headed for core, while the Typed Data changes are headed for core and not yet written as core patches.
