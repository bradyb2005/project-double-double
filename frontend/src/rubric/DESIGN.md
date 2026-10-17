# RUBRIC

*A design language for interfaces built with LLMs. One red. One display face. One mono voice.*
*Made with AI. Doesn't look it.*

**rubric** (n.) — in old manuscripts, a heading set in red ink (Latin *ruber*, red); also a set of criteria to judge by. This is both: a language built on one full-bleed red, and the rules and audit that keep generated UI from drifting back to average.

**Read this file and `specimen.html` before writing any UI. Use only the classes and tokens below. Do not invent values.**

Lineage: the structure of the Hermes Agent site (a saturated full-bleed color field, huge thin compressed headlines against tiny tracked labels, hairline frames, duotone art), rebuilt with free fonts, a pinned-art parallax, and a swappable hue so it is its own thing.

## Files

| File | Purpose |
|---|---|
| `tokens.css` | Fonts, hue presets, palette, type scale, spacing, shape. The only place raw values live. |
| `components.css` | Every component. Imports `tokens.css`. Link this one file. |
| `ui.js` | Menu, tabs, accordion, copy, form validation. No dependencies. |
| `scene3d.js` | Optional. The pinned art as a real 3D scene (hand-written WebGL2 shader, no dependencies). See `data-scene`. |
| `specimen.html` | Every component in both modes. Copy sections from it; do not redesign them. |
| `fonts/`, `assets/` | Self-hosted fonts (JetBrains Mono, Big Shoulders Display) and `panorama.png`, a sample duotone-ready engraving. |
| `LOOP.md` | The build-render-audit-fix loop and exit criteria. Read it with this file. |
| `tools/shot.mjs`, `package.json` | The render + audit tool (Playwright, Chromium and WebKit). `npm install && npm run setup` once. |

New project: copy this folder in, `cd rubric && npm install && npm run setup`, link `components.css` and `ui.js`, set `<html data-hue="…">`, copy section markup from `specimen.html`.

**Scope:** this is a marketing-site and landing-page parts kit (nav, hero, feature grid, tabs, accordion, form, pricing, footer, empty and loading states). App UI such as tables, data views, dashboards, dialogs, toasts and dense navigation is not covered yet. Extend it in the same language (add the component to `specimen.html`, run the loop) before inventing ad hoc styles.

## The rules (these are what stop it looking like slop)

1. **One hue, used as a whole section.** Rubric's hue is #FF0A01. Every color is a shade of it. Sections alternate `mode-field` (saturated color, paper text) and `mode-paper` (tinted off-white, ink text). Color is a field, never just a button accent.
2. **Thin giants, tiny labels.** Headlines: Big Shoulders Display, weight 300 (400 for titles under 48px), sentence case, line-height ~0.92, set huge. Everything else: JetBrains Mono. The size gap between the two is the style, so do not close it.
3. **Mono is a voice, not a costume.** Mono for body, labels, nav, buttons, numbers and code. Never a headline, never above 24px, never on a black background, no ligatures.
4. **Flat.** Radius 3px (controls) or 5px (plates, panels). Depth is a 1px inset ring (`var(--ring)`). No drop shadows, no glows, no gradients except inside `.plate` and `.duo`.
5. **4px grid, stepped.** Spacing only from `--s-1…--s-10`. Spacing is never fluid; it changes at breakpoints. Only type is fluid.
6. **Editorial devices, sparingly.** Numbered eyebrows (`#1 HUE`), `//MOST POPULAR` tags, a superscript mark on a heading, a hairline frame around the viewport, a giant faded wordmark in the footer. Use two or three per page, not all.
7. **Imagery is real art in the brand duotone,** or a generated `.plate`. Never stock photos, never gradient blobs, never emoji or sparkle icons.
8. **Art and solid alternate, and the art is pinned.** With `data-art="full"`, full-bleed art fills the hero, one or two middle sections and the footer; between them the sections are solid. The art is pinned to the viewport, so every art section is a different view of the same picture. Art never goes behind a form or dense reading text.

## Color

Set `<html data-hue="…">`. **Rubric's color is `rubric`: #FF0A01, the default.** Other presets exist for other projects. Each preset carries its own lightness and chroma, because equal OKLCH lightness is not equal contrast.

| Preset | Color | Paper-on-field | Note |
|---|---|---|---|
| `rubric` (default) | #FF0A01 | 3.6:1 | The brand. Fire-engine red. |
| `oxblood` | #B00000 | 6.7:1 | The deep alternate. Passes AA easily. |
| `vermilion` | warm orange-red | passes | Reference |
| `cobalt` | electric blue | passes | Closest to Hermes |
| `magenta`, `teal`, `pine`, `ochre` | | pass | Available; pine and ochre are riskier (terminal-green cliché, muddy) |

