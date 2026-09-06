# YouTube Script (ELI5): "Why Are Planets Parked Where They Are?"

[← Repository Overview](../../README.md) | [Full Research Paper](../../paper/EIGENMODE-ORBITAL-DYNAMICS.md)

**Purpose:** A short, plain-language narration script for a companion YouTube video explaining the core idea of [paper/EIGENMODE-ORBITAL-DYNAMICS.md](../../paper/EIGENMODE-ORBITAL-DYNAMICS.md) to a general audience, for cross-linking between the video and the full paper.

**Target length:** ~3–4 minutes spoken (roughly 500–550 words).

**Suggested visuals:** noted in `[brackets]` — pulls from the simulation and renders suite (screenshot / MP4) and simple on-screen text/diagrams.

---

## SCRIPT

**[Visual: slow zoom on the Solar System, planets as dots, orbits as thin rings]**

Here's a question most of us never think to ask: why is Mercury where Mercury is? Why isn't it a bit closer to the Sun, or a bit farther out? Why does Earth sit exactly where it sits, and not, say, halfway between Earth and Mars?

The textbook answer is: it's random. Planets form out of a swirling disk of gas and dust, they crash into each other, they scatter around, and wherever they end up is just... wherever they end up. No pattern. Cosmic dice roll.

**[Visual: simple chaotic scatter of dots — "the textbook picture"]**

But here's the strange part. If you plot the distance of every planet from the Sun — not on a normal ruler, but on a *ratio* scale, where each step means "twice as far" or "three times as far" instead of "one mile farther" — something odd shows up. The planets don't look random at all. They line up almost perfectly evenly spaced.

**[Visual: the log-scale ladder diagram from the paper — r0, n=1 Mercury, n=2 Venus, etc.]**

And it's not just our Solar System. Do the same trick with Jupiter's big moons. Same pattern. Saturn's moons. Same pattern. Uranus's moons. Same pattern. Point a telescope at a star trillions of miles away with its own family of planets — TRAPPIST-1, Kepler-90, a dozen others — same pattern again.

That's a big coincidence to write off as "random."

**[Visual: side-by-side comparison of 3-4 different systems, all snapping to the same ladder shape]**

So this paper asks: what if it's *not* random? What if there's an actual physical reason planets can only "park" at certain distances — like rungs on a ladder — and empty rungs are just empty, the way an empty parking space is still a parking space?

Here's the idea in one picture: think of the space around a star not as empty vacuum, but as a medium — like water, or air — that carries waves outward from the star, the same way a struck bell rings with specific pure notes instead of just any random sound.

**[Visual: ripple/standing-wave animation from the visualizer, cymatics-style rings]**

A star's environment naturally sets up standing waves in that medium — quiet zones and node points, exactly like the still points you see in a vibrating bowl of water, or the fixed points on a guitar string that don't move no matter how hard you pluck it. Matter drifting through that environment tends to settle at those quiet points, because that's where the push and pull cancel out.

Do the math on that setup properly, and you get an equation: each "rung" on the ladder is a fixed multiple of the one before it. Rung 1, then rung 1 times some number, then that times the same number again, and so on. That's exactly the pattern we see in real planets and real moons.

**[Visual: the equation r_n = r0 · k^n, animated build-up]**

Now — and this part matters — this paper doesn't claim every rung has a planet sitting on it. It claims those are the *only* legal parking spots. Some spots are empty. Some, like our asteroid belt, are only half-filled — leftover rubble that never fully came together into one world.

**[Visual: asteroid belt sitting on its "rung," labeled "occupied by debris, not by one planet"]**

And this isn't just a story — it's built to be provably wrong if it's wrong. The paper makes actual predictions: specific empty rungs in specific real star systems where, if this idea is right, we should eventually find a planet — or definitively *not* find one. Real telescopes can check that. That's the whole point of a real scientific claim: it has to be able to fail.

**[Visual: end card — link to full paper + visualizer]**

So — are planets really just randomly scattered debris? Or are they settling into the rungs of a cosmic standing wave? The maths, the data, and the predictions are all laid out in full in the paper linked below. Go check the working.

---

## Shorter Cold-Open / Hook Variant (first 15 seconds, if needed separately)

> "Why is every planet in the Solar System sitting *exactly* where it is — and not ten miles to the left? Turns out, that might not be a random question. There might be a ladder."

---

## Notes for Recording

- Keep tone curious, not preachy — this is "here's a cool pattern and a testable idea," not "here's the truth they don't want you to know."
- Avoid overly academic or esoteric terminology — use plain "wave medium" / "standing wave" language so the video stands alone for a general audience.
- The simulation (`simulation/index.html`, served via `python3 -m http.server 8085`) and `summation-video/video/eigenmode_orbital_simulation.mp4` are the primary b-roll source.
