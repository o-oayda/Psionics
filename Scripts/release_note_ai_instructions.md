# Psionics Release Notes Drafting Brief

Use these guardrails whenever you generate draft release notes for the Psionics project.

## Tone & Structure
- Audience is tabletop players and GMs; write in concise, informative prose.
- Keep headlines short and section-focused. Preferred sections (in order): `System & Rules`, `Powers`, `Classes & Subclasses`, `For Your Review`.
- Use bullet lists for change details. Each bullet should describe player-facing impact first. Don't speculate about the rationale of the change, just stick to the facts.
- Reference feature names in backticks (e.g., `Kinaesthetic Disruption`) and class names in plain text.
- Avoid speculation and implementation minutiae; surface only changes that affect players.
- Refer to the player in third person, i.e. 'the player'. Don't use second person. If in reference to a power, remember the creator of the power is called the 'manifester'.
- When referencing changes to powers, put powers on a new bullet. Don't refer to changes to multiple powers or multiple new powers on the same bullet, unless relevant to the point at hand.
- Be sure to mention which class list the new powers have been added to---you will see this in the diffs.

## Content Priorities
- Summarise notable mechanical updates: new subsystems, renamed terms, rule clarifications.
- Highlight new or reworked powers with level, discipline, and the new behaviour.
- Call out class feature changes that alter gameplay expectations.
- Mention balance tweaks (dice changes, MB adjustments) only when they influence end-user experience.
- Close with a short review checklist or callouts to prompt human verification of high-impact updates.

## Source Material To Consider
- Diff since the previous `v*` tag (commit subjects and diffstat are supplied by the caller).
- Existing release notes in `release_notes/` for tone cues.
- Any additional context provided in the invocation prompt.

## Formatting Rules
- Begin with a level-1 heading: `# Psionics v<version> (Draft)` unless the caller specifies a different title.
- Separate sections with blank lines; avoid trailing spaces and Markdown tables unless necessary.
- Do not include unreleased roadmap items or TODOs.

## Safeguards
- If information is missing or ambiguous, call it out in the draft so a human can follow up.
- Never assume the release has shipped; frame the document as a draft awaiting review.
