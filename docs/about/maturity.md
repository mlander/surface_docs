# The maturity levels

Some parts of the proof of concept have been designed, argued over and tested at length. Others were written quickly to prove that something can be done, and nobody but their author has read them. Both kinds are on this site, and each talking point says which it is, so that a reader knows how much weight a part can bear and where help is most useful.

Each talking point carries two marks.

## How solid it is

| Level | What it means | What moves it up | What its page invites |
|---|---|---|---|
| <span class="level level-settled">Settled</span> | Designed with recorded decisions, reviewed by a person other than its author, and tested end to end. | It does not move on its own. A change goes through a [change proposal](../open/proposing-a-change.md). | A change proposal that builds on the recorded reasoning. |
| <span class="level level-working">Working</span> | Built and tested end to end. The design has not been reviewed by another person. | A review by a person, and a decision record. | Review and redesign. |
| <span class="level level-sketch">Sketch</span> | In the code, mostly generated and not reviewed. It proves that something is possible. | A design pass, then tests that pin it. | A design from scratch that keeps what it proves. |
| <span class="level level-question">Question</span> | Not built. A stated question. | A design proposal. | Proposals. |

A person sets the level. Automated reviews and test counts are evidence for that person, but they never make a part Settled on their own.

Until a person has rated a part, its strip says <span class="level level-unrated">Not yet rated</span>, and may show a level proposed from the evidence in the repository.

## Where it is headed

- **Core, step 1 to 5.** Part of the [path into core](../path/index.md), at that step.
- **Stays in the proof of concept.** Working, and useful to prove the rest, but not proposed for core.
- **Later.** Proposed for core after the steps, once a question is settled.
- **Not decided.**

The two marks are separate on purpose. Staged edits are working code that is not headed for core. The changes to Typed Data are headed for core and are not yet written as core patches.

## Where the levels live

Every level is one line in `topics.yml` in this site's repository. The [board](../board.md) lists them all. A change of level is its own commit, with the reason in its message.