### The brand's one exception: contrast
Paper on #FF0A01 is 3.6:1. That is right for headlines and art (they pass the 3:1 large-text bar) but **below WCAG AA (4.5:1) for small text**. Rubric treats this as a deliberate, documented exception:

- `data-contrast="brand"` (default): the exact red. The audit allows small text down to 3.5:1 and lists how many items are below AA in its notes, every run.
- `data-contrast="aa"`: the same red nudged to **#DA0A01** (4.7:1). Everything passes WCAG AA. Use this for any product where AA is required, and for anything people have to read at length.

Custom color: convert the hex to OKLCH, set `--hue`, `--chroma`, `--field-l` (and `--fg2-mix` if muted text needs lifting), then run `node tools/shot.mjs <page> --hue <name>`.

## Display options (state lives on `<html>`)

| Attribute | Values | What it does |
|---|---|---|
| `data-hue` | a preset name | Color (see above). Default `rubric`. |
| `data-contrast` | `brand` (default), `aa` | See above. |
| `data-art` | `window`, `full` | `window`: the hero art is a framed picture beside the copy; other sections are solid. `full`: pinned full-bleed art fills the hero, any `.art-section`, and the footer, **alternating with solid sections** (hero art, work solid, about art, contact solid, footer art). The art is pinned to the viewport, so each section is a different view of the same picture. |
| `data-scroll` | `smooth` (default), `native` | `smooth`: inertial wheel scrolling (built into `ui.js`, no dependency). `data-scroll-speed` (1-100, default 50) sets how smooth: an exponential glide whose time constant is linear in the number, 50 = the default ease (11% per frame), 100 = three times as long; the Tweaks slider runs 0 (native) to 100, and `?scroll=0..100` works too. Desktop with a mouse or trackpad only; touch keeps native momentum; off for `prefers-reduced-motion`. Keyboard, scrollbar drags and nested scrollers stay native. `#anchor` links glide and honor `scroll-padding-top`. |
| `data-scene` | `flat` (default), `3d` | `3d`: needs `<script src="rubric/scene3d.js" defer>`. The pinned art becomes a real 3D scene: hatched planets, a ring and orbits drawn as engraving, rendered once per frame in WebGL2 and cropped into every `.window`. The choreography (all driven by scroll, none by time): Saturn spins and slides off to the left as soon as the page scrolls. The planets the hero copy hides sit on the left and start following their orbits once About comes into view. Near the end of About the camera whips round to the top-down footer view while Saturn returns to the centre and the planets settle, so the footer shows the whole system. Ring bands, planet bands and orbit ticks turn at their own speeds. The views are named in `scene3d.js` (`VIEWS`). Black ink on white, so `.duo` / `.duo--inv` give it the hue and AA mode for free. Falls back to the `<img>` when WebGL2 is missing, the context is lost, or the user prefers reduced motion. The footer wordmark uses `assets/panorama-3d.png` (regenerate with `node tools/scene-still.mjs`). Cost: about one 2-megapixel shader pass per frame while art is on screen. |
| `data-motion` | `journey` (default), `fixed`, `original`, `astronaut` | Only with `data-scene="3d"`. `journey`: the scroll choreography above. `fixed`: Saturn spins in place on the hero's right, the hidden planets sit still, About pans to them and zooms in slowly, the footer is the plain top-down view, no whip. `original`: the first 3D version. The camera orbits Saturn from section to section and the planets follow real orbits with the scroll, but they sit on wide orbits, so most are off-screen or behind the copy and only Saturn reads. `astronaut`: no other planets. Saturn follows the original camera path through the hero and drifts off to the right; the third page (About, needs `data-art="full"`) is an astronaut floating from left to right (a ray-marched SDF in the same shader, a faint ghost under the copy on desktop); Saturn is back at the bottom as in the original. All four are kept as switches. |

All of them can be set from the URL (`?hue=oxblood&art=full&scene=3d&motion=fixed&scroll=native&contrast=aa`) and are remembered in `localStorage`. The `details.dock` Tweaks panel exposes them as buttons (`<button data-opt="art" data-val="full">`). It is a dev aid: remove it before shipping.

### Art sections (`data-art="full"`)
- **Hero:** needs `class="… hero-section"`. The art fills it, masked out under the copy.
- **Any section:** add `art-section` and, as its first child, `<div class="art-bg" aria-hidden="true"><div class="duo duo--inv window"><img …></div></div>`. `art-bg` shows the art on the left (copy on the right on desktop); `art-bg--all` unmasked; `art-bg--dim` lower opacity. On phones and tablets tall sections get uniformly dim art, because the art is pinned to the viewport and a fade cannot keep it off text in a section taller than the screen.
- **Footer wordmark** (`.art-footer .ghost`): the word is a window onto the same pinned art, bright inside the letters and dim outside. It needs `data-text="…"` matching its text (a pale copy on top keeps it readable). `--ghost-fill` (default 0.5) sets how pale the letters are.
- **Solid sections between art sections stay solid.** Never put art behind a form.

