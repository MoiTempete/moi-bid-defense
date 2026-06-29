# Contributing

Thanks for helping improve `moi-bid-defense`.

This project is a Skill for AI agents that generate bid defense presentation slides from completed technical response documents. The most useful contributions are specific, reproducible, and tied to real defense presentation output.

## Before Opening an Issue

Please check whether the problem belongs to one of these buckets:

- Parsing accuracy: the response parser misses section structure, star references, or quantitative metrics.
- Extraction quality: the golden thread scoring model misses important content or overweights boilerplate.
- Slide content quality: generated slides are too generic, lack speaker notes, or miss differentiation points.
- Q&A anticipation: missed obvious judge questions or gave vague answers.
- HTML output: Swiss/magazine style rendering issues, layout problems, or dark/light theme defects.
- Script behavior: `parse_response.py` or `extract_threads.py` produce errors or unexpected output.
- Documentation: installation, usage, or workflow instructions are unclear.

When reporting, please include:

- The response document (if shareable) or a description of its content and structure.
- The slide deck generated and the specific issues.
- The agent and environment used (Claude Code, Codex, etc.).

## Pull Request Guidelines

Keep PRs focused. A small fix with a clear before/after example is easier to review than a large rewrite.

### For parsing changes (`scripts/parse_response.py`):

- Test against at least one real response document (or a representative fixture).
- Keep the JSON output schema backward-compatible.
- New metric categories should be documented.

### For extraction changes (`scripts/extract_threads.py`):

- Test the three scoring dimensions (Pain Point / Differentiation / Quantitative Impact) independently.
- New scoring rules should include the regex pattern, point value, and rationale comment.
- Verify that the topic classification (`classify_theme`) still produces reasonable distributions.

### For strategy guide changes (`references/defense-strategy.md`):

- New strategies should include audience, rhythm, per-slide characteristics, and common pitfalls.
- Speaker note templates should be concrete and actionable, not abstract.

### For workflow changes (`SKILL.md`):

- Keep the 5-step workflow structure clear.
- Each step should state its input, output, and exit criteria.
- User confirmation gates (Step 2, Step 3, per-page in Step 4) must not be removed.

### For HTML generation (Step 5):

- Test the full pipeline: markdown → 投喂版 → guizang-ppt → HTML.
- Verify all slides render correctly in Chrome/Safari/Firefox.
- Check Swiss style rules: no serif fonts, no gradients, no rounded corners, single accent color.
- Verify text readability at projection sizes (body ≥18px, description ≥16px, label ≥14px).
- Check that speaker notes are NOT visible on slides.

## Good PRs Usually Include

- A short summary of the problem.
- The exact files changed.
- Before/after output snippets (slide content, extraction scores, or HTML screenshots).
- Test results or validation notes.

## Style Notes

This Skill is opinionated by design. It prefers structured, impactful defense slides with honest Q&A anticipation over generic bullet-point decks. The constraints (title as assertion, one core number per slide, speaker notes required) make AI-generated presentations more valuable for real bid defenses.

When in doubt, preserve the existing workflow structure and improve the quality around it.

## Key Design Decisions

- **Golden thread extraction first**: Content must be scored before outline generation. This prevents "everything looks important" paralysis.
- **Pain point + Differentiation + Quantification**: The three scoring dimensions ensure slides address client needs, showcase uniqueness, and provide memorable numbers.
- **Style must be confirmed before outline**: Prevents mismatch between narrative strategy and content.
- **Outline must be confirmed before writing**: Prevents wasted writing effort on wrong structure.
- **Slide-by-slide confirmation**: Allows course correction without regenerating the entire deck.
- **Markdown before HTML**: Separates content authoring from visual rendering, making content review independent of styling.
- **Separation of slides and notes**: Speaker notes must never appear on slides. This is enforced at the 投喂版 editing step.
