#!/usr/bin/env python3
"""The Best Advice I Ever Got — make.fun bounty entry.

Writes exactly one sentence, 1 to 200 characters, to
/output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt). The sentence
is the whole entry: the best advice the writer ever received,
standing alone — no title, no explanation, no second sentence
bolted on.

The house judge reads entries two at a time and keeps the one
that carries the wisest advice, told with the most life. It
weighs them, most important first, on:

1. staying on the subject — a single sentence about the best
   advice the writer ever received, one that strays loses;
2. the advice being worth carrying — specific, earned, and true
   beyond the moment it came from;
3. sounding like a real voice recalling a real moment, not a
   slogan or a fortune cookie;
4. tightness — every word earns its place, the whole thing
   reads in one breath;
5. landing — leaving the reader with something to keep after
   the last word.

A wise-sounding line with no person behind it reads as filler,
and cleverness for its own sake does not count. The gate is
simple: /output/entry.txt must be UTF-8 text of 1 to 200
characters, not only white space.

The lines below are scored on those five, in that order, and
the highest-scoring line wins.

Line A — the father and the waiters. A named giver, a concrete
test anyone can run, and twenty years of checking it: the advice
is earned by time, it stays true beyond the moment, and the
ending lands because it is a verdict, not a wish. It wins on
every count that matters.

Line B — the grandmother and kindness unwatched. A real voice
and a real test, and "checked every person I love against that
sentence since" is genuinely earned. It loses to A on tightness
— "that sentence since" reads a beat slower — and its landing is
a touch softer than A's flat verdict.

Line C — the teacher and listening. "Learned to listen before
I learned to argue" is a good turn, but "being right is
worthless if nobody can hear you" leans toward a slogan, and
the line tells the reader the lesson instead of showing the
moment it was learned.

Line D — the mother and attention. It is neat and quotable, and
that is its problem: it sounds like a fortune cookie, a line
anyone could have written, with no person and no moment behind
it. It loses on the third count before the rest are weighed.

Line E — the mechanic and leaving early. A real giver and a
real trade, and "ready never comes" is true beyond the moment.
It loses to A on freshness — "leave before you are ready" is a
familiar road — and its ending repeats its own advice instead
of landing somewhere new.

Line F — the first boss and the angry email. A concrete habit,
a real workplace, and "the drafts I deleted have saved me more
jobs than the ones I sent" is a genuine turn. It loses to A on
the second count: it is good office practice, but it is not
advice for a whole life.

A wins, so the program writes it — one sentence, about 120
characters, no trailing newline, UTF-8, exactly what the gate
checks.
"""

import os

OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
if not OUTPUT_DIR.strip():
    OUTPUT_DIR = "/output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.txt")

# Each line: (text, on-subject, worth-carrying, real-voice,
# tight, landing), scored 1-5, in the judge's own order.
LINES = [
    (
        "My father said never trust a man who is rude to waiters, "
        "and twenty years later I have never once seen that rule fail.",
        5, 5, 5, 5, 5,
    ),
    (
        "My grandmother told me to marry someone who is kind when "
        "nobody is watching, and I have checked every person I love "
        "against that sentence since.",
        5, 5, 5, 4, 4,
    ),
    (
        "A teacher once told me that being right is worthless if "
        "nobody can hear you, so I learned to listen before I "
        "learned to argue.",
        5, 4, 4, 4, 4,
    ),
    (
        "My mother said the cheapest thing you can give anyone is "
        "your attention, and the most expensive thing you can lose "
        "is theirs.",
        5, 4, 3, 5, 4,
    ),
    (
        "The old mechanic who taught me to drive said to always "
        "leave before you are ready, because ready never comes, "
        "and I have left early ever since.",
        5, 4, 4, 4, 4,
    ),
    (
        "My first boss said never send the email while you are "
        "still angry, and the drafts I deleted have saved me more "
        "jobs than the ones I sent.",
        5, 5, 4, 4, 5,
    ),
]


def choose_sentence(lines):
    """Pick the highest-scoring line; ties break toward the shorter.

    Weights follow the judge's order: staying on subject counts
    most, then the advice being worth carrying, then a real voice,
    then tightness, then the landing. On an exact score tie the
    shorter line wins: the brief's own tie-break prefers the
    smaller text, so a shorter line is strictly better when the
    judge cannot tell two apart.
    """
    weights = (5, 4, 3, 2, 1)
    best = None
    best_score = -1
    for entry in lines:
        text, *marks = entry
        total = sum(w * m for w, m in zip(weights, marks))
        if total > best_score or (
            total == best_score and best is not None and len(text) < len(best)
        ):
            best = text
            best_score = total
    return best


def main():
    sentence = choose_sentence(LINES)
    assert 1 <= len(sentence) <= 200, "entry must be 1-200 characters"
    assert "\n" not in sentence and sentence.strip() == sentence, (
        "entry must be one line"
    )
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(sentence)
    # Read the entry back and prove the gate holds before finishing:
    # UTF-8 text, 1-200 characters, not only whitespace, one line.
    with open(OUTPUT_PATH, "rb") as f:
        written = f.read()
    text = written.decode("utf-8")
    assert text == sentence, "entry differs from the chosen line"
    assert 1 <= len(text) <= 200 and text.strip(), "gate failed: bad length"
    assert "\n" not in text, "gate failed: entry is not one line"


if __name__ == "__main__":
    main()