### Footer
The footer's label and links sit on the **same solid as the section above** (`.footer-solid`, same paper as Contact, divided from it by a hairline), not on a bar of their own. The art footer (`.art-footer`, with the ghost wordmark) starts directly below.

### Floating CTA
`<a class="btn cta-float" data-float-cta href="#contact">` is a solid button that stays on screen on desktop. It flips to field-on-paper or paper-on-field to stay legible over whatever is under it, and steps away once `nav[aria-label="Footer"]` is on screen. Phones get the CTA in the menu instead.

## Type

| Token | Value | Use |
|---|---|---|
| `--t-hero` | clamp(64, 12vw, 152) | `.display` (hero uses a container-relative size) |
| `--t-h2` | clamp(48, 7vw, 96) | `.h2`, price figures |
| `--t-h3` | clamp(32, 3.4vw, 44) | `.h3` titles, heading marks |
| `--t-body` 15 · `--t-small` 13 · `--t-label` 12 · `--t-micro` 11 | | body, secondary, tracked uppercase labels, smallest legal size |

Minimum 11px anywhere. Body is 15px. Inputs are 16px (stops iOS zoom). At most 10 distinct sizes on a page.

## Modes

Put `mode-field` or `mode-paper` on a `.section`. Components read only the semantic vars it sets (`--bg --fg --fg-2 --line --ring --panel --btn-bg --btn-fg --plate-bg`), so any component works in either mode. Never hard-code a color inside a component.

## Components (all in `specimen.html`)

`header` + `.nav-links` + `.menu-toggle` + `.menu-panel` · `.display .h2 .h3 .eyebrow .label .small .micro .muted` · `.btn` `.btn--ghost` `.btn--block` `.link` · `.hero` · `.grid--3 / --4` · `.feature` + `.plate--{rays,rings,grid,bars,dots,waves}` · `.duo` / `.duo--inv` (duotone) · `.window` (pins the art to the viewport so frames reveal different parts of one picture as you scroll; pure CSS, static under reduced motion; use a landscape panorama like `assets/panorama.png`) · `.term` tabs + copy · `.acc` accordion · `.field` + `.input` + `.check` form · `.tier` pricing · `.empty` and `.loading` states · `.work-list` + `.work` editorial rows · `.fact` label/value rows · `.dock` Tweaks panel (collapsible; hue swatches and `.seg` toggles via `data-opt` / `data-val`) · `.cta-float` · `.footer-solid` · `.art-section` / `.art-bg` · `.swatch` · `.ghost-wrap .ghost` footer wordmark · `.footer-row`.

Duotone: `.duo` (dark linework on paper, for paper sections) or `.duo--inv` (light linework melting into the field, for field sections). Drop in any photo. Source real art that is free to use: Met Museum Open Access, Rijksmuseum, Wikimedia Commons, Biodiversity Heritage Library engravings. Keep the contrast high; hatching, engravings and halftones suit the style.

## Responsive contract

Breakpoints: `600`, `1024`, `1440`. Every screen is composed for its size, not squeezed:

| Width | Layout |
|---|---|
| < 600 phone | Single column. 20px gutters. Buttons full width and ≥ 44px tall. Nav collapses to a full-screen menu panel with display-size links. Full-bleed art fades in below the copy; tall sections get uniformly dim art. |
| 600–1023 tablet | Two-column grids. 32px gutters. Menu panel still used. Buttons inline. |
| ≥ 1024 desktop | Inline nav. Hero is 7/5 columns. 3- and 4-column grids. 48px gutters. |
| ≥ 1440 wide | Content caps at 1280px. Type reaches its maximum. |

Every control is reachable by touch, mouse and keyboard at every width, with a visible focus ring. Never hide a nav destination without giving it another route.

## Banned

Purple/blue gradient backgrounds · glassmorphism · icon-in-a-circle feature grids · centered hero with two buttons over a gradient · uniform rounded cards with soft shadows · emoji or sparkles as icons · pure `#000` or `#fff` · mono headlines · mono above 24px · green or cyan on black · blinking cursors, typewriter effects, decorative `>` or `~/` prompts · glow borders · dark-only themes · lorem ipsum, "Acme", "John Doe" · hover-only reveals (touch has no hover) · fluid spacing.

## Prompting an LLM with this

> Build `<page>` using the Rubric design language. Read `rubric/DESIGN.md` and `rubric/specimen.html` first. Use only existing classes and tokens; copy section markup from the specimen. Then follow `rubric/LOOP.md` until it passes.
